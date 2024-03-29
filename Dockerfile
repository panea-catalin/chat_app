# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install required system libraries for Tkinter and X11 forwarding
RUN apt-get update && apt-get install -y --no-install-recommends \
        libtk8.6 \
        xauth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable for X11 forwarding
ENV DISPLAY=:0

# Run app.py when the container launches
CMD ["python", "app.py"]
