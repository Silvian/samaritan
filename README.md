# Samaritan CMA (Church Management Assistant)
[![<Samaritan>](https://circleci.com/gh/circleci/circleci-docs.svg?style=shield)](https://app.circleci.com/pipelines/github/Silvian/samaritan)

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


# Production Environment Setup

### Setting Up Nginx Proxy with HTTPS for a Dockerized Web Application on Ubuntu 22

This guide will help you set up Nginx as a reverse proxy for your web application running in a Docker container and configure HTTPS on an Ubuntu 22 server.
Ensure Docker and Nginx are installed on your Ubuntu server.

### Install Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt update
sudo apt install -y nginx

sudo docker run -d --name my-web-app -p 8000:8000 my-web-app-image
```
### Configure Nginx:

```bash
sudo nano /etc/nginx/sites-available/my-web-app

server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

sudo ln -s /etc/nginx/sites-available/my-web-app /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx
```

### Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain_or_ip

server {
    listen 80;
    server_name your_domain_or_ip;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain_or_ip;

    ssl_certificate /etc/letsencrypt/live/your_domain_or_ip/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain_or_ip/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

sudo certbot renew --dry-run
```

### Add Certbot renew to cronjob:

```bash
#certbot SSL/TLS certificates renewal runs twice a day
30 08,22 * * * certbot renew --quiet
```
