# Use the official Python image from the Docker Hub for the build stage
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /workspace

# Copy the requirements file into the container
COPY /workspace/requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip setuptools && \
	pip install --no-cache-dir -r requirements.txt

# Use the official Python image from the Docker Hub for the final stage
FROM python:3.9-slim

# Expose port 5000 for the application
EXPOSE 5000

# Copy only the necessary files from the build stage
COPY --from=builder /workspace /workspace

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]