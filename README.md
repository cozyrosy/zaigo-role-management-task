# zaigo-role-management-task

## Role Management API
This Django REST framework project provides an API for managing roles, which are associated with rights. 
The API allows creating, retrieving, updating, and deleting roles, as well as associating rights with roles.

### Features
1. Create a new role with a name and associated rights. <br>
2. Retrieve a list of all roles, including their associated rights.<br>
3. Retrieve a single role by its primary key, including its associated rights.<br>
4. Update a role by its primary key, including updating its associated rights.<br>
5. Delete a role by its primary key.<br>
6. Permissions: Authentication is required for all operations on roles.<br>
7. Error handling: Appropriate error responses are provided for validation errors, non-existent roles or rights, and other error scenarios.

### Setup
1. Clone the repository: git clone https://github.com/cozyrosy/zaigo-role-management-task.git <br>
2. Install dependencies: pip install -r requirements.txt <br>
3. Create and configure the Django project and app. <br>
4. Migrate the database: python manage.py migrate <br>
5. Create a superuser: python manage.py createsuperuser <br>
6. Run the development server: python manage.py runserver <br>
### API Documentation :
https://docs.google.com/document/d/1eixo5beI3nuqinHC6SoPl5L8BHWHJJks/edit?usp=share_link&ouid=114033247930435116993&rtpof=true&sd=true
       
