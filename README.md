
# Elevator Assignment
By: hemant.cdy@gmail.com

## Content:

1. About
2. Project Setup
3. 

### About
This repository serves as the backend for an elevator management system, offering an end-to-end solution for various aspects of elevator management. It includes functionalities for initializing elevator systems with custom floors and elevators, managing user requests, handling maintenance, optimizing traffic flow, and planning elevator routes. 

### Project Setup

Note: The project is recommended to be run in a Linux Ubuntu OS.

Download the code using the link: 
https://github.com/hkc03/elevator/archive/refs/heads/production.zip



1. Unzip the project and it should contain two folders namely elevator, elevator_api and two files manage.py and requirements.txt. 
2. Once you are in the project directory, install virtualenv by running the command     

        pip install virtualenv 

3. After successful installation, create a new virtual environment by running 

        virtualenv venv


4. This will create a new folder named "venv" within the current directory.Activate the virtual environment by running:

        source venv/bin/activate

5. Open your terminal inside the terminals and exceute the command:
        
        pip install -r requirements.txt


6. Setting up Postgres:

        sudo -i -u postgres psql
        CREATE DATABASE personal;
        CREATE USER personal WITH ENCRYPTED PASSWORD '1234';
        \q
7. Setting up Django:


