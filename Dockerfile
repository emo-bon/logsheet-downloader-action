FROM python:3.9
RUN pip install pandas openpyxl
RUN pip install git+https://github.com/emo-bon/emobon-dm-tools.git@release/v0.1.0
COPY action.py /opt/action.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
ENTRYPOINT ["/opt/entrypoint.sh"]
