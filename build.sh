#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "prince"
password = "prince"

user, created = User.objects.get_or_create(username=username)
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

print("Superuser password reset successfully")
EOF
