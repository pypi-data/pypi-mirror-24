

# base this Image on python 3
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# this uses '-U -I --no-cache-dir' for debugging purposes only, so that it always downloads the latest version of my dependencies whenever I change them
RUN pip install -r requirements.txt -U -I --no-cache-dir

# Run app.py when the container launches
CMD ["python", "app.py"]

