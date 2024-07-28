import pathlib
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile

"""
import pathlib, py_pg_embed

jar = pathlib.Path("tmp.jar")
pg = pathlib.Path("pg")
data = pathlib.Path("data")

py_pg_embed._download(py_pg_embed.get_url(), jar)
py_pg_embed.extract(jar, pg)
py_pg_embed.initdb(pg, data)
py_pg_embed.postgres(pg,data)

...

$ psql -h localhost postgres
"""


def get_url(os="linux", arch="amd64", version="16.3.0"):
    return f"https://repo1.maven.org/maven2/io/zonky/test/postgres/embedded-postgres-binaries-{os}-{arch}/{version}/embedded-postgres-binaries-{os}-{arch}-{version}.jar"


def _download(url, path: pathlib.Path):
    with path.open("wb") as out:
        with urllib.request.urlopen(url) as in_:
            shutil.copyfileobj(in_, out)


def extract(package, path: pathlib.Path, os="linux", arch="x86_64"):
    with zipfile.ZipFile(package) as zip:
        with zip.open(f"postgres-{os}-{arch}.txz") as txz:
            with tarfile.open(mode="r:xz", fileobj=txz) as tar:
                tar.extractall(path)


def initdb(extracted: pathlib.Path, datadir: pathlib.Path):
    subprocess.run([extracted / "bin" / "initdb", "-D", datadir], check=True)


def postgres(extracted: pathlib.Path, datadir: pathlib.Path):
    subprocess.run([extracted / "bin" / "postgres", "-D", datadir], check=True)
