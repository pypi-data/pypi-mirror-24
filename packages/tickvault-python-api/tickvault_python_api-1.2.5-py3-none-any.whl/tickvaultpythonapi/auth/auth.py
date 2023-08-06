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
Custom Auth classes
'''

import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


class BasicAuth(HTTPBasicAuth):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


class OAuth(AuthBase):
    
    def __init__(self, secret):
        self.secret = secret
        
    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = "Bearer " + self.secret
        return r


if __name__ == '__main__':
    
    r = requests.get("http://httpbin.org/", auth=BasicAuth("user","pass"))
    print(r.request.headers)
    
    r = requests.get("http://httpbin.org/", auth=OAuth("pass"))
    print(r.request)
    print(r.request.headers)