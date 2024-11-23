#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Set the correct time zone (replace US/Eastern with your desired time zone)
export TZ=US/Eastern
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Start rsyslog for cron logging
rsyslogd

# Start cron service
echo "Starting cron service..."
service cron start

# Optional: Check if cron started successfully
if [[ $? -ne 0 ]]; then
  echo "Failed to start cron service."
  exit 1
fi
# Remove Django crontab jobs
python manage.py crontab remove

# Add Django crontab jobs
python manage.py crontab add

#python manage.py flush --no-input
#python manage.py migrate

exec "$@"
