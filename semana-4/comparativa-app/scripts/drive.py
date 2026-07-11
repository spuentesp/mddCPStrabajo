#!/usr/bin/env python3
import sys, json, urllib.request

def transform(input_xml_path, xsl_path):
    with open(input_xml_path, encoding="utf-8") as f:
        xml = f.read()
    with open(xsl_path, encoding="utf-8") as f:
        xsl = f.read()
    payload = json.dumps({"inputXML": xml, "xslTransformation": xsl}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:3000/transform",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode("utf-8")

if __name__ == "__main__":
    inp, xsl, out = sys.argv[1], sys.argv[2], sys.argv[3]
    status, body = transform(inp, xsl)
    print("HTTP", status, "-> bytes:", len(body))
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    # quick sanity peek
    print(body[:600])
