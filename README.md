# Seared Quail

[![Build Status](https://travis-ci.org/RevolutionTech/seared-quail.svg?branch=master)](https://travis-ci.org/RevolutionTech/seared-quail)
[![codecov](https://codecov.io/gh/RevolutionTech/seared-quail/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/seared-quail)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf08621ec3d54837b3d64f8e880f6d9e)](https://www.codacy.com/app/RevolutionTech/seared-quail)

![Seared Quail](https://revolutiontech.s3.amazonaws.com/media/img/searedquail1.png)

***

## About

Seared Quail is an open-source digital restaurant menu web application. Below are instructions for setup and deployment for which you can create your own Seared Quail instance in a restaurant setting. Once your instance is deployed you can customize the menu in the Django admin interface for your restaurant. You are also welcome to fork the project and make changes specific to your use case as per the license provided in this project.

Seared Quail is under active development. Follow my progress [on Trello](https://trello.com/b/6KWEejar).

## Setup

### Prerequisites

Seared Quail requires [PostgreSQL](https://www.postgresql.org/) to be installed.

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Seared Quail uses [python-dotenv](https://github.com/theskumar/python-dotenv) to read environment variables in from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate

### Deployment

Before deploying, you will need to add some additional environment variables to your `.env` file. See `prod.py` for the environment variables used in production.

###### Note: The remainder of this section assumes that Seared Quail is deployed in a Debian Linux environment.

Since Seared Quail uses websockets, Apache with mod_wsgi is not a valid production setup. Instead, we will use Gunicorn with [runit](http://smarden.org/runit/) and [Nginx](http://nginx.org/). You can install them with the following:

    sudo apt-get install runit nginx

Then we need to create the Nginx configuration for Seared Quail:

    cd /etc/nginx/sites-available
    sudo nano mydomain.com

And in this file, generate a configuration similar to the following:

    server {
        server_name www.mydomain.com;
        return 301 http://mydomain.com$request_url;
    }

    server {
        server_name mydomain.com;

        access_log off;

        location /static/ordered_model/ {
            alias /home/lucas/.virtualenvs/seared-quail/lib/python2.7/site-packages/ordered_model/static/ordered_model/;
        }
        location /static/admin/ {
            alias /home/lucas/.virtualenvs/seared-quail/lib/python2.7/site-packages/django/contrib/admin/static/admin/;
        }
        location /static/ {
            alias /home/lucas/seared-quail/static/;
        }
        location /media/ {
            alias /home/lucas/seared-quail/media/;
        }

        location /socket.io {
            proxy_pass http://127.0.0.1:8001/socket.io;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        location /favicon.ico {
            alias /home/lucas/seared-quail/static/favicon.ico;
        }

        location / {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
    }

Save the file and link to it from sites-enabled:

    cd ../sites-enabled
    sudo ln -s ../sites-available/mydomain.com mydomain.com

Then we need to create a script to run Seared Quail on boot with runit:

    sudo mkdir /etc/sv/seared-quail
    cd /etc/sv/seared-quail
    sudo nano run

In this file, create a script similar to the following:

    #!/bin/sh

    GUNICORN=/home/lucas/.cache/pypoetry/virtualenvs/seared-quail-py3.6/bin/gunicorn
    ROOT=/home/lucas/seared-quail/seared_quail
    PID=/var/run/gunicorn.pid

    APP=seared_quail.wsgi:application

    if [ -f $PID ]; then rm $PID; fi

    cd $ROOT
    exec $GUNICORN -c $ROOT/seared_quail/gunicorn.py --pid=$PID $APP

Then change the permissions on the file to be executable and symlink the project to /etc/service:

    sudo chmod u+x run
    sudo ln -s /etc/sv/seared-quail /etc/service/seared-quail

Seared Quail should now automatically be running on the local machine.
