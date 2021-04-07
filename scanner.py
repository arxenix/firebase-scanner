#Modifications to fix a few issues I ran into

from typing import Tuple
from io import StringIO
from argparse import ArgumentParser, FileType
import requests
import json
import sys

common_endpoints = [
        "",
        "users",
        # TODO - users/$uid - extract uid from JWT?
        "groups",
        "messages",
        "posts",
        "chats",
]

# TODO - attempt using different values to check value filters
value_attempts = [
        "1",
        "0",
        "-1",
        "1566889891"
        "true",
        "false",
        "a",
        "null",
        "-JSOpn9ZC54A4P4RoqVa",
        "591dd66c-ffb0-4f7c-80f2-13345066a159"
]


def try_endpoint(args, site, endpoint):
    #.code is not a field of args; this was causing an exception
    #Instead, we want the current site from the for loop
    #Also, we need to check if it's the entire url or just the code portion
    if '.firebaseio.com' in site:
        site = site.split('.')[0]
    url = 'https://{}.firebaseio.com/{}.json'.format(site, endpoint)
    if args.auth is not None:
        url += '?auth={}'.format(args.auth)
    read_r = requests.get(url)
    # POST nothing to test write access to avoid overwriting data
    write_r = requests.post(url, data="null", headers={'Content-type': 'application/json'})
    data = read_r.json() if read_r.status_code != 401 else None
    print("Site: " + site + " endpoint: " + endpoint + " data: " + json.dumps(data))
    return read_r.status_code != 401, write_r.status_code != 401, data


# from https://stackoverflow.com/a/7205107/2683545
def merge(a, b, path=None):
        "merges b into a"
        if path is None: path = []
        for key in b:
                if key in a:
                        if isinstance(a[key], dict) and isinstance(b[key], dict):
                                merge(a[key], b[key], path + [str(key)])
                        elif a[key] == b[key]:
                                pass # same leaf value
                        else:
                                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                else:
                        a[key] = b[key]
        return a


def scan_sites(args):
    #Opening files should be surrounded by a try/except in case it fails
    try:
        firebase_sites = args.sites.read().splitlines()
    except:
        print("Opening sites file failed")
        exit(1)
    output = {}
    for site in firebase_sites:
        print("Scanning site {}...".format(site))
        # The user may not specify endpoints. Handle this cleanly if so
        if args.endpoints:
            arg_endpoints = args.endpoints.read().splitlines()
            endpoint_list = common_endpoints + arg_endpoints # If there are endpoints specified, use them!
        else:
            endpoint_list = common_endpoints # Otherwise just use the common endpoint list
        endpoint_info = {}
        db_dump = {}
        for endpoint in endpoint_list:
            dump_path = endpoint.split("/")
            read_success, write_success, data = try_endpoint(args, site, endpoint)
            if data is not None:
                for part in dump_path:
                    if part not in db_dump:
                        db_dump[part] = {}
                    if isinstance(data, dict):
                        db_dump[part] = merge(db_dump[part], data)
                    else:
                        db_dump[part] = data
                    if read_success or write_success:
                        endpoint_info[endpoint] = {"read": read_success, "write": write_success}
        output[site] = {"info": endpoint_info, "dump": db_dump}
    args.out.write(json.dumps(output))
    args.out.close()


def parse_args():
        parser = ArgumentParser()
        parser.add_argument('--sites', help="File containing list of firebase sites to scan [code].firebaseio.com", type=FileType('r'))
        # parser.add_argument('--methods', help="A list of HTTP methods to try", nargs="*", default=firebase_http_methods, choices=fireba
se_http_methods)
        parser.add_argument('--auth', help="An optional auth token to use")
        parser.add_argument('--endpoints', help="A list of known endpoints to check", nargs='?', type=FileType('r'), default=StringIO("")
)
        parser.add_argument('--dirty', help="Should we modify the db to find more writable locations?", action="store_true", default=Fals
e)
        parser.add_argument('--out', help="A file to dump info to", nargs='?', type=FileType('w'), default=sys.stdout)
        args = parser.parse_args()
        scan_sites(args)


if __name__ == '__main__':
        parse_args()
