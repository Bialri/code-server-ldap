FROM python:3.12

RUN apt-get update  &&  apt-get install -y --reinstall build-essential &&  apt-get install -y libsasl2-dev python-dev-is-python3 libldap2-dev libssl-dev
RUN pip install fastapi uvicorn python-ldap python-multipart

COPY . /app

WORKDIR /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]