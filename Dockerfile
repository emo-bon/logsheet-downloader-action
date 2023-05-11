FROM python:3.9
RUN pip install pandas pyyaml openpyxl
RUN pip install git+https://github.com/emo-bon/emobon-dm-tools.git@release/v0.0.0
COPY action.py /action.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
