# Firebase-scanner

This project contains various tools used for automated scanning and vulnerability discovery in firebase apps.


# Components

- `db-discovery.py` - This tool will aggregate various services (DNSDumpster) to attempt to discover random firebase DBs.
- `endpoint-discovery.py` - Run this tool on a wireshark .pcap or binary file to extract potential firebase DB endpoints.
- `scanner.py` - This tool will see what data and endpoints in the realtime DB are accessible (read/write info) and dump that information. It can also optionally dump everything that it can read. You can optionally give it an auth token and a list of endpoints (from endpt discovery script) to help it find more data.


# Sample usage - mass project scan
1. Acquire a list of firebase DB project codes: [code].firebaseio.com. A good way to do this is to use [Sublist3r](https://github.com/aboul3la/Sublist3r) on the domain firebaseio.com. Running `db-discovery.py` should also work, but it is not as advanced as Sublist3r.
2. Run `scanner.py [codes file]` to scan r/w info about this project and dump any available data

# Sample usage - single target
1. Create a file containing the name of the target firebase project (code.txt)
2. Acquire a file in which accesses to this firebase DB are made. Examples are: pcap of traffic from app interacting with this firebase db, code which accesses this firebase db (executable, JS file, APK, etc.). Run `endpoint-discovery.py [file] --out endpoints.txt` script on this file to gather a list of potential endpoint candidates.
3. Run `scanner.py code.txt --endpoints endpoints.txt` to scan r/w info about this project and dump any available data


If you have an auth token for the firebase project you are scanning, you can use it with `scanner.py code.txt --endpoints endpoints.txt --token [token]`
