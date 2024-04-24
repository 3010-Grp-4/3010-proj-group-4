# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install PostgreSQL
USER root
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Initialize the database and start PostgreSQL
RUN service postgresql start && \
    su - postgres -c "createuser --superuser appuser" && \
    su - postgres -c "createdb ecu_dash_db -O appuser"

# [OPTIONAL] Copy the backup SQL file into the container
#COPY ecu_dash_bu_sever.sql /app/
# Restore the database from the backup file
#RUN service postgresql start && \
#    su - postgres -c "psql ecu_dash_db < /app/ecu_dash_bu_sever.sql"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Switch to root user to collect static files
USER root
RUN python manage.py collectstatic --noinput

# Change ownership to appuser for all application files
RUN chown -R appuser:appuser /app

# Switch back to the non-root user
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Command to run the application using Gunicorn
CMD gunicorn 'ecu_dash.wsgi' --bind=0.0.0.0:8000
