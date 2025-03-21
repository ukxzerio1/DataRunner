# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your local directory to the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your script inside the container
CMD ["python", "jwt_auth.py"] 
