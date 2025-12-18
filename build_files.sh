echo "Deployment started"

# 1. Install EVERYTHING from your requirements file
# This ensures google-genai, dotenv, requests, etc. are all present.
python3.12 -m pip install -r requirements.txt

# 2. Collect Static Files
python3.12 manage.py collectstatic --noinput

echo "Deployment completed"