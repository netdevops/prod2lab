#!/bin/bash

sed -i 's/\# \"django_auth_ldap.backend.LDAPBackend\"/\"django_auth_ldap.backend.LDAPBackend\"/g' /opt/prod2lab/prod2app/settings.py