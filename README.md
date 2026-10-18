\# Project 7: Python Network Checker



A small Python tool that checks configured TCP ports on lab hosts.



\## What it does



\- Reads hosts, ports, and expected states from `targets.json`.

\- Uses a configurable connection timeout.

\- Reports each result as `PASS`, `FAIL`, or `ERROR`.

\- Saves JSON and CSV reports.

\- Returns exit code `0` when every check passes, `1` when a check fails or errors, and `2` for invalid configuration or report-writing problems.



The tool uses only Python’s standard library.



\## Result meanings



\- \*\*Open:\*\* A TCP connection succeeded.

\- \*\*Closed:\*\* The connection was refused.

\- \*\*Error:\*\* A timeout or another network problem prevented a clear result. A timeout does not prove a port is closed; a firewall may be dropping traffic.



Network behavior can differ between computers because their routes and firewalls may differ.



\## Run it



Linux: `python3 checker.py`



Windows: `python checker.py`



Run it only against lab hosts and ports you’re authorized to check.

