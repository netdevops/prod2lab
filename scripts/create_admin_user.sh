#!/bin/bash

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username=\"$PROD2LAB_ADMIN_USER\", password=\"$PROD2LAB_ADMIN_PASS\", email=None)" | python /opt/prod2lab/manage.py shell