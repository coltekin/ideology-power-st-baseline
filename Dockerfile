# You should select the python version matching on your system
# so that the models saved by joblib are compatible.
FROM python:3-slim

COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r  /requirements.txt

COPY data.py /data.py
COPY parliaments.py /parliaments.py
COPY linear-baseline.py /linear-baseline.py

COPY models/ /models/

ENTRYPOINT [ "/linear-baseline.py", "-t", "orientation", "-t", "populism", "-t", "power", "-l", "/models", "all"]
