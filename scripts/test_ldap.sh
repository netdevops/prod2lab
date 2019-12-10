#!/bin/bash

ldapsearch -x -LLL -H $LDAP_SERVER_URI -D $LDAP_SERVER_USERNAME -w $LDAP_SERVER_PASSWORD -b $LDAP_SERVER_SEARCH -s sub "(objectClass=user)"