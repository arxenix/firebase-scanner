from argparse import ArgumentParser, FileType
import re
import sys


def search_pcap(args):
    import pyshark
    fname = args.file.name
    args.file.close()
    cap = pyshark.FileCapture(input_file=fname, display_filter="http.request.uri contains \"/firebaseio/\"")

    endpoints = []
    for packet in cap:
        uri = packet.http.request.uri
        pattern = re.compile("https?://(.+)\\.firebaseio\\.com/(.*)")
        match = pattern.match(uri)
        path = match.group(2)
        endpoints.append(path)
    return endpoints


def search_binary_exact(args):
    binary = args.file.read()
    pattern = re.compile("https?://(.+)\\.firebaseio\\.com/(.*)")
    matches = pattern.findall(binary)
    endpoints = [match.group(2) for match in matches]
    return endpoints


def search_binary_strings(args):
    binary = args.file.read()
    pattern = re.compile("\\w{5,}")  # find all text with len >= 5
    matches = pattern.findall(binary)
    endpoints = [match.group(0) for match in matches]
    return endpoints


def discover_endpoints(args):
    endpoints = []
    if args.type == 'pcap':
        endpoints = search_pcap(args)
    elif args.type == 'binary_exact':
        endpoints = search_binary_exact(args)
    elif args.type == 'binary_strings':
        endpoints = search_binary_strings(args)

    cleaned_endpoints = []
    for endpoint in endpoints:
        if endpoint.startswith("/"):
            endpoint = endpoints[1:]
        if endpoint.endswith(".json"):
            endpoint = endpoints[:-5]
        cleaned_endpoints.append(endpoint)

    endpoints = cleaned_endpoints
    print("{} potential endpoints found.".format(len(endpoints)))
    data = "\n".join(endpoints) + "\n"
    args.out.write(data)
    args.out.close()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('type', help="Look for potential endpoints in the specified file type", choices=["pcap", "binary_exact", "binary_strings"])
    parser.add_argument('file', help="The file to search through", type=FileType('w'))
    parser.add_argument('--out', help="A file to dump results to", nargs='?', type=FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    discover_endpoints(args)


if __name__ == '__main__':
    parse_args()