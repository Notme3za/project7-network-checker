import csv
import json
import socket


def check_port(host, port, timeout):
    """Check a TCP port and return its observed state and explanation."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "open", "connection succeeded"
    except ConnectionRefusedError:
        return "closed", "connection was refused"
    except TimeoutError:
        return "error", "connection timed out"
    except OSError as error:
        return "error", str(error)


def main():
    try:
        with open("targets.json", encoding="utf-8") as file:
            config = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read targets.json: {error}")
        return 2

    if not isinstance(config, dict):
        print("Invalid config: the top level must be an object.")
        return 2

    targets = config.get("targets")
    if not isinstance(targets, list) or not targets:
        print("Invalid config: 'targets' must be a non-empty list.")
        return 2

    timeout = config.get("timeout", 2)
    if (
        not isinstance(timeout, (int, float))
        or isinstance(timeout, bool)
        or not 0.1 <= timeout <= 10
    ):
        print("Invalid config: timeout must be between 0.1 and 10 seconds.")
        return 2

    json_report = config.get("json_report", "report.json")
    csv_report = config.get("csv_report", "report.csv")
    if not isinstance(json_report, str) or not json_report.strip():
        print("Invalid config: 'json_report' must be a filename.")
        return 2
    if not isinstance(csv_report, str) or not csv_report.strip():
        print("Invalid config: 'csv_report' must be a filename.")
        return 2

    results = []

    for number, target in enumerate(targets, start=1):
        if not isinstance(target, dict):
            print(f"Invalid config: target {number} must be an object.")
            return 2

        host = target.get("host")
        port = target.get("port")
        expected = target.get("expected")

        if not isinstance(host, str) or not host.strip():
            print(f"Invalid config: target {number} needs a host.")
            return 2
        if (
            not isinstance(port, int)
            or isinstance(port, bool)
            or not 1 <= port <= 65535
        ):
            print(f"Invalid config: target {number} needs a port from 1 to 65535.")
            return 2
        if expected not in ("open", "closed"):
            print(f"Invalid config: target {number} expected must be open or closed.")
            return 2

        actual, detail = check_port(host, port, timeout)
        result = "ERROR" if actual == "error" else (
            "PASS" if actual == expected else "FAIL"
        )

        row = {
            "host": host,
            "port": port,
            "expected": expected,
            "actual": actual,
            "result": result,
            "detail": detail,
        }
        results.append(row)
        print(
            f"{result}: {host}:{port} expected={expected}, "
            f"actual={actual} ({detail})"
        )

    passed = sum(row["result"] == "PASS" for row in results)
    failed = sum(row["result"] == "FAIL" for row in results)
    errors = sum(row["result"] == "ERROR" for row in results)
    print(f"Summary: {passed} passed, {failed} failed, {errors} errors")

    columns = ["host", "port", "expected", "actual", "result", "detail"]
    try:
        with open(json_report, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2)

        with open(csv_report, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(results)
    except OSError as error:
        print(f"Could not save a report: {error}")
        return 2

    print(f"Saved reports: {json_report} and {csv_report}")

    if failed or errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
