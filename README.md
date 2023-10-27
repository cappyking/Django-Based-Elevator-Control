
# Elevator Assignment
By: hemant.cdy@gmail.com

## Content:

1. About
2. Milestones Achieved
3. Notes for Developer/Assumptions made
4. Repository Structure
5. Architectural Design
5. Database Design
6. Project Setup
7. Testing

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
- Video link to postman testing/project demo: https://drive.google.com/file/d/1zavwNSm1tnhK-66VeTzsXtmkiyW7VaCD/view?usp=sharing
- the BASE_URL mentioned throughout this documment is the ip and port you are running the project on. Usually it is ```http://localhost:8000/```
- The project makes an assumption that, on each floor, there will be individual call buttons for each elevator in the system.
- It is also assumed that the number of floors are to be requested by the user.
- Lastly, it is assumed that no simulation system was to built to show movement of the lift.

### Repository Structure
        .
        ├── elevator/
        │   ├── asgi.py
        │   ├── __init__.py
        │   ├── __pycache/
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── elevator_api/
        │   ├── admin.py
        │   ├── apps.py
        │   ├── __init__.py
        │   ├── migrations/
        │   ├── models.py
        │   ├── __pycache__/
        │   ├── serializers.py
        │   ├── services.py
        │   ├── tests.py
        │   ├── urls.py
        │   └── views.py
        ├── manage.py
        ├── README.md
        ├── requirements.txt
        └── Elevator System.postman_collection.json

### Architectural Design
1. Technology Stack
- Database: PostgreSQL is chosen as the relational database for its robustness, data integrity, and scalability.

- Framework: Django is the primary framework for developing the backend. It provides a powerful and secure foundation for web applications.

- API Development: Django Rest Framework (DRF) is used to create a RESTful API for communication between the frontend and backend. DRF simplifies API development and serialization.
- No extra library or plugin has been used apart from the mentioned choices in the instruction.

2. Components
- Django Application: The core component of the backend, built using the Django framework. It includes the application logic, models, views, and URLs.

- Database: PostgreSQL is the backend database management system that stores and retrieves data efficiently. It is a reliable choice for data persistence.

- Django Models: Django models define the database schema. Models are used to represent data entities such as Elevator, Floor, and ElevatorRequest.

- API Endpoints: DRF is used to create API endpoints that handle requests and responses for elevator management, user interactions, and data retrieval.

- Views: Django views process HTTP requests, interact with models and serializers, and return responses. DRF serializers are used for data serialization.



### Database Design:

The database design for this Django application is created to model the functionality of an elevator management system. The design includes four main models: `ElevatorSystem`, `Elevator`, `Floor`, and `ElevatorRequest`. Here's an explanation of why each model is included and its role in the system:

1. **ElevatorSystem**:
   - **Purpose**: The `ElevatorSystem` model represents an elevator system within a building or facility. It's responsible for managing a group of elevators and the associated floors.
   - **Attributes**: It has a `name` attribute to identify the system. This model is necessary to group and organize multiple elevators within the same system.

2. **Elevator**:
   - **Purpose**: The `Elevator` model represents individual elevator units within the system. It tracks the status and properties of each elevator.
   - **Attributes**: It includes attributes such as `name` (a user-friendly name for the elevator), `current_floor` (the current position of the elevator), `status` (indicating whether the elevator is stopped, moving up, moving down, or under maintenance), `operational` (a boolean field to indicate if the elevator is operational or under maintenance), and `door_open` (to track whether the elevator's doors are open). It also includes a unique `elevator_number` to identify the elevator within the system and a foreign key relationship with the associated `ElevatorSystem`.

3. **Floor**:
   - **Purpose**: The `Floor` model represents individual floors within the building. It's used to map the floors to the elevator system.
   - **Attributes**: It has a `floor_number` attribute to identify the floor, and it also establishes a foreign key relationship with the associated `ElevatorSystem`.

4. **ElevatorRequest**:
   - **Purpose**: The `ElevatorRequest` model is used to record requests made by users to move between floors using the elevators.
   - **Attributes**: It includes a foreign key relationship with the specific `Elevator` that is requested, `destination_floor` (the floor the user wants to reach), `from_floor` (the floor the user is starting from), a `timestamp` to record when the request was made, and a `completed` field to track whether the request has been fulfilled.

Overall, this database design provides the necessary structure to manage elevator systems, individual elevators, floors, and user requests efficiently. It allows for tracking the status of elevators, their positions, and user requests within a building, making it a fundamental part of the elevator management system's functionality.


### Project Setup

Note: The project is recommended to be run in a Linux Ubuntu OS.

Download the code using the link: 
https://github.com/hkc03/elevator/archive/refs/heads/test_ready.zip



1. Unzip the project and it should contain two folders namely elevator, elevator_api and two files manage.py and requirements.txt and one postman collection file.
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


### Testing 

Note: To set up Postman for testing, open Postman and follow these steps: Click on the "Import" option, then select "Select File." Navigate to the file named "Elevator System.postman_collection.json," and click on the file to select it. Finally, click the "Import" button. This will import the Postman collection for testing your project.

A. Initialization [POST]:

1. The initialization API , located at, BASE_URL+```initialize-elevator-system/``` accepts three parameters as form-data or Raw JSON:
-  ```name```: this parameneter defines the name of a particular elevator system.Acceptable values: Boolean
- ```num_elevators```: this defines the number of elevators you want to configure inside the particular elevator system. Acceptable values: Integer
- ```floors```: This defines the number of floors inside the system. Acceptable values: Integer

2. Success Response:
- Status Code 200

With example:
        
        {
    "message": "3 elevators have been initialized on floor 0 with 5 floors associated with the elevator system: Test | Created at 2023-10-27 06:46:49",
    "elevator_system": {
        "id": 31,
        "name": "Test | Created at 2023-10-27 06:46:49"
    },
    "elevators": [
        {
            "id": 128,
            "name": "Elevator 1 | Elevator System Test | Created at 2023-10-27 06:46:49 ",
            "current_floor": 0,
            "status": "stopped",
            "operational": true,
            "door_open": false,
            "elevator_number": 1,
            "elevator_system": 31
        },
        {
            "id": 129,
            "name": "Elevator 2 | Elevator System Test | Created at 2023-10-27 06:46:49 ",
            "current_floor": 0,
            "status": "stopped",
            "operational": true,
            "door_open": false,
            "elevator_number": 2,
            "elevator_system": 31
        },
        {
            "id": 130,
            "name": "Elevator 3 | Elevator System Test | Created at 2023-10-27 06:46:49 ",
            "current_floor": 0,
            "status": "stopped",
            "operational": true,
            "door_open": false,
            "elevator_number": 3,
            "elevator_system": 31
        }
    ],
    "floors": [
        {
            "id": 109,
            "floor_number": 1,
            "elevator_system": 31
        },
        {
            "id": 110,
            "floor_number": 2,
            "elevator_system": 31
        },
        {
            "id": 111,
            "floor_number": 3,
            "elevator_system": 31
        },
        {
            "id": 112,
            "floor_number": 4,
            "elevator_system": 31
        },
        {
            "id": 113,
            "floor_number": 5,
            "elevator_system": 31
        }
    ]
        }

B. Elevator Call button [GET]:

1. The API could be located at BASE_URL=```elevator-requests/``` and accepts 4 parameters:
- ```from_floor```: Defines the pickup floor. Acceptable value: Integer
- ```destination_floor```: Defines destination floor. Acceptable value: Integer
- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer

2. Success Response:
- 201 created status code 
- sample Response: ```"Added to queue"```

3. Error Response: 
- Elevator under maintenance: 503 Service unavailable error
- Invalid Data Type/Invalid elevator number/system number/floors raises a 400 Bad Request error

C. View Pending Requests [GET]:

1. The api could be located at ```elevator-requests/```  and accepts 2 parameters:
- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer

2. Success Response:
- 200 Ok status code
- Sample Response:
        
        [
        {
        "elevator_number": 3,
        "from_floor_number": 3,
        "destination_floor_number": 4,
        "timestamp": "2023-10-27T06:48:28.538547Z",
        "completed": false
        },
        {
        "elevator_number": 3,
        "from_floor_number": 3,
        "destination_floor_number": 1,
        "timestamp": "2023-10-27T06:49:52.611115Z",
        "completed": false
        }
        ]

3. Error Response:
- Elevator under maintenance: 503 Service unavailable error
- Invalid Data Type/Invalid elevator number/ raises a 400 Bad Request error

D. Door Open Close [Post]:

1. 1. The api could be located at ```toggle-door/```  and accepts 3 parameters:
- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer
- ```door_open```: Defines the choice you want. To open Send True, while to close send False. Acceptable value Boolean

2. Success Response:
- 200 Ok status code
- Sample Response when request is processed

        {
        "id": 128,
        "name": "Elevator 1 | Elevator System Test | Created at 2023-10-27 06:46:49 ",
        "current_floor": 0,
        "status": "stopped",
        "operational": true,
        "door_open": false,
        "elevator_number": 1,
        "elevator_system": 31
        }
- Response when door is already open or closed: ```Door already closed```

3. Error Response:
- Elevator under maintenance: 503 Service unavailable error
- Invalid Data Type/Invalid elevator number/door-open raises a 400 Bad Request error

E. Maintenance [Post]:

1. 1. The api could be located at ```toggle-door/```  and accepts 3 parameters:
- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer
- ```elevator_maintenance_request```: Defines the choice you want. To put elevator under maintenance Send True, while to resume operation send False. Acceptable value Boolean

2. Successful Response:

- 200 Ok status code
- Sample Response when request is processed:

        {
        "message": "All available requests for this elevator has been transferred to other operational elevators within the same elevator system.",
        "elevator_status": {
            "id": 129,
            "name": "Elevator 2 | Elevator System Test | Created at 2023-10-27 06:46:49 ",
            "current_floor": 0,
            "status": "stopped",
            "operational": false,
            "door_open": false,
            "elevator_number": 2,
            "elevator_system": 31
        }
        }

- The message can also be ```All pending requests have been marked cancelled since there are marked completed since no other elevator is available within this elevator system to fulfill the requests.``` based on elevator availablity.

3. Error Response:

-  Invalid Data Type/Invalid elevator number/elevator_maintenance_request raises a 400 Bad Request error

F. Elevator Direction [GET]:

1. The API is used to get the immediate direction with respect to current floor to pick or drop a user. It is located at BASE_URL+ ```get-direction/```. It accepts 2 parameters:

- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer

2. Success Response:
- 200 Ok status code
- Sample Response

        {
            "direction": "Upwards",
            "current_floor": 0
        }

3. Error Response:
- No pending requests for the elevator with status code 204 No Content.
- Elevator under maintenance: 503 Service unavailable error
- Invalid Data Type/Invalid elevator number/elevator_system raises a 400 Bad Request error

G. Next Elevator FLoor [GET]:

1. The API fetches the next floor with respect to the current floor of the elevator. It also handles route and elevator flow planning by taking in all the requests, prioritizing them based on the request with the earliest timestamp, and then further prioritizing them based on direction. It can be located at BASE_URL+```next-destination/```. It accepts the following two parameters:

- ```elevator_system```: Defines the Elevator System. Acceptable value: Integer
- ```elevator_number```: Defines the elevator number. Acceptable value :Integer

2. Success Response:
- 200 Ok status code
- Sample Success Response:
    
        {
        "next_destination_floor": 1,
        "elevator_flow_path": [
        1,
        3,
        4,
        5,
        3,
        1
        ]
        }
3. 3. Error Response:

- No pending requests for the elevator with status code 204 No Content.
- Elevator under maintenance: 503 Service unavailable error
- Invalid Data Type/Invalid elevator number/elevator_system raises a 400 Bad Request error
