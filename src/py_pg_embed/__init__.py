import pathlib
import shutil
import urllib.request


def get_url(os="linux", arch="amd64", version="16.3.0"):
    return f"https://repo1.maven.org/maven2/io/zonky/test/postgres/embedded-postgres-binaries-{os}-{arch}/{version}/embedded-postgres-binaries-{os}-{arch}-{version}.jar"


def _download(url, path: pathlib.Path):
    with path.open("wb") as out:
        with urllib.request.urlopen(url) as in_:
            shutil.copyfileobj(in_, out)
