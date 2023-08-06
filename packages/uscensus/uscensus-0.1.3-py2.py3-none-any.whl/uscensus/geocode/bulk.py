"""Bulk geocoding API wrapper.

Attributes:
    CENSUS_GEO_COLNAMES: column names in output from geocoding API.
"""
from __future__ import print_function, unicode_literals

import csv
import fiona
from io import StringIO
from itertools import islice
import numpy as np
import geopandas as gpd
from gevent.pool import Pool
import glob
import grequests
import os
import os.path
import pandas as pd
import grequests
import shapely
import sqlalchemy

CENSUS_GEO_COLNAMES = [
    'Key',
    'In.Address',
    'Match',
    'Exact',
    'Geo.Address',
    'Geo.Lon.Lat',
    'Geo.TIGER.LineID',
    'Geo.TIGER.Side',
    'Geo.FIPS.State',
    'Geo.FIPS.County',
    'Geo.Tract',
    'Geo.Block',
]


def chunker(n, iterable):
    iterable = iter(iterable)
    return iter(lambda: list(islice(iterable, n)), [])


class FilePersister(object):
    def __init__(self, tempOut, finalOut):
        self.temp = tempOut
        self.cols = None
        self.final = finalOut
        self.idx = 0
        os.makedirs(os.dirname(self.temp))
        os.makedirs(os.dirname(self.final))

    def prepare(self, cols):
        self.cols = cols

    def persistTemp(self, rows):
        with open(self.temp.format('000{}'.format(self.idx)[-4:]), 'w') as f:
            wr = csv.DictWriter(f, fieldnames=self.cols)
            wr.writerows(rows)
        self.idx += 1

    def persistFinal(self):
        with open(self.final, 'w') as f:
            f.write(','.join(self.cols))
            f.write('\n')
            for fn in glob.glob(self.temp.format('*')):
                with open(fn) as part:
                    data = part.read()
                    f.write(data)
                    if not data.endswith('\n'):
                        f.write('\n')
        return pd.read_csv(
            self.final,
            dtypes={
                'Key': int,
                'Geo.TIGER.LineID': str,
                'Geo.FIPS.State': str,
                'Geo.FIPS.County': str,
                'Geo.Tract': str,
                'Geo.Block': str,
            })


class SqlAlchemyPersister(object):
    def __init__(self, connstr, table, if_exists):
        self.connstr = connstr
        self.engine = sqlalchemy.create_engine(self.connstr)
        self.table = table
        self.cols = None

    def prepare(self, cols):
        self.cols = cols
        with self.engine.begin() as conn:
            md = sqlalchemy.MetaData()
            sqlalchemy.Table(
                self.table,
                md,
                *(
                    sqlalchemy.Column(
                        col, sqlalchemy.String
                    )
                    for col in self.cols
                )
            )
            md.create_all(bind=conn)

    def persistTemp(self, rows):
        with self.engine.begin() as conn:
            md = sqlalchemy.MetaData(bind=conn)
            tbl = sqlalchemy.Table(self.table, md, autoload=True)
            s = tbl.insert()
            params = list(rows)
            conn.execute(s, *params)

    def persistFinal(self):
        ret = pd.read_sql(
            'SELECT * FROM "' + self.table + '"',
            self.connstr,
        )
        ret.dtypes['Key'] = int
        return ret

class CensusBulkGeocoder(object):
    """Geocode many addresses."""
    def __init__(
            self,
            persister,
            endpoint='https://geocoding.geo.census.gov/geocoder/geographies/addressbatch',
            benchmark='Public_AR_Current',
            vintage='Current_Current',
            chunksize=1000,
            concurrency=10,
    ):
        self.persister = persister
        self.endpoint = endpoint
        self.benchmark = benchmark
        self.vintage = vintage
        self.chunksize = chunksize
        self.concurrency = concurrency
        # set headers
        self.persister.prepare(CENSUS_GEO_COLNAMES)

    def _generate_requests(
            self,
            rows,
            session=None
    ):
        for idx, chunk in enumerate(chunker(self.chunksize, rows)):
            print('Processing chunk #{}: geocoding {} addresses'.format(
                idx,
                len(chunk)))
            sio = StringIO()
            csv.writer(sio).writerows(chunk)
            req = sio.getvalue().rstrip()
            params = {
                'benchmark': self.benchmark,
                'vintage': self.vintage,
            }
            files = {
                'addressFile': ('Addresses.csv', StringIO(req), 'text/csv')
            }
            yield grequests.post(
                self.endpoint,
                params=params,
                files=files,
                stream=False,
                session=session)

    def geocode_addresses(self, key, street, city, state, zip5, session=None):
        """The main geocoding routing.

        Arguments:
          * key: unique identifiers.
          * street: street addresses.
          * city: city names.
          * state: state abbreviations.
          * zip5: ZIP codes as strings.

        Returns: DataFrame with geocoding output with rows keyed by
          the input key.
        """
        reqiter = self._generate_requests(
            zip(key, street, city, state, zip5),
            session=session,
        )
        reqs = list(reqiter)
        req_to_idx = {req: idx for idx, req in enumerate(reqs)}

        def handleResp(idx, req, retry=True):
            chunkno = req_to_idx.get(req, 'N/A')
            if req.response is not None:
                print('Finished req {}/{} for chunk#{}'.format(
                    idx+1, len(reqs), chunkno))
                r = req.response
                if r.status_code == 200:
                    rdr = csv.DictReader(
                        StringIO(r.text),
                        fieldnames=CENSUS_GEO_COLNAMES,
                    )
                    self.persister.persistTemp(rdr)
                else:
                    print('Failed req {}/{} for chunk#{}: '
                          'status_code={}'.format(
                              idx+1, len(reqs), chunkno,
                              r.status_code))
                    req.response = None
                    reqs.append(req)
            else:
                print('Failed req {}/{} for chunk#{}: '
                      'exception={}'.format(
                          idx+1, len(reqs), chunkno,
                          req.exception))
                if retry:
                    print('Retrying...')
                    req.send()
                    handleResp(idx, req, False)

        print('Processing {} requests'.format(len(reqs)))
        # reimplement grequests.imap so that we get back the
        # request object to use as a correlator.
        pool = Pool(self.concurrency)
        for idx, req in enumerate(
                pool.imap_unordered(grequests.AsyncRequest.send,
                                    reqs)):
            handleResp(idx, req)
        print('Processed {} responses'.format(idx+1))
        df = self.persister.persistFinal()
        return df
