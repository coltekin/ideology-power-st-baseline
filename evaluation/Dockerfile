FROM python:3-slim

COPY requirements.txt /requirements.txt
RUN pip3 install -r  /requirements.txt

COPY evaluate.py /evaluate.py
COPY parliaments.py /parliaments.py

ENTRYPOINT [ "/evaluate.py" ]
