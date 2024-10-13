# Bynry case study: Gas Utility Software
Develop a Django application to provide consumer services for gas utilities. The application would allow customers to submit service requests online, track the status of their requests, and view their account information. 
The application would also provide customer support representatives with a tool to manage requests and provide support to customers.

## Stack
- Python (3.11)
- Django (>=4.1)
- MySQL
- UIKit (https://getuikit.com)

## Instructions to run
- Default DB is in MySQL, thus for running and migrating first time, make sure yo have XAMPP or any server configuration supporting MySQL installed, then run: `python manage.py makemigrations` and then `python manage.py migrate`
- Then run `python manage.py runserver`

## DB Instructions
- For building a case study solution, the user for the customer service representative was created in DB itself. Thus, once migrated, create a user with group ampping named csr



