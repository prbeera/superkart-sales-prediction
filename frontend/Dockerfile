
# Use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all frontend files into the container
COPY . .

# Default backend URL (can be overridden at runtime)
ENV BACKEND_URL=http://backend:7860

# Install Python dependencies listed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
