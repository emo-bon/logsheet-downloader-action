import os
import pandas as pd
import requests
import shutil
import uritemplate
import uuid
import yaml

def get_xlsx(doc_id, path):
    ut = "https://docs.google.com/spreadsheets/d/{id}/export{?format,id}"
    url = uritemplate.expand(ut, {"id": doc_id, "format": "xlsx"})
    r = requests.get(url, allow_redirects=True)
    
    with open(os.path.join(path, f"{doc_id}.xlsx"), "wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    GITHUB_WORKSPACE = "/github/workspace"
    
    with open(os.path.join(GITHUB_WORKSPACE, "config", "google-docs.yml"), "r", encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.BaseLoader)

    for habitat in ("water", "sediment"):
        url = config[habitat]
        
        if not url.startswith("https://"):
            continue

        doc_id = url.split("/")[5]
        tmp = str(uuid.uuid1())
        path_xlsx = os.path.join(GITHUB_WORKSPACE, tmp)
        
        if not os.path.exists(path_xlsx):
            os.makedirs(path_xlsx)

        get_xlsx(doc_id, path_xlsx)
        xlsx = pd.read_excel(os.path.join(path_xlsx, f"{doc_id}.xlsx"), sheet_name=None)
        path_csv = os.path.join(GITHUB_WORKSPACE, "downloads", "gdoc-csv")
        
        if not os.path.exists(path_csv):
            os.makedirs(path_csv)

        for sheet in ("observatory", "sampling", "measured"):
            xlsx[sheet].to_csv(os.path.join(path_csv, f'{habitat}_{sheet}.csv'), index=False)

        shutil.rmtree(path_xlsx)
