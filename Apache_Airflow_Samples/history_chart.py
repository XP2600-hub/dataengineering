from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = Path("/tmp/wikipedia")


def create_history_chart():
    csv_files = sorted(OUTPUT_DIR.glob("pageviews-*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found.")

    history = []

    for csv_file in csv_files:
        timestamp = csv_file.stem.replace("pageviews-", "")

        df = pd.read_csv(csv_file)

        row = {
            "Timestamp": pd.to_datetime(
                timestamp,
                format="%Y%m%d-%H%M%S",
            )
        }

        for _, record in df.iterrows():
            row[record["Provider"]] = record["Views"]

        history.append(row)

    history_df = (
        pd.DataFrame(history)
        .fillna(0)
        .sort_values("Timestamp")
    )

    plt.figure(figsize=(12, 6))

    for provider in ["AWS", "Azure", "GCP"]:
        plt.plot(
            history_df["Timestamp"],
            history_df[provider],
            marker="o",
            linewidth=2,
            label=provider,
        )

    plt.title("Wikipedia Cloud Provider Page Views")
    plt.xlabel("Timestamp")
    plt.ylabel("Views")
    plt.grid(True)
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    output = OUTPUT_DIR / "history.png"

    plt.savefig(output, dpi=150)
    plt.close()

    print(f"History chart written to {output}")

    return str(output)