# Building Item Catalog
This is the 4th project in Udacity.

## About This Project
This project utilizing the flask framework and allow access to the SQL database using Google Accounts . we used Oauth2
to apply CRUD operations.i got the oauth2 from [Google Developer Console](https://www.developers.google.com).
## Files In This Repository
this project has 3 main files 
*database_setup.py* --> For Creating The SQL Database<br>
*flowers.py*--> For Populating the Database<br>
*Final.py*--> Which Runs The Flask Application

## Technologies Used
1. Html & Css
2. OAuth from google developers Console
3. Flask 

## How To Install
There are some Instructions Below To Install These
1. Install [Vagrant](https://www.vagrantup.com/) & [VirtualBox](https://www.virtualbox.org/wiki/Downloads) from the given links
2. Create Vagrantfile
3. Go to Vagrant directory 
3. Launch VM (`vagrant up`)
4. Log in to VM (`vagrant ssh`)
5. Go to `cd/vagrant` 
6. Run File `python /item-catalog/database_setup.py`
7. Run File `python /item-catalog/flower.py`
8. Run File `python /item-catalog/final.py`
9. Go To Application locally using http://localhost:5000


## Getting Google Signin
FolloW These Steps

1. First of all Go to [Google Developer Console](https://console.developers.google.com)
2. Login with Your Google Account
3. then Credintials >>Create Crendentials >> OAuth Client ID
4. Enter any Name You Want
5. Enter origins = 'http://localhost:5000'
6. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
7. Click  on Create
8. Copy the Client ID
9. paste in login.html
