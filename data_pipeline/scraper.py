#!/usr/bin/env python3
"""
Download all PDF from Digital庁 ガイドラインページ
Trace each step on Langfuse
"""

import re, time, requests, pathlib
from bs4 import BeautifulSoup
from langfuse import Langfuse
from urllib.parse import urljoin
from config import BASE_URL, RAW_DIR, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST

lf = Langfuse(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST
)

def collect_pdf_urls() -> list[str]:
    resp = requests.get(BASE_URL, timeout=20)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [
        a["href"] for a in soup.select("a[href$='.pdf']")
        if "guideline" in a["href"]
    ]
    # Convert relative URLs to absolute
    unique = sorted(set(links))
    return [urljoin(BASE_URL, href) for href in unique]

def download(url: str) -> pathlib.Path:
    fname = RAW_DIR / pathlib.Path(url).name
    if fname.exists():
        return fname
    r = requests.get(url, stream=True, timeout=60)
    with open(fname, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return fname

def main():
    urls = collect_pdf_urls()
    # If Langfuse tracing is available, record spans; otherwise proceed without tracing
    if hasattr(lf, 'trace'):
        with lf.trace(name="scraper") as trace:
            for u in urls:
                with trace.span(name="download", input=u) as span:
                    try:
                        path = download(u)
                        span.output = str(path)
                    except Exception as e:
                        span.error = str(e)
    else:
        for u in urls:
            try:
                path = download(u)
                print(f"Downloaded: {path}")
            except Exception as e:
                print(f"Error downloading {u}: {e}")

if __name__ == "__main__":
    main()
