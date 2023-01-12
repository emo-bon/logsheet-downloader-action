# emobon_dm_gdrive_downloader

To give an example, the following workflow file will download the google drive sheets, convert them to csv format and commit the changes if relevant.

```
on:
  push:
  schedule:
    - cron: '0 0 * * 0'
jobs:
  emobon_job:
    runs-on: ubuntu-latest
    name: emobon dm gdrive downloader job
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: download
        uses: emo-bon/emobon_dm_gdrive_downloader@master
      - name: commit
        uses: stefanzweifel/git-auto-commit-action@v4
```
