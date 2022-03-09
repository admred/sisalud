FROM python:3.7-alpine

RUN adduser sisalud

WORKDIR /home/sisalud

COPY requirements.txt .
COPY webapp webapp

RUN python3 -m venv venv

RUN venv/bin/pip3 install --timeout 60 --retries 5 -r sisalud/requirements.txt

RUN chown -R sisalud.sisalud /home/sisalud

EXPOSE 5000

CMD "./run.sh"

