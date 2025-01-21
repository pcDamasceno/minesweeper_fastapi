# Use an official Python runtime as a parent image
FROM python:3.9.20-alpine3.19
# set environment variables                         
ENV PYTHONDONTWRITEBYTECODE 1                       
ENV PYTHONUNBUFFERED 1  

# Set the working directory inside the container
WORKDIR /ing

# Copy the project code
COPY . /ing

# Expose the port the app will run on
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt &&


CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]