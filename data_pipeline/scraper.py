from __future__ import annotations

import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests


def download_file(url: str, output_dir: Path) -> Path:
    """Download a single file from ``url`` into ``output_dir``.

    ``url`` can be an ``http``/``https`` URL or a local filesystem path.
    ``output_dir`` is created if it does not exist.
    Returns the path to the downloaded file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    parsed = urlparse(url)
    filename = Path(parsed.path).name
    dest_path = output_dir / filename

    if parsed.scheme in ("http", "https"):
        with requests.get(url, stream=True) as resp:
            resp.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    else:
        src_path = Path(url)
        if not src_path.exists():
            raise FileNotFoundError(src_path)
        shutil.copyfile(src_path, dest_path)

    return dest_path


def download_pdfs(urls: list[str], output_dir: Path) -> list[Path]:
    """Download multiple PDF files from ``urls`` into ``output_dir``."""
    return [download_file(url, output_dir) for url in urls]


def download_zips(urls: list[str], output_dir: Path) -> list[Path]:
    """Download multiple ZIP files from ``urls`` into ``output_dir``."""
    return [download_file(url, output_dir) for url in urls]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download PDF/ZIP files")
    parser.add_argument("urls", nargs="+", help="URLs or local paths to download")
    parser.add_argument("--out", default="data/raw", help="Destination directory")
    args = parser.parse_args()

    download_files = [download_file(url, Path(args.out)) for url in args.urls]
    for path in download_files:
        print(f"Downloaded {path}")
