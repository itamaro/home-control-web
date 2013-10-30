Home Control Web Server and Apps
================================

Django project & apps that implement the web-app front-end for the Home Control system.

See [my blog post](http://itamaro.com/2013/10/04/ac-control-project-bringing-it-together/) for extended description and design.

Additional Home-Control projects:

- [HomeControl RPC Agent](https://github.com/itamaro/home-control-RPC)
- [HomeControl Arduino A/C Controller](https://github.com/itamaro/home-control-arduino)

![Mobile UI in Action](docs/UI-in-Mobile-Action.png)


Requirements
------------

- [Django](https://www.djangoproject.com/) (developed and tested with v1.5).
- [Django JS Reverse](https://github.com/version2/django-js-reverse).


Installation
------------

As a Django project & apps, installation and deployment are not different than [other Django projects](https://docs.djangoproject.com/en/1.5/howto/deployment/) (several deployment configuration examples below).

1. Clone the repository to the server machine that will serve the site.
2. Optionally, create a `local_settings.py` file in [`HomeControlWeb/HomeControlWeb`](HomeControlWeb/HomeControlWeb) to override settings from the [generic settings](HomeControlWeb/HomeControlWeb/settings.py) (feel free to use [local_settings.py.sample](HomeControlWeb/HomeControlWeb/local_settings.py.sample) as a suggestion).
3. Run `manage.py syncdb` to initialize the DB (and create a super user).
4. Set up your web server of choice to serve the Django site.
5. [Deploy](https://docs.djangoproject.com/en/1.5/howto/static-files/deployment/) the [static files](https://github.com/itamaro/home-control-web/tree/master/static) to your web server of choice (global static files as well as app-specific static files!).
6. Access the admin interface (e.g. at `http://your-deployed-host/admin/`) to configure the installed apps (see the app-specific documentation for details on their configurations).
7. Win.


Available Apps
--------------

- [A/C Control App](HomeControlWeb/AC)
- [Webcam App](HomeControlWeb/cam)



Deployment Examples and Development Setup
=========================================


Web Server Agnostic Deployment on Ubuntu 12.04
----------------------------------------------

(tested with Ubuntu-Desktop-12.04.2-x64)

Install requirements:

* Python and various dependencies: `sudo apt-get install libexpat1 python-pip build-essential python-imaging python-pythonmagick python-markdown python-textile python-docutils`
 * **WARNING:** Do not install python-django via apt-get on 12.04 - the default repositories has an old version...
* Django, Django JS Reverse: `sudo pip install Django django-js-reverse`

Create webmasters group:

* `sudo groupadd webmasters`
* `sudo usermod -a -G webmasters <username>`

Create directories for static and media and configure ownerships:

* `sudo mkdir -p /var/www/home-control-web/static`
* `sudo chown www-data:webmasters -R /var/www/home-control-web/static`
* `sudo mkdir -p /var/www/home-control-web/media/webcam`
* `sudo chown www-data:webmasters -R /var/www/home-control-web/media`

Clone and configure the home-control-web project:

* `cd ~`
* `git clone https://github.com/itamaro/home-control-web.git`
* `cd home-control-web/HomeControlWeb/HomeControlWeb`
* `cp local_settings.py.sample local_settings.py`
  - Edit `local_settings.py` till happy.
* `cd ..`
* `python manage.py syncdb`
 * Create a super user

Deploy Django static files to statically served directory:

* `cd ~/home-control-web/HomeControlWeb`
* `python manage.py collectstatic`

After setting up a web server to serve the Django site (and static and media directories) (see web-server-specific examples below),
access the Django admin interface (e.g. `https://your.domain.com/home-control/admin/`) to configure the installed apps (see [app-specific](#available-apps) README's for further details).


Apache+WSGI on Ubuntu Deployment Example
----------------------------------------

(tested with Ubuntu-Desktop-12.04.2-x64)

Install Apache & mod-wsgi:

* Apache2, mod-WSGI: `sudo apt-get install apache2 apache2-mpm-prefork libapache2-mod-wsgi`

Add Apache to the webmasters group:

* `sudo usermod -a -G webmasters www-data`

Create a virtual host conf file for the Apache site:

* `cd /etc/apache2`
* `sudo <your-favorite-editor> sites-available/home-control-web`

```apache
<VirtualHost *:80>
     ServerAdmin <your@email>

     Alias /static/ /var/www/home-control-web/static/
     Alias /media/ /var/www/home-control-web/media/
     
     WSGIScriptAlias /home-control /home/username/home-control-web/HomeControlWeb/HomeControlWeb/wsgi.py
     WSGIDaemonProcess home-control python-path=/home/<username>/home-control-web/HomeControlWeb
     WSGIProcessGroup home-control

     <Directory />
          Options FollowSymLinks
          AllowOverride None
     </Directory>
     <Directory /var/www/home-control-web/>
          Options Indexes FollowSymLinks MultiViews
          AllowOverride None
          Order allow,deny
          allow from all
     </Directory>
     <Directory /home/<username>/home-control-web/HomeControlWeb/HomeControlWeb>
          <Files wsgi.py>
               Order deny,allow
               Allow from all
          </Files>
     </Directory>

     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Disable the default site and enable to home control web site:

* `sudo a2dissite 000-default`
* `sudo a2ensite home-control-web`

Reload the Apache server:

* `sudo service apache2 reload`


Nginx+Gunicorn on Ubuntu Deployment Example
-------------------------------------------

Soon


Local Development Setup in Windows
----------------------------------

(my dev-env is Windows 7 Professional SP1 x64)

1. Install Python, setuptools, pip, Git client (e.g. [Git Extensions](https://code.google.com/p/gitextensions/))
2. `pip install Django django-js-reverse south`
3. Clone `https://github.com/itamaro/home-control-web.git` to your local workspace (e.g. `C:\Users\<name>\Workspaces\home-control\home-control-web`.
4. Copy `local_settings.py.win-dev-sample` to `local_settings.py` in the `HomeControlWeb\HomeControlWeb` directory.
   * Edit it until you're happy.
5. In command prompt, cd to `C:\Users\<name>\Workspaces\home-control\home-control-web\HomeControlWeb`
6. `python manage.py syncdb`
   * Create super user. 
7. Create `media\webcam` directory next to the global `static` directory.
8. `python manage.py runserver`

The home-control site is now available on `http://localhost:8000/` -
access `/admin/` to configure app-settings, and hack away at the project.

You would probably also want to set up a local development environment of the [home-control-RPC project](https://github.com/itamaro/home-control-RPC/) in order to have a fully functional setup.

Please share interesting stuff you do!
