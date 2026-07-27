from __future__ import annotations

import gzip
import shutil
from pathlib import Path

import pendulum
import requests

from airflow.sdk import dag, task


DATA_DIR = Path("/tmp/wikipedia")
DATA_DIR.mkdir(exist_ok=True)

PAGE = "Google"
LANGUAGE = "en"


@dag(
    dag_id="wikipedia_pageviews",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["book", "wikipedia"],
)
def wikipedia_pageviews():

    @task
    def download(logical_date=None) -> str:
        """
        Download one hourly Wikimedia pageviews file.

        Uses the DAG run's logical date.
        """

        dt = logical_date

        url = (
            "https://dumps.wikimedia.org/other/pageviews/"
            f"{dt.year}/{dt.year}-{dt.month:02d}/"
            f"pageviews-{dt.year}"
            f"{dt.month:02d}"
            f"{dt.day:02d}-"
            f"{dt.hour:02d}0000.gz"
        )

        gz_file = DATA_DIR / "pageviews.gz"

        print(f"Downloading {url}")

        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()

        with open(gz_file, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

        return str(gz_file)

    @task
    def unzip(gz_filename: str) -> str:
        output = DATA_DIR / "pageviews"

        with gzip.open(gz_filename, "rb") as fin:
            with open(output, "wb") as fout:
                shutil.copyfileobj(fin, fout)

        return str(output)

    @task
    def count_views(filename: str) -> int:

        with open(filename, encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.split()

                if len(parts) < 4:
                    continue

                domain, page, views, _ = parts

                if domain == LANGUAGE and page == PAGE:
                    print(f"{PAGE}: {views} views")
                    return int(views)

        print(f"{PAGE} not found.")
        return 0

    gz = download()
    txt = unzip(gz)
    count_views(txt)


wikipedia_pageviews()