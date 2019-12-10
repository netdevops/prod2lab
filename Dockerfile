FROM python:3-buster

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y install postgresql-client sshpass libldap2-dev libsasl2-dev ldap-utils
RUN echo "tls_reqcert never" >> /etc/ldap/ldap.conf

COPY . /opt/prod2lab/

RUN pip install -r /opt/prod2lab/requirements.txt
