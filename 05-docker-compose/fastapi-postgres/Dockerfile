# Use official os image as a parent image
FROM debian:bookworm

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment
RUN python3 -m venv venv

# Ensure the virtual environment is used by appending to the front of PATH
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file into the container in working directory
COPY ./requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the rest of the application code into the container in working directory
COPY ./main.py ./main.py
COPY ./.env ./.env

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["fastapi", "run", "main.py"]
