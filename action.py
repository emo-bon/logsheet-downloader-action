import os
import pandas as pd
import shutil
import uuid
import yaml
from pyedm.gg import get_xlsx

GITHUB_WORKSPACE = "/github/workspace"

with open(os.path.join(GITHUB_WORKSPACE, "config", "google-docs.yml"), "r", encoding="utf-8") as f:
    config = yaml.load(f.read(), Loader=yaml.BaseLoader)

for habitat in ("water", "sediment"):
    url = config[habitat]
    
    if not url.startswith("https://"):  # url = NaN
        continue

    doc_id = url.split("/")[5]
    temp_folder_name = str(uuid.uuid1())
    path_xlsx = os.path.join(GITHUB_WORKSPACE, temp_folder_name)
    
    if not os.path.exists(path_xlsx):
        os.makedirs(path_xlsx)

    get_xlsx(os.path.join(path_xlsx, f"{doc_id}.xlsx"), doc_id)
    xlsx = pd.read_excel(os.path.join(path_xlsx, f"{doc_id}.xlsx"), sheet_name=None)
    path_csv = os.path.join(GITHUB_WORKSPACE, "downloads", "gdoc-csv")
    
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)

    for sheet in ("observatory", "sampling", "measured"):
        xlsx[sheet].to_csv(os.path.join(path_csv, f'{habitat}_{sheet}.csv'), index=False)

    shutil.rmtree(path_xlsx)
