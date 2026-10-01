"""
Corrigan Peak - Dispatch Exception Triage
Normalise FreightWorks exception records (terminal, carrier code, timestamp),
summarise counts by event type, and flag records that could not be cleaned
with confidence. Prepared for Ajaia (https://ajaia.ai).

Usage:  python clean_exceptions.py exceptions_raw.csv
Output: exceptions_clean.csv, exceptions_flagged.csv, summary printed to screen
"""
import csv, re, sys
from collections import Counter
from datetime import datetime

# Known terminal aliases -> canonical name. Unknown values are flagged, not guessed.
TERMINAL_ALIASES = {"terminal 1": "Terminal 1", "t1": "Terminal 1",
                    "terminal 2": "Terminal 2", "t2": "Terminal 2",
                    "terminal 3": "Terminal 3", "t3": "Terminal 3"}

# Accepted timestamp formats. Anything else is flagged.
TS_FORMATS = [("%Y-%m-%d %H:%M:%S", False),   # 2026-08-14 09:12:00 (no timezone)
              ("%m/%d/%Y %H:%M", False),      # 08/14/2026 09:45  (no timezone, no seconds)
              ("%Y-%m-%dT%H:%M:%SZ", True)]   # 2026-08-14T10:03:00Z (explicit UTC)

def norm_terminal(v):
    return TERMINAL_ALIASES.get((v or "").strip().lower())

def norm_carrier(v):
    v = (v or "").strip().upper()
    return v if re.fullmatch(r"[A-Z]{2,4}", v) else None   # SCAC-style codes are 2-4 letters

def norm_ts(v):
    v = (v or "").strip()
    for fmt, is_utc in TS_FORMATS:
        try:
            return datetime.strptime(v, fmt).strftime("%Y-%m-%d %H:%M:%S"), is_utc
        except ValueError:
            continue
    return None, None

def clean(rows):
    clean_rows, flagged = [], []
    for r in rows:
        issues = []
        term = norm_terminal(r["terminal"])
        carrier = norm_carrier(r["carrier_code"])
        ts, is_utc = norm_ts(r["event_ts"])
        if term is None:
            issues.append(f"unknown terminal '{r['terminal']}'")
        if carrier is None:
            issues.append("missing carrier code" if not r["carrier_code"].strip()
                          else f"invalid carrier code '{r['carrier_code']}'")
        if ts is None:
            issues.append(f"unparseable timestamp '{r['event_ts']}'")
        elif is_utc:
            # Other rows carry no timezone, so we cannot safely compare or convert this one.
            issues.append("timestamp is UTC ('Z') while others have no timezone; "
                          "kept as written, needs FreightWorks to confirm source timezone")
        out = {"exception_id": r["exception_id"].strip(),
               "terminal": term or r["terminal"],
               "event_type": r["event_type"].strip().lower(),
               "carrier_code": carrier or "",
               "event_ts": ts or r["event_ts"],
               "ts_timezone": "UTC" if is_utc else "unspecified",
               "confident": "no" if issues else "yes",
               "issues": "; ".join(issues)}
        clean_rows.append(out)
        if issues:
            flagged.append(out)
    return clean_rows, flagged

def main(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    clean_rows, flagged = clean(rows)
    fields = list(clean_rows[0].keys())
    for name, data in [("exceptions_clean.csv", clean_rows), ("exceptions_flagged.csv", flagged)]:
        with open(name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(data)

    counts = Counter(r["event_type"] for r in clean_rows)
    print(f"Records in: {len(rows)}   Cleaned: {len(clean_rows)}   Flagged: {len(flagged)}\n")
    print("Exceptions by event type")
    for k, v in counts.most_common():
        print(f"  {k:<22}{v}")
    print(f"  {'TOTAL':<22}{sum(counts.values())}\n")
    print("Records not confidently cleaned")
    for r in flagged:
        print(f"  {r['exception_id']}: {r['issues']}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "exceptions_raw.csv")
