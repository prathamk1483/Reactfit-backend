echo "Deployment started"

# REMOVE the venv lines (python3.12 -m venv env / source env...) if you haven't already!

# Update this line to include djangorestframework
python3.12 -m pip install Django==5.1.6 djangorestframework sqlparse==0.5.3 tzdata==2025.1

python3.12 manage.py collectstatic --noinput

echo "Deployment completed"