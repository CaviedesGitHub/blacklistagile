export FLASK_APP=flaskr.application.py
export FLASK_DEBUG=1
export FLASK_ENV=development

export RDS_DB_NAME=blacklist
export RDS_USERNAME=admin
export RDS_PASSWORD=admin
export RDS_HOSTNAME=localhost
export RDS_PORT=5432

sudo ufw allow 5000
gunicorn --bind 0.0.0.0:5000 wsgi:application

