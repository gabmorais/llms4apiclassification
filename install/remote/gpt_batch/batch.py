import json
import os

import pandas as pd


def batch_decode(directory_in, directory_out):
    for file in os.listdir(directory_in):
        results = []
        with open(os.path.join(directory_in, file), "r", encoding="utf-8") as f:
            for line in f:
                json_data = json.loads(line.strip())
                results.append((json_data["custom_id"], json_data["response"]["body"]["choices"][0]["message"]["content"]))
        df = pd.DataFrame.from_records(results, columns=["filename", "gpt-4o-mini"])
        df = df.sort_values("filename")
        df.iloc[:, -1].to_csv(f"{directory_out}/{file.split('.')[0]}.csv", index=False, sep=";")


if __name__ == "__main__":
    # Decode batch
    batch_decode("batch", "result")
