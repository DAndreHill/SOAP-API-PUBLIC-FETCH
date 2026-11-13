# SOAP-API-PUBLIC-FETCH

## Project Description:
This project is a Python Flask application that connects to a public SOAP web service using the Zeep library. The application retrieves football stadium names and allows users to search for stadiums using GET and POST requests.

## SOAP Web Service:
The Football Pool Information Service was selected because it provides stadium information that can be retrieved and validated.

WSDL URL: https://footballpool.dataaccess.eu/info.wso?WSDL

## Requirements:
* Python 3
* Flask
* Zeep
* lxml

## How to Run:
1. Install the required libraries using python -m pip install flask zeep lxml.
2. Run the application using python app.py.
3. Open http://127.0.0.1:5001/stadiums?name=MetLife to test the GET request.
4. Use the following command to test the POST request:

curl -X POST http://127.0.0.1:5001/stadiums -H "Content-Type: application/json" -d '{"name":"MetLife"}'

## Data Validation:
The application checks that stadium names are valid strings and do not exceed 100 characters. It provides custom error messages when invalid information is entered or the SOAP service fails.

## Reflection:
The 100–200-word reflection is included in reflection.md.