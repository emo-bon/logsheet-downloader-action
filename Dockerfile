FROM python:3.9
RUN pip install pandas requests uritemplate pyyaml openpyxl
COPY gdrive_client.py /gdrive_client.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
