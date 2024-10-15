import os
import pathlib
import platform
import platformdirs
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

"""
import pathlib, py_pg_embed

data_dir = pathlib.Path("data")
pg = py_pg_embed.get_pg_dir("17.0.0")
py_pg_embed.initdb(pg, data_dir)
py_pg_embed.postgres(pg,data_dir)

...

$ psql -h localhost postgres
"""


def get_url(version, os, arch_1):
    return f"https://repo1.maven.org/maven2/io/zonky/test/postgres/embedded-postgres-binaries-{os}-{arch_1}/{version}/embedded-postgres-binaries-{os}-{arch_1}-{version}.jar"


def _download(url, path: pathlib.Path):
    with path.open("wb") as out:
        with urllib.request.urlopen(url) as in_:
            shutil.copyfileobj(in_, out)


def extract(package, path: pathlib.Path, os, arch_2):
    with zipfile.ZipFile(package) as zip:
        with zip.open(f"postgres-{os}-{arch_2}.txz") as txz:
            with tarfile.open(mode="r:xz", fileobj=txz) as tar:
                tar.extractall(path)


def initdb(extracted: pathlib.Path, data_dir: pathlib.Path):
    subprocess.run([extracted / "bin" / "initdb", "-D", data_dir], check=True)


def postgres(extracted: pathlib.Path, data_dir: pathlib.Path):
    subprocess.run([extracted / "bin" / "postgres", "-D", data_dir], check=True)


def get_pg_dir(version, os=None, arch_1=None, arch_2=None):
    if not os:
        os = platform.system().lower()
    if not arch_1:
        arch_1 = {"x86_64": "amd64"}[platform.machine()]
    if not arch_2:
        arch_2 = platform.machine()

    cache_dir = pathlib.Path(platformdirs.user_cache_dir("pypgembed", "pdp7"))
    cache_dir.mkdir(parents=True, exist_ok=True)

    id = f"{os}-{arch_2}-{version}"

    pg_dir = cache_dir / f"{id}"

    if pg_dir.exists():
        return pg_dir

    archive = cache_dir / f"{id}.jar"

    if not archive.exists():
        _download(get_url(version, os, arch_1), archive)

    extract(archive, pg_dir, os, arch_2)

    return pg_dir


def run_with_dj_database_url():
    assert len(sys.argv) > 3, "arguments VERSION DATA_DIR PROGRAM ARG1 ARG2..."

    version = sys.argv[1]
    data_dir = pathlib.Path(sys.argv[2])
    command = sys.argv[3:]

    pg_dir = get_pg_dir(version)

    if not data_dir.exists():
        initdb(pg_dir, data_dir)

    with subprocess.Popen([pg_dir / "bin" / "postgres", "-D", data_dir]) as pg_proc:
        os.environ["DATABASE_URL"] = "postgresql://localhost/postgres"
        subprocess.run(command, check=True)
        pg_proc.terminate()
