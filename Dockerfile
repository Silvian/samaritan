FROM python:2.7

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/usr/src/app/static/

EXPOSE 8000
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application's code
COPY . /usr/src/app

# Run Django migrations
RUN python /usr/src/app/manage.py migrate

# Run the app
CMD ["./run_app.sh"]

