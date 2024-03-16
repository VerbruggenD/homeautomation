# Use the official Python image as the base image
FROM arm32v7/python:3.9

# Set the working directory in the container
WORKDIR /App

# Install gcc compiler
RUN apt-get update \
    && apt-get install -y gcc

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY /App .

# Expose the port that the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
