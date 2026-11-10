"""
Automated Uptime and Health Monitoring Daemon for EduTask
Performs synthetic HTTP health checks, measures latency, records logs, and calculates availability.
Usage:
  python scripts/uptime_monitor.py --single-run
  python scripts/uptime_monitor.py --url http://localhost:8000/api/health --interval 10
"""

import sys
import time
import json
import os
import argparse
from datetime import datetime
import urllib.request
import urllib.error


def ping_health_endpoint(url: str, timeout: int = 5):
    """Perform HTTP GET request to /api/health and measure latency"""
    start_time = time.time()
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "EduTask-Uptime-Monitor/1.1", "Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            status_code = response.getcode()
            body = response.read().decode("utf-8")
            data = json.loads(body)
            return {
                "success": status_code == 200 and data.get("status") == "UP",
                "status_code": status_code,
                "latency_ms": latency_ms,
                "data": data,
                "error": None
            }
    except urllib.error.HTTPError as he:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "success": False,
            "status_code": he.code,
            "latency_ms": latency_ms,
            "data": None,
            "error": f"HTTP Error {he.code}: {he.reason}"
        }
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "success": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "data": None,
            "error": str(e)
        }


def record_log(log_entry: dict, log_file: str):
    """Write structured JSON log line to audit file"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    parser = argparse.ArgumentParser(description="EduTask Uptime and Health Monitor")
    parser.add_argument("--url", default="http://localhost:8000/api/health", help="Target healthcheck URL")
    parser.add_argument("--interval", type=int, default=10, help="Poll interval in seconds")
    parser.add_argument("--log-file", default="logs/uptime_audit.log", help="Path to audit log file")
    parser.add_argument("--single-run", action="store_true", help="Execute single probe and exit")
    parser.add_argument("--count", type=int, default=0, help="Number of probes (0 for infinite)")

    args = parser.parse_args()

    print(f"============================================================")
    print(f"  EduTask DevOps Health & Uptime Monitoring Daemon")
    print(f"  Target URL: {args.url}")
    print(f"  Audit Log:  {args.log_file}")
    print(f"  Timestamp:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"============================================================")

    total_probes = 0
    successful_probes = 0
    total_latency = 0.0

    try:
        while True:
            total_probes += 1
            result = ping_health_endpoint(args.url)
            timestamp = datetime.now().isoformat()

            log_entry = {
                "timestamp": timestamp,
                "url": args.url,
                "success": result["success"],
                "status_code": result["status_code"],
                "latency_ms": result["latency_ms"],
                "error": result["error"]
            }

            if result["success"]:
                successful_probes += 1
                total_latency += result["latency_ms"]
                uptime_data = result["data"]
                print(
                    f"[{timestamp}] [STATUS: UP] Code={result['status_code']} "
                    f"Latency={result['latency_ms']}ms | Service={uptime_data.get('service')} "
                    f"| Ver={uptime_data.get('version')} | Uptime={uptime_data.get('uptime_seconds')}s"
                )
            else:
                print(
                    f"[{timestamp}] [STATUS: DOWN/FAIL] Code={result['status_code']} "
                    f"Latency={result['latency_ms']}ms | Error={result['error']}"
                )

            record_log(log_entry, args.log_file)

            if args.single_run or (args.count > 0 and total_probes >= args.count):
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

    # Summary
    if total_probes > 0:
        availability = (successful_probes / total_probes) * 100.0
        avg_latency = round(total_latency / successful_probes, 2) if successful_probes > 0 else 0.0
        print("\n---------------- MONITORING SUMMARY ----------------")
        print(f"Total Probes:       {total_probes}")
        print(f"Successful Pings:   {successful_probes}")
        print(f"Failed Pings:       {total_probes - successful_probes}")
        print(f"Service Uptime:     {availability:.2f}%")
        print(f"Average Latency:    {avg_latency} ms")
        print(f"Log written to:     {os.path.abspath(args.log_file)}")
        print("----------------------------------------------------\n")


if __name__ == "__main__":
    main()
