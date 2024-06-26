# Use an official Python runtime as a parent image
FROM python:3.10.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Create the directory where your models will be stored
RUN mkdir -p /usr/src/app/available_models

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Run app.py when the container launches for the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
