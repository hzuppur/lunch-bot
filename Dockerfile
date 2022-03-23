# Set up base image
FROM python:3.10-slim-bullseye
RUN pip install pipenv

# Make sure a correct locale is used
RUN apt-get update && apt-get install -y locales
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Copy configuration files
COPY ./config ./config

# Set working directory
WORKDIR /app

# Install dependencies and add to path
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY ./src .

# Run the application
CMD ["python3", "main.py"]
