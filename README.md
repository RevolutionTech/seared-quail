## Seared Quail
#### Created by: Lucas Connors

### Prerequisites

Seared Quail requires [PostgreSQL](http://www.postgresql.org/), which you can install on debian with:

    sudo apt-get install postgresql postgresql-contrib libpq-dev python-dev

I recommend using a virtual environment for Seared Quail. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenv virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv seared-quail

In the future you can reactivate the virtual environment with:

    workon seared-quail

### Installation

Then in your virtual environment, you will need to install Python dependencies such as [gevent](http://www.gevent.org/), psycopg2, psycogreen, [Gunicorn](http://gunicorn.org/), [django](https://www.djangoproject.com/), and [pillow](https://pillow.readthedocs.org/). You can do this simply with the command:

    pip install -r requirements.txt

### Configuration

Next we will need to create a file in the same directory as `settings.py` called `settings_secret.py`. This is where we will store all of the settings that are specific to your instance of Seared Quail. Most of these settings should be only known to you. Your file should define a secret key, and the database credentials. Your `settings_secret.py` file might look something like:

    SECRET_KEY = '-3f5yh&(s5%9uigtx^yn=t_woj0@90__fr!t2b*96f5xoyzb%b'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'abc123'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database.

With everything installed and all files in place, you may now create the database tables. You can do this with:

    python manage.py migrate

### Deployment

Since Seared Quail uses websockets, Apache with mod_wsgi is not a valid production setup. Instead, we will use Gunicorn with [runit](http://smarden.org/runit/) and [Nginx](http://nginx.org/). You can install them with the following:

    sudo apt-get install runit nginx

Then we need to create the Nginx configuration for Seared Quail:

    cd /etc/nginx/sites-available
    sudo nano mydomain.com

And in this file, generate a configuration similar to the following:

    server {
        server_name mydomain.com;

        access_log off;

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
            proxy_pass http://127.0.0.1:8000/socket.io;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        location / {
            proxy_pass http://127.0.0.1:8000;
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

    GUNICORN=/home/lucas/.virtualenvs/seared-quail/bin/gunicorn
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
