# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory
WORKDIR /app

# --- VIRTUAL ENV SETUP ---
# 1. Create a virtual environment in the container
# We put it in /opt/venv (standard location), but you can name it 'env' if you prefer
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# 2. "Activate" the environment
# By adding the venv/bin to the PATH, all subsequent commands (pip, python) 
# will automatically use the virtual environment.
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# --- INSTALLATION ---
# Install dependencies (This now installs INTO the virtual env because of the PATH above)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]