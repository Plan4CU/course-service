# The base image for python. There are countless official images.
# Alpine just sounded cool.
#
FROM python:3.11-alpine

# The directory in the container where the app will run.
#
WORKDIR /app_working

# Copy the requirements.txt file from the project directory into the working
# directory and install the requirements.
#
COPY ./requirements.txt /app_working
RUN pip install -r requirements.txt
RUN pip install fastapi[standard]

# Copy over the files.
#
COPY . .

# Expose/publish port 8000 for the container.
#
EXPOSE 8000

# Look in the code. This is an environment variable
# passed to the application.
#
ENV WHEREAMI=DOCKER

# Run the app. using fastapi run command
CMD ["fastapi", "run"]
