
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the backend API port
EXPOSE 7860

# Start the Streamlit API using Gunicorn
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0", "--server.headless", "true"]
