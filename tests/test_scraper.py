import zipfile
from pathlib import Path

import pytest

from data_pipeline.scraper import download_file, download_pdfs, download_zips


@pytest.fixture
def sample_files(tmp_path):
    pdf = tmp_path / "sample.pdf"
    pdf.write_text("%PDF-1.4\nDummy PDF file")

    zipf = tmp_path / "sample.zip"
    with zipfile.ZipFile(zipf, "w") as zf:
        zf.writestr("inside.txt", "hello")

    return pdf, zipf


def test_download_file_pdf(tmp_path, sample_files):
    pdf, _ = sample_files
    out_dir = tmp_path / "out"
    path = download_file(str(pdf), out_dir)
    assert path.exists()
    assert path.read_bytes() == pdf.read_bytes()


def test_download_file_zip(tmp_path, sample_files):
    _, zipf = sample_files
    out_dir = tmp_path / "out"
    path = download_file(str(zipf), out_dir)
    assert path.exists()
    assert path.read_bytes() == zipf.read_bytes()


def test_download_pdfs(tmp_path, sample_files):
    pdf, _ = sample_files
    out_dir = tmp_path / "out"
    paths = download_pdfs([str(pdf)], out_dir)
    assert len(paths) == 1
    assert paths[0].exists()


def test_download_zips(tmp_path, sample_files):
    _, zipf = sample_files
    out_dir = tmp_path / "out"
    paths = download_zips([str(zipf)], out_dir)
    assert len(paths) == 1
    assert zipfile.is_zipfile(paths[0])
