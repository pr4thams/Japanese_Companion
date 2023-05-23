# We start from a base image with Python 3.8 installed.
FROM python:3.11

# Set a directory for the application
WORKDIR /ai_translator

# Copy all the files from the current directory to the docker container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD [ "python", "./GUI.py" ]
