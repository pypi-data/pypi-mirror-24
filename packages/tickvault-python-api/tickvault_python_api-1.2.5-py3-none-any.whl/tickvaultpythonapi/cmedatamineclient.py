#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017 TickSmith Corp.
# 
# Licensed under the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


'''
Python wrapper for TickSmith Query API - Specific to CME
'''

import ujson
from tickvaultpythonapi.client import BaseClient
from tickvaultpythonapi.auth.auth import BasicAuth
from tickvaultpythonapi.parsing.parse import Parser
from tickvaultpythonapi.parsing.predicate import BasePredicate


class CmeDatamineClient(BaseClient):

    def __init__(self, user_name, password, base_url="https://datamine.cmegroup.com/cme"):
        '''
        Keyword args:
            user_name -- UNO API ID
            password -- UNO API password
        '''
        self.base_url = base_url
        self.api_url = self.base_url + "/api/v1"
        self.user_name = user_name
        self.password = password

        self.auth = BasicAuth(self.user_name, self.password)

    def _query_bitcoin(self, dataset, date_from, date_to):
        """
        Queries a CME bitcoin dataset with the given arguments
    
        Keyword args:
            dataset -- BRR/FEED
            date_from -- Start time of query (format: yyyymmdd)
            date_to -- End time of query (format: yyyymmdd)
    
        Returns:
            The result of the query as a JSON list
        """
        # Define endpoint pattern and the dictionary containing k-v pairs to replace the placeholders
        endpoint_pattern = self.api_url + "/query/{ds}/{dateFrom}/{dateTo}"

        replace_dict = {'ds': dataset,
                        'dateFrom': date_from, 
                        'dateTo': date_to}

        result = self.run_query(pattern=endpoint_pattern,
                                replace_dict=replace_dict,
                                auth=self.auth)

        # Result's first line is useles, hence result.split("\n")[1:]
        # Each line in result.split("\n")[1:] has a leading and trailing comma, hence x[1:-1]
        return [ujson.loads(x[1:-1]) for x in result.split("\n")[1:] if x]   

    def query_brr(self, date_from, date_to):
        """
        Queries the BRR CME bitcoin dataset with the given arguments
    
        Keyword args:
            date_from -- Start time of query (format: yyyymmdd)
            date_to -- End time of query (format: yyyymmdd)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_bitcoin("btc_brr", date_from, date_to)

    def query_feed(self, date_from, date_to):
        """
        Queries the FEED CME bitcoin dataset with the given arguments
    
        Keyword args:
            date_from -- Start time of query (format: yyyymmdd)
            date_to -- End time of query (format: yyyymmdd)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_bitcoin("btc_feed", date_from, date_to)

    def _query_dataset(self, dataset, exchange, date_from, date_to, period, product_codes, predicates=""):
        """
        Queries a CME dataset with the given arguments

        Keyword args:
            dataset -- EOD
            date_from -- Start time of query (format: yyyymmdd)
            date_to -- End time of query (format: yyyymmdd)
            period -- The period of the files (values: e/p/f) (early, preliminary, late)
            product_codes -- The symbol(s) to query (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")

        Returns:
            The result of the query as a JSON list
        """
        # Define endpoint pattern and the dictionary containing k-v pairs to replace the placeholders
        endpoint_pattern = self.api_url + "/query/{ds}/{exchange}/{dateFrom}/{dateTo}/{period}/{prods}"

        replace_dict = {'ds': dataset,
                        'exchange': exchange,
                        'dateFrom': date_from, 
                        'dateTo': date_to,
                        'period': period,
                        'prods': self._list_to_str("product codes", product_codes)}

        # Parse predicates 
        parsedPredicates = Parser(BasePredicate).parseString(predicates)

        return self.run_query(pattern=endpoint_pattern,
                              replace_dict=replace_dict,
                              auth=self.auth,
                              predicates=parsedPredicates)

    def query_eod(self, exchange, date_from, date_to, period, product_codes, predicates=""):
        """
        Queries the EOD CME dataset with the given arguments

        Keyword args:
            exchange -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)

        Returns:
            The result of the query as a JSON list
        """
        return self._query_dataset("eod", exchange, date_from, date_to, period, product_codes, predicates)


if __name__ == "__main__":
    #cme = CmeDatamineClient(user_name="API_ali.aqueel@ticksmith.com", password="Smalldata$")
    '''
    result = cme.query_brr(date_from=20170108, date_to=20170426)
    print(result)
    
    result = cme.query_feed(date_from=20170411, date_to=20170426)
    prices = []
    for entry in [x for x in result if 'mdEntries' in x]:
        prices.append({'transactTime': entry['transactTime'],
                       'price': entry['mdEntries'][0]['mdEntryPx']})
    df = cme.as_dataframe(in_list=prices, index="transactTime")

    print(df.head())
    print(df.info())
    print(df.describe())
    df = df.astype(float)
    df.plot()
    '''
    
    #result = cme.query_eod(exchange="xcme", date_from=20170830, date_to=20170830, 
    #                       period="f", product_codes=['ze'])
    #print(result)
