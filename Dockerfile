# Use the official Python 3.9 image as the base for the container, providing the Python runtime environment.
FROM python:3.9  

# Set the working directory inside the container to /code where all subsequent commands will be executed.
WORKDIR /code  

# Copy the requirements.txt file from the host to the /code directory in the container. This file lists all the Python dependencies needed for the application.
COPY ./requirements.txt /code/requirements.txt  

# Install the Python dependencies specified in requirements.txt using pip. 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt  
# --no-cache-dir prevents pip from caching packages, reducing the image size.
# --upgrade ensures that the latest compatible versions of the dependencies are installed.
# Example: If requirements.txt contains "fastapi==0.70.0", this command will install FastAPI version 0.70.0.

# Install additional dependencies for audio processing
RUN apt-get update && apt-get install -y ffmpeg

# Copy all files from the current directory on the host machine into the /code directory inside the container. 
COPY . /code  
# This includes the application code, configuration files, and any other necessary resources.

# Define the default command to run when the container starts.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]  
# This command launches the Uvicorn server to serve the FastAPI application defined in app.py.
# --host "0.0.0.0" makes the server accessible externally.
# --port "7860" sets the port on which the application will listen.
# Example: Running this command starts the web server, allowing users to access the Telegram Voice Transcription Bot via port 7860.