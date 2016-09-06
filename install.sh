
# Create vEnv
echo "Creating virtual environment..."
virtualenv --python=python2.7 venv_adkweb
source venv_adkweb/bin/activate
echo "OK"

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
echo "OK"

# Turn off vEnv
echo "Shutting down virtual environment..."
deactivate
echo "OK"

# Add external libraries
echo "Downloading external libraries..."
cd static
echo "NetworkInformation-Library"
git clone https://github.com/niclabs/NetworkInformation-Library.git
echo "OK"
cd ..
