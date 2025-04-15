import json
import logging
import azure.functions as func
import mysql.connector
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('EventLogger triggered.')

    # Extract from query parameters
    event = req.params.get('event')
    user = req.params.get('user')
    extra = req.params.get('extra', None)

    try:
        # Try reading JSON body if any field is missing
        req_body = req.get_json()
    except ValueError:
        req_body = {}

    if not event:
        event = req_body.get('event')
    if not user:
        user = req_body.get('user')
    if not extra:
        extra = req_body.get('extra')

    if not event or not user:
        return func.HttpResponse(
            "Missing 'event' or 'user'.",
            status_code=400
        )
    
    # Ensure 'extra' is a string
    if extra and not isinstance(extra, str):
        if isinstance(extra, dict):
            extra = json.dumps(extra)  # Convert dictionary to JSON string
        else:
            extra = str(extra)  # Convert other types to string

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        cursor = conn.cursor()

        # Insert event
        cursor.execute('''
            INSERT INTO events (user, type, extra)
            VALUES (%s, %s, %s)
        ''', (user, event, extra))

        conn.commit()
        conn.close()

        return func.HttpResponse("Event recorded.", status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "Server error: " + str(e),
            status_code=500
        )
