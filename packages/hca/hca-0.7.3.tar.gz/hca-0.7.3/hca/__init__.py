"""HCA DCP CLI."""

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import requests
import sys

# from .define_api import API


def main():
    """Entrance to functionality."""
    # cli = API()
    # response = cli.make_request(sys.argv[1:])
    response = requests.get("www.example.com")
    if isinstance(response, requests.Response):
        print(response.content.decode())
    else:
        print(json.dumps(response))
