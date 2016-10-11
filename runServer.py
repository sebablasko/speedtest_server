from app import app
from app.dbmanager import innitDB

innitDB()
app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)
