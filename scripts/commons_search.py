#!/usr/bin/env python3
"""Search Wikimedia Commons files (licence, size, thumbnail), ≥ 2 s between requests."""
import json, sys, time, urllib.parse, urllib.request
UA = "punctured-sky/0.1 (research; github.com/maribakulj/punctured-sky)"
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    time.sleep(2)
    return json.load(urllib.request.urlopen(req, timeout=60))
def search(q, n=12):
    r = api({"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {q}", "gsrnamespace": 6,
             "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 400})
    out = []
    for p in (r.get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
        out.append({"title": p["title"], "w": ii["width"], "h": ii["height"], "thumb": ii.get("thumburl"),
                    "url": ii["url"], "license": md.get("LicenseShortName", {}).get("value"),
                    "artist": md.get("Artist", {}).get("value", "")[:80]})
    return out
if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("##", q)
        for x in search(q): print(json.dumps(x, ensure_ascii=False))
