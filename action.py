#!/usr/bin/env python
import os
import tempfile
import pandas as pd
from pathlib import Path
from pyedm.gg import get_xlsx


GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
WATER_LOGSHEET_URL = os.getenv("WATER_LOGSHEET_URL")
SEDIMENT_LOGSHEET_URL = os.getenv("SEDIMENT_LOGSHEET_URL")
ARMS_LOGSHEET_URL = os.getenv("ARMS_LOGSHEET_URL")


if __name__ == "__main__":
    for habitat, url in {"water": WATER_LOGSHEET_URL, "sediment": SEDIMENT_LOGSHEET_URL, "arms": ARMS_LOGSHEET_URL}.items():
        if not url.startswith("http"):  # url = NaN
            continue

        with tempfile.TemporaryDirectory() as tmpd:
            doc_id = url.split("/")[5]
            path_xlsx = Path(tmpd) / f"{doc_id}.xlsx"
            get_xlsx(path_xlsx, doc_id)
            xlsx = pd.read_excel(path_xlsx, sheet_name=None, dtype=object, keep_default_na=False)  # read without type sniffing
            path_csv = Path(GITHUB_WORKSPACE) / "logsheets" / "raw"
            path_csv.mkdir(parents=True, exist_ok=True)

            for sheet in ("observatory", "sampling", "measured"):
                xlsx[sheet].to_csv(path_csv / f'{habitat}_{sheet}.csv', index=False)
