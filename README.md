# Samaritan CMA (Church Management Assistant)
[![Build Status](https://travis-ci.org/Silvian/samaritan.svg?branch=master)](https://travis-ci.org/Silvian/samaritan)

This is the main development project repository for Samaritan CMA

@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3 - please read the LICENSE included.
@Contributors: Veronica Timofte & Abel Hristodor

For any issues, queries or bugs please contact me directly: silvian.dragan@gmail.com

Samaritan CMA is designed to address the long standing needs of churches and other organisations to better manage their internal administrative affairs.
This web application wishes to address the following requirements for any church organisation:

- Ability to access and view their entire up to date members list securely and accessible on the cloud anywhere in the world and on any device.
- A simple and easy way to to add members, guests, assign members to groups/organisations assign members roles, and keep track of members who have left.
- A very intuitive user interface which is mobile friendly and easily understood. Minimal training should be required to use this Web application.


# Installation Guide:

This project is dockerized so the following guide will highlight the requirements and steps needed to run in a docker environment.

Install docker and docker-compose specific to your operating system. See https://www.docker.com for more details.

git clone the project and in the project base directory create a .env file with the following inside:

```
# Database credentials

DATABASE_HOST=postgres
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
POSTGRES_HOST_AUTH_METHOD=trust

# Memcached host

MEMCACHED_HOST=memcached

# Email Host SMTP Settings

EMAIL_HOST=your.email.host
EMAIL_PORT=port
EMAIL_HOST_USER=user
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# SMS Service Settings

SMS_URL=https://textbelt.com
SMS_TOKEN=your.token
```

Inside the project base directory where docker-compose.yml file can be found, run the following commands:
*docker-compose up --build*

Once the process has finished and the postgres sql database and application are running, run the migrations and load data command inside docker as following:
*docker-compose run --rm web scripts/migrate_loaddata.sh*

This also creates a default user: *root* with password: *root*

Login to the django administration page at: http://localhost:8000/admin/ with the credentials above to verify this.

Note: you can login with the default user created here at http://localhost:8000/ or create other users via django admin panel.


# Tests:

To run the test pack simply run:
*./scripts/test.sh*
