#!/usr/bin/env python
import pandas as pd
import shutil
import uuid
import yaml
from pathlib import Path
from pyedm.gg import get_xlsx

GITHUB_WORKSPACE = Path("/github/workspace")

# read workflow properties as configuration file
with open(GITHUB_WORKSPACE / "config" / "workflow_properties.yml", "r", encoding="utf-8") as f:
    config = yaml.load(f.read(), Loader=yaml.BaseLoader)

# download logsheets for each habitat
for habitat in ("water", "sediment"):
    url = config[habitat]
    
    if not url.startswith("http"):  # url = NaN
        continue

    doc_id = url.split("/")[5]
    temp_folder_name = str(uuid.uuid1())  # uuid to avoid name collision
    path_xlsx = GITHUB_WORKSPACE / temp_folder_name
    path_xlsx.mkdir(parents=True, exist_ok=True)

    get_xlsx(path_xlsx / f"{doc_id}.xlsx", doc_id)
    xlsx = pd.read_excel(path_xlsx / f"{doc_id}.xlsx", sheet_name=None, dtype=object, keep_default_na=False)  # read without type sniffing
    path_csv = GITHUB_WORKSPACE / "logsheets" / "raw"
    path_csv.mkdir(parents=True, exist_ok=True)

    for sheet in ("observatory", "sampling", "measured"):
        xlsx[sheet].to_csv(path_csv / f'{habitat}_{sheet}.csv', index=False)

    shutil.rmtree(path_xlsx)
