# Linux Server Configuration 
## Description
This is the third project for the [Udacity full stack web developer nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) ,it 's a baseline installation of a Linux server then preparing it to host a web application.the server is also secured from a number of attack vectors with installation and configuration the database server, and deploy one of an  existing web applications into it .


## Server Details
Server IP Address: 18.185.149.226

SSH server access port: 2200

SSH login username: grader

Application URL: http://18.185.149.226/
## Setting up the Server 
### 1.SSH into the server
* Download default public key file from ssh keys section on aws account 
* Then run this command to log into the server 
``` bash
 ssh -i LightsailDefaultKey-eu-central-1.pem ubuntu@18.185.149.226
  ```
### 2.Update all currently installed packages
``` bash
sudo apt-get update 
sudo apt-get upgrade
  ```
## 3.changing ssh port
``` bash
cd /etc/ssh
sudo nano sshd_config
  ```
  * on line 13 change port number from 22 to 2200 then save 

  ## 4.Firewall configuration 
  
  * enabling only the following ports SSH (port 2200), HTTP (port 80), and NTP (port 123)
  ``` bash
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow ntp
sudo ufw enable 
  ```
  * then running 
   ``` bash
sudo ufw status 
```
* you should see the following 
```bash
  Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
```
* click on the Manage option of the Amazon Lightsail Instance, then the Networking tab, and then change the firewall configuration to match the internal firewall settings above.
## 5.creating user grader and giving it sudo permission
* run the following 
```bash
sudo adduser grader

sudo cp /etc/sudoers.d/90-cloud-init-users /etc   sudoers.d/grader

sudo nano /etc/sudoers.d/grader
```
* change the following line
 ubuntu    ALL=(ALL:ALL) ALL to be grader ALL=(ALL:ALL) ALL

 ## 6.creating an SSH key pair for grader
* In your local machine run 
```bash 
ssh-keygen
```
* then two file will be generated in .ssh directory

1.id_rsa

2.id_rsa.pub 

* where the second file will be placed on the server 
* log in into ubuntu and switch user to grader the run the follwoing 
```bash
mkdir .ssh
chmod 700 .ssh
cd .ssh/
touch authorized_keys
chmod 644 authorized_keys
nano authorized_keys
```
* then paste the content of id_rsa.pub file in authorized_keys and save 

* you are now able to ssh into grader using the follwing 
```bash
ssh -i .ssh/id_rsa grader@18.184.180.50 -p 2200 
```
## 7.configure the local timezone to UTC.
```bash
sudo timedatectl set-timezone UTC
```
## 8.Install Apache 
```bash
sudo apt install apache2
```

## 9.installing git

* install git
```bash
sudo apt install git
```
* configuring git
```bash
git config --global user.name "omar.bakr"
git config --global user.email "email"
```

## 10.installing pip
the package pip required to install certain packages
```bash
sudo apt install python-pip
```

## 11. installing and configuring postgresql
* install postgresql
```bash
sudo apt install postgresql
```
* log in as the user postgres
```bash
 sudo su - postgres
 ```
 * open psql shell
 ```bash
 psql
 ```
 * type the follwoing commands one by one 
```postgres 
postgres=# CREATE DATABASE catalog;
postgres=# CREATE USER catalog;
postgres=# ALTER ROLE catalog WITH PASSWORD 'yourpassword';
postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
```
* then exit from the terminal by running \q followed by exit.

## 12.setting up apache to run the flask application

* Installing mod_wsgi
```bash
sudo apt install libapache2-mod-wsgi
``` 
* cloning the Item Catalog flask application, run the commands one by one
```bash
cd /var/www/

sudo mkdir FlaskApp

cd FlaskApp/

sudo git clonehttps://github.com/omar-bakr/Deploy.git FlaskApp
```
* install required packages
```bash
sudo pip install --upgrade Flask SQLAlchemy httplib2 oauth2client requests psycopg2
```
* setting up the virtualHost configuration
```bash
 sudo nano /etc/apache2/sites-available/FlaskApp.conf
 ```
 then add the following line to FlaskApp.conf :-

 ```bash
 <VirtualHost *:80>
   ServerName 18.185.149.226
   ServerAdmin email
   WSGIScriptAlias / /var/www/FlaskApp/FlaskApp/flaskapp.wsgi
   <Directory /var/www/FlaskApp/FlaskApp/>
       Require all granted
   </Directory>
   Alias /static /var/www/FlaskApp/FlaskApp/static
   <Directory /var/www/FlaskApp/FlaskApp/static/>
       Require all granted
   </Directory>
   ErrorLog ${APACHE_LOG_DIR}/error.log
   LogLevel warn
   CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
* enable the virtual host
```bash
 sudo a2ensite FlaskApp
 ```
 * restsrt apache 
 ```bash
sudo service apache2 restart
 ```

* creating the .wsgi File
apache uses the .wsgi file to serve the Flask app. move to the /var/www/FlaskApp/ directory and create a file named flaskapp.wsgi with following commands:
```bash
cd /var/www/FlaskApp/FlaskApp/
sudo nano flaskapp.wsgi
```
Add the following lines to the flaskapp.wsgi file:
```python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/FlaskApp/")

from app import app as application
application.secret_key = 'super_secret_key'
```
* restart apache server

```bash
sudo service apache2 restart
```
now you should be able to run the application at http://18.185.149.226/

## 13.Debugging
* If you are getting an Internal Server Error or any other error(s), make sure to check out Apache's error log for debugging:
```bash
sudo cat /var/log/apache2/error.log
```

## Resources
* [How To Deploy a Flask Application on an Ubuntu VPS](https://digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

* [Initial Server Setup with Ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)

 * [Ask ubuntu](https://askubuntu.com/)