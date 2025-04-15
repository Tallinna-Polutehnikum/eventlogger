# eventlogger
 Loendab erinevaid sündumis, tegevusi ja kogub tagasisidet. Näiteks loendab juhtkonna poole pöördumisi või kodutööde osas "meeldis või mitte" tagasisidet.

This project contains both edge server code to record events and code for physical device to trigger event on a button press.

## Setup

Set these in Azure portal or local.settings.json (for local dev):

    MYSQL_HOST
    MYSQL_USER
    MYSQL_PASSWORD
    MYSQL_DATABASE

## Devices

For physical logger device install the required packages

    ```bash
    pip install -r devices/admins-requirements.txt
    ```