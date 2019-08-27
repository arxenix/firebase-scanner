import sys

import requests
from argparse import ArgumentParser, FileType
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI


def dnsdumpster():
    results = DNSDumpsterAPI().search('firebaseio.com')
    return [domain['domain'] for domain in results['dns_records']['host']]


def is_firebase_project(code: str) -> bool:
    r = requests.get("https://{}.firebaseio.com".format(code))
    return r.status_code != 404


def has_realtime_db(code: str) -> bool:
    r = requests.options("https://{}.firebaseio.com/.json".format(code))
    return r.status_code != 423


def discover_dbs(args):
    db_candidates = []
    if args.type == "dnsdumpster":
        db_candidates = dnsdumpster()

    print("Discovered DBs:")
    for candidate in db_candidates:
        if is_firebase_project(candidate) and has_realtime_db(candidate):
            args.out.write(candidate + "\n")
            if args.out != sys.stdout:
                print(candidate)



def parse_args():
    parser = ArgumentParser()
    parser.add_argument('type', help="Look for potential dbs through this specified method", choices=["dnsdumpster"])
    parser.add_argument('--out', help="A file to dump results to", nargs='?', type=FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    discover_dbs(args)




if __name__ == '__main__':
    parse_args()