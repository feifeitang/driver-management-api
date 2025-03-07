# Use the official Python 3.10 image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install the project dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the .env file to the container
COPY .env /code/.env

# Copy all files from the current directory to the container’s /app folder
COPY ./app /code/app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
