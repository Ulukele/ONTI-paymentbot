FROM python:3

COPY src/requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY src/ src/

WORKDIR src/


