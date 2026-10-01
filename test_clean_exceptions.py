"""Checks that the cleaner produces the RIGHT output, not just that it runs."""
from clean_exceptions import clean, norm_terminal, norm_carrier, norm_ts
import csv

rows = list(csv.DictReader(open("exceptions_raw.csv")))
out, flagged = clean(rows)
by_id = {r["exception_id"]: r for r in out}

assert len(out) == len(rows) == 5, "no record may be dropped"
assert all(r["terminal"] == "Terminal 3" for r in out), "T3 alias must map to Terminal 3"
assert {by_id[i]["carrier_code"] for i in ["CPX-88213","CPX-88214","CPX-88215"]} == {"SWFT"}, "swft/SWFT/Swft -> SWFT"
assert by_id["CPX-88214"]["event_ts"] == "2026-08-14 09:45:00"
assert by_id["CPX-88217"]["event_ts"] == "2026-08-15 08:02:00"
assert by_id["CPX-88216"]["confident"] == "no" and "missing carrier" in by_id["CPX-88216"]["issues"]
assert by_id["CPX-88215"]["confident"] == "no" and "UTC" in by_id["CPX-88215"]["issues"]
assert sorted(r["exception_id"] for r in flagged) == ["CPX-88215", "CPX-88216"]
# Edge cases: unknown values are flagged, never guessed
assert norm_terminal("Terminal 9") is None
assert norm_carrier("SW1FT") is None
assert norm_ts("14/08/2026 09:45") == (None, None)
print("All 11 checks passed.")
