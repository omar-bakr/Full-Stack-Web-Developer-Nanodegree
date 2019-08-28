# Item Catalog project
## Description
This is the second project for the [Udacity full stack web developer nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) ,this is a web application that provides a list of items within a variety of categories as well as provide a user registration and authentication system,where registered users will have the ability to post, edit and delete their own items.



## Pre-requisites
* python3
* Vagrant
* VirtualBox
* Git


## How to run 
1.Download and install last version of [Vagrant ](https://www.vagrantup.com/), [Virtual Box](https://www.virtualbox.org/wiki/Downloads),[Git](https://git-scm.com/downloads)
and [Python](https://www.python.org/downloads/)

2.open bash terminal and type the following 

```bash
git clone https://github.com/omar-bakr/Full-Stack-Web-Developer-Nanodegree.git

cd Project 2

vagrant up

vagrant ssh

cd /vagrant

python database_setup.py

python dummy_data.py

python app.py

```
Then open chrome or any browser and go to this URL to see the web application :-

http://localhost:5000

## JSON endpoints

http://localhost:5000/catalog.json

http://localhost:5000/category_name.json

http://localhost:5000/catalog/category_name/item_name.json



