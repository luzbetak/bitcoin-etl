# The MIT License (MIT)
#
# Copyright (c) 2018 Omidiora Samuel, samparsky@gmail.com
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
import base64
import json

from web3 import HTTPProvider
from web3.utils.request import make_post_request


class BatchRPCProvider(HTTPProvider):

    def __init__(self, provider_uri):
        self.provider_uri = provider_uri

    def make_request(self, commands):
        rpc_calls = []
        for command in commands:
            m = command.pop(0)
            rpc_calls.append({"jsonrpc": "2.0", "method": m, "params": command, "id": "1"})
        text = json.dumps(rpc_calls)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.provider_uri,
            request_data,
            timeout=60
        )

        response = self.decode_rpc_response(raw_response)

        result = []
        for resp_item in response:
            if resp_item.get('result') is None:
                raise ValueError('"result" is None in the JSON RPC response {}', resp_item.get('error'))
            result.append(resp_item.get('result'))
        return result

    def getblockhash(self, param):
        response = self.make_request([['getblockhash', param]])
        return response[0] if len(response) > 0 else None

    def getblock(self, param):
        response = self.make_request([['getblock', param]])
        return response[0] if len(response) > 0 else None

    def getblockcount(self):
        response = self.make_request([['getblockcount']])
        return response[0] if len(response) > 0 else None
