# Pull the latest code from GitHub
git pull

# Install new dependencies if any
poetry install

# Store credentials in environment variables
source credentials.sh

# Run database migrations if applicable
poetry run flask db upgrade

# Restart app
pkill -f 'flask run'
poetry run flask run --host=0.0.0.0 &
echo "Deployment successful!"
