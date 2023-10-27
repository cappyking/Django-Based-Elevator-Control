
# Elevator Assignment
By: hemant.cdy@gmail.com

## Content:

1. About
2. Milestones Achieved
3. Notes for Developer/Assumptions made
4. Project Setup
5. 

### About
This repository serves as the backend for an elevator management system, offering an end-to-end solution for various aspects of elevator management. It includes functionalities for initializing elevator systems with custom floors and elevators, managing user requests, handling maintenance, optimizing traffic flow, and planning elevator routes. 

### Milestones Achieved:
- [x]Initialise the elevator system to create ‘n’ elevators in the system
- [x]Fetch all requests for a given elevator
- [x]Fetch the next destination floor for a given elevator
- [x]Fetch if the elevator is moving up or down currently
- [x]Saves user request to the list of requests for a elevator
- [x]Mark a elevator as not working or in maintenance 
- [x]Open/close the door.

Additional Features:
- In the event that a lift goes under maintenance while other lifts are still operational within the same elevator system, the pending requests of the unavailable elevator shall be evenly distributed among the other elevators.

### Notes for Developer/Assumptions made:
- The project is recommended to be run in a Linux Ubuntu OS.
- The project was tested in Postman using both FormData and RawJSON and it is recommended that the project is tested there.
- The project makes an assumption that, on each floor, there will be individual call buttons for each elevator in the system.
- It is also assumed that the number of floors are to be requested by the user.
- Lastly, it is assumed that no simulation system was to built to show movement of the lift.


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


6. Setting up Postgres: Follow the following commands in sequence

        sudo -i -u postgres psql
        CREATE DATABASE personal;
        CREATE USER personal WITH ENCRYPTED PASSWORD '1234';
        \q
7. Setting up Django: 
Make sure your environment is active and follow the following commands in sequnce:

a. ```python manage.py runserver```: This command will start the development server to ensure everything is running correctly. If the server starts successfully without any errors, you can stop it by pressing Ctrl + C.

b. ```python manage.py makemigrations```: Use this command to create the initial database migrations for the project.

c. ```python manage.py migrate``` : Run this command to apply the database migrations and create the necessary tables in the database.

d. ```python manage.py createsuperuser```: Execute this command to create an admin account that will allow you to access the project's admin panel. Provide a username and password when prompted.

e. ```python manage.py runserver```: Finally, start the development server again to run the project.


### 