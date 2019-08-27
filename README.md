# Firebase-scanner

This project contains various tools used for automated scanning and vulnerability discovery in firebase apps.


# Components

- `db-discovery.py` - This tool will aggregate various services (DNSDumpster, Shodan) to attempt to discover random firebase project codes.
- `endpoint-discovery.py` - Run this tool on a wireshark .pcap or binary file to extract potential firebase db endpoints.
- `scanner.py` - This tool will see what data and endpoints in the realtime DB are accessible (read/write info) and dump that information. It can also optionally dump everything that it can read. You can optionally give it an auth token and a list of endpoints (from endpt discovery script) to help it find more data.
