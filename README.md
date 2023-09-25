## Project Setup


### Running the project

Simply use the command `make up` and wait for the application to run.

### Migrations

In a separate terminal tab / window use the command `make bash`.
This will open a terminal inside the container. 

run the following `python manage.py migrate` to run the migrations.

### Importing the data

Once the migrations have been completed, if you wish to load the fixture data
simply run the following `python manage.py loaddata dump.json` to load fixtures.