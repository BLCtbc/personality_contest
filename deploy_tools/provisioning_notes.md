Provisioning new site
===============================

## Prereqs

* nginx
* python 3.6.x (django, gunicorn, virtualenv)
* memcached
* Git
* certbot (SSL encryption)
* fail2ban
* postgresql


## setup (unordered)

- install various essential packages/libraries (nginx, python3.6.x, memcached)
- setup virtual env
- set SITENAME, USERNAME, and PROJECTNAME env vars in venv source file (typically here: /venv/bin/activate)
- run virtual env
- install python libraries in requirements.txt
- open fabfile and edit repo REPO_URL
- run fabfile
- create django project (if not pulled from repo)
- `django-admin startproject SITENAME .`
    - `python manage.py startapp APPNAME`
-

```
$ sudo apt-get install nginx memcached git certbot-nginx certbot fail2ban postgresql
```

#### Environment variables for use with the sed command throughout setup

`SITENAME` should be the actual website address, `USERNAME` should be the same as
the username account on the server/system, and `PROJECTNAME` should be the name of the Django project

```
$ export SITENAME=www.example.com USERNAME=myusername PROJECTNAME=example
```
test:
```
$ echo $SITENAME
```

### installing Python 3.6.x

##### Raspbian (Originally followed [these instructions](https://installvirtual.com/install-python-3-on-raspberry-pi-raspbian/)):

```
$ sudo apt-get update
$ sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
$ wget https://www.python.org/ftp/python/3.6.11/Python-3.6.11.tgz
$ sudo tar -xvf Python-3.6.8.tgz
$ cd Python-3.6.8
$ sudo ./configure --with-ensurepip=install
$ sudo make && sudo make install
```

##### Debian:

```
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev libreadline-gplv2-dev libgdbm-dev libc6-dev
$ cd ~
$ wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
$ tar -xvf Python-3.6.9.tgz
$ cd Python-3.6.9
$ ./configure --with-ensurepip=install
$ sudo make && sudo make install
```
##### make python3.6.x the default
```
$ nano ~/.bashrc
```
add the following line:
```
alias python='/usr/local/bin/python3.6'
```
then source the .bashrc file:
```
$ source ~/.bashrc

```
test:
```
$ python
Python 3.6.8 (default, Mar 12 2021, 12:00:25)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
##### set python3.6.9 as default for  `python3` (old)
```
$ sudo update-alternatives --install /usr/bin/python3 python3 ~/Python-3.6.9/python 10
```
test:
```
$ python3
Python 3.6.9 (default, Jul 18 2019, 15:22:48)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

#### setup database
* start the server and login
    * linux
    ```
    $ sudo -u postgres psql
    ```
    * mac (assuming installation was via [homebrew](https://wiki.postgresql.org/wiki/Homebrew))
    ```
    $ brew services start postgresql
    $ psql postgres
    ```
* create database/user with [optimal](https://docs.djangoproject.com/en/3.0/ref/databases/#optimizing-postgresql-s-configuration) settings
```
postgres=# CREATE DATABASE $myproject;
postgres=# CREATE USER $myprojectuser WITH PASSWORD 'password';
postgres=# ALTER ROLE $myprojectuser SET client_encoding TO 'utf8';
postgres=# ALTER ROLE $myprojectuser SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE $myprojectuser SET timezone TO 'UTC';
```
* grant permissions, then quit
```
postgres=# GRANT ALL PRIVILEGES ON DATABASE $myproject TO $myprojectuser;
postgres=# \q
```

#### setup nginx
```
$ cd ~/$SITENAME/tools/deploy
$ sudo cp nginx.template.conf /etc/nginx/sites-available/nginx.template.conf
$ cd /etc/nginx/sites-available
$ sed -i "s/SITENAME/$SITENAME/g" nginx.template.conf
$ sed -i "s/USERNAME/$USERNAME/g" nginx.template.conf
$ sudo mv nginx.template.conf $SITENAME
$ sudo ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
```

#### setup fail2ban

#### Getting an SSL certificate
```
$ sudo certbot --nginx -d $SITENAME
```

#### setup logrotate for gunicorn
```
$ cd ~/$SITENAME/tools/deploy
$ sudo cp logrotate.template.conf /etc/logrotate.d/$SITENAME
$ cd /etc/logrotate.d/$SITENAME
$ sed -i "s/SITENAME/$SITENAME/g" logrotate.template.conf
```
#### setup virtualenv:
```
$ pip install virtualenv
$ cd ~/$SITENAME
$ python3.6 -m venv venv
```

#### activate virtualenv:
1. navigate to folder where repo will live
```
$ cd \path\to\your\repo
```

2. clone repo into said folder
```
$ git clone repo_url
```
3. install virtual env via pip
```
$ pip install virtualenv
```
4. create the virtual environment
    unix:
```
$ python3.6 -m venv venv
```
    windows:
```
$ python -m venv venv
```
5. activate virtual env
    unix:
```
$ source venv/bin/activate
```
    windows:
```
$ source venv/scripts/activate
```
6. install requirements
```
(venv) $ pip install -r tools/deploy/requirements.txt
```

#### set up testing suite (recommended)

1. get database username
    either from `settings.py`, see: `'USER': username`
    or
    if using env vars, `$ echo $DB_USER` (must have virtual env activated)
```
(venv) $ echo $DB_USER
username
```
2. give username found above CREATEDB permission (a test database is created and destroyed each time tests are ran)
```
$ psql postgres
postgres=# ALTER USER username CREATEDB;
postgres=# \q
```

#### import existing data into database (optional)
```
(venv) $ python manage.py loaddata datadump.json --exclude=contenttypes --exclude=auth --exclude=home.ConsumeList --exclude=home.Spec --exclude=home.Rating --exclude=home.TreeAllotted --exclude=home.Consume
```

#### start the services
```
$ sudo systemctl reload nginx
$ sudo systemctl enable gunicorn-$SITENAME
$ sudo systemctl start gunicorn-$SITENAME
```
installing memcached: https://memcached.org/downloads
memcached -d -s /tmp/memcached.sock // running memcache as a daemon and listening via socket
memcached -d -p <port> // running memcache as a daemon and listening to custom port (defaults to port 11211)

brew services start memcached // on macos with brew

environment variables should be stored in the gunicorn service above the ExecStart and below the WorkingDirectory
