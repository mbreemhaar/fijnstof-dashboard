# Fijnstof Dashboard
The Fijnstof Dashboard is a Django web application that shows data about particulate matter observations in the Netherlands.

## Installation
To install the Fijnstof Dashboard and run a development server, follow the instructions below.
1. Make sure Python 3.11 (or higher) is installed on your system.
2. Install the required Python packages.
    ```bash
    python3 -m pip install -r requirements.txt
    ```
3. Initialize the database by running the migrations.
    ```bash
    python3 manage.py migrate
    ```
4. Start the Django development server.
    ```bash
    python3 manage.py runserver
    ```
5. Navigate to http://127.0.0.1:8000/ to use the application.

## Testing
To run the tests, you can use this command:
```bash
python3 manage.py test
```
