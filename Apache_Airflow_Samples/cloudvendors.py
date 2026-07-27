import csv
import gzip
import shutil
from pathlib import Path

import pendulum
import requests

from airflow.sdk import dag, task, get_current_context

OUTPUT_DIR = Path("/tmp/wikipedia")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "airflow-tutorial/1.0 (example@example.com)"

PAGES = {
    "Amazon_Web_Services": "AWS",
    "Microsoft_Azure": "Azure",
    "Google_Cloud_Platform": "GCP",
}


@dag(
    dag_id="wikipedia_cloudvendors",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["tutorial"],
)
def wikipedia_pageviews():

    @task(retries=3)
    def download():

        context = get_current_context()
        logical_date = context["logical_date"]

        year = logical_date.strftime("%Y")
        month = logical_date.strftime("%Y-%m")
        timestamp = logical_date.strftime("%Y%m%d") + "-000000"

        url = (
            f"https://dumps.wikimedia.org/other/pageviews/"
            f"{year}/{month}/pageviews-{timestamp}.gz"
        )

        outfile = OUTPUT_DIR / f"pageviews-{timestamp}.gz"

        if outfile.exists():
            print(f"{outfile} already exists. Skipping download.")
            return str(outfile)

        print(f"Downloading {url}")

        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=120,
            stream=True,
        )

        response.raise_for_status()

        with open(outfile, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print(f"Saved {outfile}")

        return str(outfile)

    @task
    def unzip(gz_file):

        txt_file = Path(gz_file).with_suffix("")

        if txt_file.exists():
            print(f"{txt_file} already exists. Skipping extraction.")
            return str(txt_file)

        with gzip.open(gz_file, "rb") as src:
            with open(txt_file, "wb") as dst:
                shutil.copyfileobj(src, dst)

        print(f"Extracted {txt_file}")

        return str(txt_file)

    @task
    def count_views(txt_file):

        results = {
            "AWS": 0,
            "Azure": 0,
            "GCP": 0,
        }

        with open(txt_file, encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) < 3:
                    continue

                project = parts[0]
                page = parts[1]

                if project != "en":
                    continue

                if page not in PAGES:
                    continue

                try:
                    views = int(parts[2])
                except ValueError:
                    continue

                results[PAGES[page]] = views

        timestamp = Path(txt_file).stem
        csv_file = OUTPUT_DIR / f"{timestamp}.csv"

        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Provider", "Views"])

            for provider, views in results.items():
                writer.writerow([provider, views])

        print("\nCloud Provider Page Views\n")

        for provider, views in results.items():
            print(f"{provider:8}: {views:,}")

        print(f"\nCSV written to {csv_file}")

        return str(csv_file)

    csv_result = count_views(unzip(download()))


wikipedia_pageviews()