# prod2lab
Automatically consume router and switch production running configs, render lab configs, and put them on lab devices.

## Development Environment

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