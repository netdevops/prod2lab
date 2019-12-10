# prod2lab
Automatically consume router and switch production running configs, render lab configs, and put them on lab devices.


* create a `prod2lab.env` file

If you want to use the postgres database, change the `DJANGO_SETTINGS_MODULE` environment variable to `prod2app.settings.production`. The production module also enables the LDAP authentication functionality by default.

```
# REQUIRED
DJANGO_SETTINGS_MODULE=prod2app.settings.development
PROD2LAB_SECRET_KEY='-%nf2l6y%!#y-c-75mndrzkd()v-*bgcja5*@=aw7%&3-&&hh&'
PROD2LAB_SSH_USER=prod2lab_user
PROD2LAB_SSH_PASS=supersecretpassphrase
# OPTIONAL
POSTGRES_DB=prod2lab
POSTGRES_HOST=db
POSTGRES_USER=prod2lab
POSTGRES_PASSWORD=supersecretpassphrase
PROD2LAB_LDAP_SERVER_URI=ldaps://ad.example.corp
PROD2LAB_LDAP_SERVER_USERNAME=prod2lab_svc@example.corp
PROD2LAB_LDAP_SERVER_PASSWORD=supersecretpassphrase
PROD2LAB_LDAP_SERVER_SEARCH=ou=Accounts,dc=example,dc=corp
PROD2LAB_BROKER_URL=amqp://guest:guest@rabbitmq:5672
PROD2LAB_ADMIN_USER=admin
PROD2LAB_ADMIN_PASS=supersecretpassphrase
```

## Development Environment

* enable environment variables
```
source prod2lab.env
```
* create python development environment
```
python3 -m venv env
```
* use development environment
```
source env/bin/activate
```
* install python requirements
```
pip install -r requirements.txt
```
* spin up rabbitmq
```
docker run -d --name rabbitmq -p 5672:5672 rabbitmq
```
* create database
```
./manage.py migrate
```
* create super user
```
./manage.py createsuperuser
```
* run django app
```
./manage.py runserver
```
* start celery
```
celery -A prod2app worker -l info
```

## Docker-compose Environment

* spin up docker containers
```
docker-compose up
```
* create super user
```
docker exec -it prod2lab_web_1 /opt/prod2lab/scripts/create_admin_user.sh
```
* optional: enable ldap
```
docker exec -it prod2lab_web_1 /opt/prod2lab/scripts/enable_ldap.sh
```
