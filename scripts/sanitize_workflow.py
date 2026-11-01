"""Removes API keys / tokens from an exported n8n workflow JSON.
Usage: python3 sanitize_workflow.py exported.json clean.json
"""
import re, sys, json

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()

patterns = [
    (r"Bearer\s+[A-Za-z0-9._\-]{12,}", "Bearer YOUR_HUBSPOT_TOKEN"),
    (r"pat-[a-z0-9]+-[0-9a-f\-]{20,}", "YOUR_HUBSPOT_TOKEN"),
    (r"gsk_[A-Za-z0-9]{20,}", "YOUR_API_KEY"),
    (r"sk-[A-Za-z0-9_\-]{20,}", "YOUR_API_KEY"),
    (r"AIza[0-9A-Za-z_\-]{30,}", "YOUR_API_KEY"),
]
for pat, rep in patterns:
    text = re.sub(pat, rep, text)

json.loads(text)  # make sure it is still valid JSON
open(dst, "w", encoding="utf-8").write(text)

left = re.findall(r"(pat-[a-z0-9]+-|gsk_|AIza|sk-[A-Za-z0-9])", text)
print("Saved", dst, "| possible leftovers:", len(left))
