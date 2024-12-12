# Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY ./app /app/app
COPY requirements.txt /app/requirements.txt

# Copy the model file
COPY ./app/sign_language_model_v4_newdata_only.keras /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]