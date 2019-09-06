# Linux Server Configuration 
## Description
This is the third project for the [Udacity full stack web developer nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) ,it 's a baseline installation of a Linux server then preparing it to host a web application.the server is also secured from a number of attack vectors with installation and configuration the database server, and deploy one of an  existing web applications into it .


## Server Details
Server IP Address: 18.184.180.50

SSH server access port: 2200

SSH login username: grader

Application URL: http://18.184.180.50

## Setting up the Server 
### 1.SSH into the server
* Download default public key file from ssh keys section on aws account 
* Then run this command to log into the server 
``` bash
 ssh -i LightsailDefaultKey-eu-central-1.pem ubuntu@18.184.180.50
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
## 8.Install and configure Apache to serve a Python mod_wsgi application
```bash

sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
