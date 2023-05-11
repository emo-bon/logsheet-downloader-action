# logsheet-downloader-action

To give an example, the following workflow file will download the logsheets, convert them to csv format and commit the changes if relevant.

```
on:
  push:
  schedule:
    - cron: '0 0 1 * *'
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: logsheet-downloader-action
        uses: emo-bon/logsheet-downloader-action@master
      - name: git-auto-commit-action
        uses: stefanzweifel/git-auto-commit-action@v4
```
