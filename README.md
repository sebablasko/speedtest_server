# Speedtest Server

## Installation
1. Clone repository
  * `git clone https://github.com/sebablasko/speedtest_server.git`
2. Install dependecies:
  * `cd speedtest_server/`
  * `pip install -r requirements.txt`
3. Run server
  * `python server.py`

## Usage
The server is visible at `http://127.0.0.1:5000/`, visible for the whole network.

### Download Test
For request data for download speedtest, make a **GET HTTP request** to `http://127.0.0.1:5000/speedtest/<size_in_mB>`, where `<size_in_mB>` is the desired size of the data to download.

### Upload Test
To send data to check the upload speedtest, make a **POST HTTP request** to `http://127.0.0.1:5000/speedtest/`.
