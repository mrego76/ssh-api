# Use the official fastapi image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set environment variables
ENV SSH_HOST your_ssh_host
ENV SSH_PORT your_ssh_port
ENV SSH_USERNAME your_ssh_username
ENV SSH_PASSWORD your_ssh_password
ENV FAST_API_KEY your_api_key

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
