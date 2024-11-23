# Pull official base image
FROM python:3.11

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    cron \
    tzdata \
    netcat-traditional \
    && apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Install Pillow first to handle specific dependencies
RUN pip install --no-cache-dir Pillow==10.4.0

# Install remaining dependencies from requirements.txt
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project files
COPY . .

# Run the Django crontab setup toremove previous jobs and then  register jobs
RUN /usr/local/bin/python /usr/src/app/manage.py crontab remove
RUN /usr/local/bin/python /usr/src/app/manage.py crontab add

# Ensure rsyslog is installed and configured
RUN apt-get update && apt-get install -y rsyslog

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Start cron and your application
#CMD service cron start && /usr/src/app/entrypoint.sh
