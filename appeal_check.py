#!/usr/bin/env python3
"""Criterion 4 (appeals) and the sixth criterion-5 case, which run_eval.py can't express."""
import json, sys, requests
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"
TEXTS = [
    "Went for a run. Legs hurt. Worth it.",
    "The landlord finally fixed the heater, but it clanks at 4am like someone is trapped inside.",
    "We lost 3-2 on Saturday. Dani's own goal, ninety-first minute. Bought everyone chips afterward.",
    "Honestly I almost missed the bus again today. Ran the last block with my bag banging into my hip.",
    "My grandmother kept her good scissors in a biscuit tin, and God help you if you used them on paper.",
]
def log():
    return requests.get(f"{URL}/log", timeout=30).json()
def entries(cid):
    d = log(); d = d.get("entries", d) if isinstance(d, dict) else d
    return [e for e in d if e.get("content_id") == cid]
ok = 0
for i, t in enumerate(TEXTS):
    cid = requests.post(f"{URL}/submit", json={"text": t, "creator_id": f"appeal_{i}"}, timeout=120).json()["content_id"]
    before = [e for e in entries(cid) if "event" not in e]
    r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": "I wrote this myself."}, timeout=30)
    after = entries(cid)
    appeals = [e for e in after if e.get("event") == "appeal"]
    decision_same = [e for e in after if "event" not in e] == before
    good = r.status_code == 200 and r.json().get("status") == "under_review" and len(appeals) == 1 and decision_same
    ok += good
    print(i, r.status_code, r.json().get("status"), "appeal entries:", len(appeals), "decision unchanged:", decision_same, "->", "PASS" if good else "FAIL")
n0 = len([e for e in (log().get("entries", log()) if isinstance(log(), dict) else log()) if e.get("event") == "appeal"])
r = requests.post(f"{URL}/appeal", json={"content_id": "not-a-real-id", "reasoning": "x"}, timeout=30)
n1 = len([e for e in (log().get("entries", log()) if isinstance(log(), dict) else log()) if e.get("event") == "appeal"])
good = r.status_code == 404 and n0 == n1
ok += good
print("unknown id", r.status_code, "appeal entries added:", n1 - n0, "->", "PASS" if good else "FAIL")
print(f"criterion 4: {ok}/6")
r = requests.post(f"{URL}/submit", data=json.dumps([{"text": "hello"}]), headers={"Content-Type": "application/json"}, timeout=30)
print("JSON list body:", r.status_code, r.text.strip()[:120].replace("\n", " "))
print("/ping afterwards:", requests.post(f"{URL}/ping", json={"message": "hi"}, timeout=10).status_code)
