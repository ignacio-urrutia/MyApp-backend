#!/bin/bash

# Navigate to your project directory
cd /path/to/your/repo

# Activate the virtual environment
source myenv/bin/activate

# Pull the latest code from your GitHub repo
git pull

# Install new dependencies if any
poetry install

# Run database migrations if applicable
# Uncomment the next line if you have a database
poetry run flask db upgrade

# Restart your app
# If you're using Gunicorn and Nginx:
# systemctl restart gunicorn
# Or if you're just running the Flask app:
pkill -f 'flask run'
poetry run flask run --host=0.0.0.0 &
echo "Deployment successful!"
