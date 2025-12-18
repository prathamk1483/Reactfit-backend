echo "Deployment started"

# REMOVE the venv lines (python3.12 -m venv env / source env...) if you haven't already!

# Update this line to include djangorestframework
python3.12 -m pip install Django==5.1.6 djangorestframework psycopg2-binary==2.9.11 groq==0.37.1

python3.12 manage.py collectstatic --noinput

echo "Deployment completed"