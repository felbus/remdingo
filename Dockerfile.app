# Python image to use.
FROM python:3.11.2

# Set the working directory
WORKDIR /app

ENV REMDINGO_DOCKER="1"
ENV REMDINGO_ENVIRONMENT=1

COPY ./requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./remdingo /app/remdingo/

EXPOSE 5004/tcp

# Run the web service on container startup. Here we use the gunicorn webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD exec gunicorn --bind :5004 --workers 1 --threads 8 --timeout 0 remdingo.app.wsgi:app

# CMD [ "python", "-m", "remdingo.app.wsgi" ]
