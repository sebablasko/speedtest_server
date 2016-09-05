
# Create vEnv
virtualenv venv_adkweb
source venv_adkweb/bin/activate

# Install requirements
pip install -r requirements.txt

# Add external libraries
cd static
git clone https://github.com/niclabs/NetworkInformation-Library.git
cd ..

# Start Servert
python server.py
