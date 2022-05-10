# pull official base image
FROM python:3

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Temporarly install build Dependincies
#RUN apk update \
    #&& apk add --virtual build-deps postgresql-dev gcc python3-dev musl-dev \
    #&& apk add jpeg-dev zlib-dev libjpeg

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#remove temorary build depemdemcies
#RUN apk del build-deps

RUN apt-get update \
    && apt-get install -yyq netcat

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh


# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]