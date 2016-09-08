from flask import Flask,request,render_template,g
from flask.ext.cors import CORS
import datetime, os
import pprint
import sqlite3
app = Flask(__name__, static_url_path='')
CORS(app)

app.config["DEBUG"] = True


# DB
DATABASE = 'database.db'


@app.route("/", methods=['GET'])
def home_html():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload_file():
    msg = "Request via post\n sus parametros son: \n"
    print request
    print request.files['uploaded_file']
    filenombre = datetime.datetime.now().isoformat()
    f = open(filenombre, "wb")
    request.files['uploaded_file'].save(f)
    f.close()
    for k in request.form:
        msg += k+":"+request.form[k]+"\n"
    msg += "\n\n"
    msg += "Archivo guardado en " + filenombre
    return msg

@app.route("/speedtest/<int:mo_size>", methods=['GET'])
def speedtest1(mo_size):
    if mo_size > 100:
        return 'File too big', 413
    print "download speedtest"
    return download_speedtest(mo_size)


@app.route("/speedtest/", methods=['POST'])
def speedtest2():
    print "upload speedtest"
    return upload_speedtest()

def download_speedtest(mo_size):
    return get_binary_file(mo_size)

def get_binary_file(mo_size):
    filename = "speedtest_files/" + str(mo_size) + 'Mo.dat'
    print filename
    try:
        return app.send_static_file(filename)
    except:
        create_random_binary_file(mo_size * 1024 * 1024)
        return get_binary_file(mo_size)

def upload_speedtest():
    #print dir(request)
    print request.headers
    print len(request.data)
    print request.data
    #pprint.pprint(request)
    b = request.data
    return "OK"

def create_random_binary_file(bytes_size):
    mbytes = bytes_size/(1024**2)
    filepath = 'static/speedtest_files/' + str(mbytes) + "Mo.dat"
    with open(filepath, 'wb') as fout:
        fout.write(os.urandom(bytes_size))
    return fout


@app.route("/request/")
def getRequestDetails():
    return "<pre>%s</pre>" %request.__dict__
    #return msg

@app.route("/innitDB/")
def innitDB():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE hosts (ip TEXT, port INT, country TEXT, added TIMESTAMP)')
        conn.close()
    except Exception as e:
        return "ERROR"
    return "OK"

@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/activeServers/", methods=['get'])
def getActiveServers():
    hosts = g.db.execute("SELECT * FROM hosts").fetchall()
    return str(hosts)

@app.route("/activeServers/", methods=['post'])
def addActiveServer():
    try:
        ip = request.form['ip']
        port = request.form['port']
        country = request.form['country']
        timestamp = request.form['timestamp']
        print "recuperados ", ip, port, country, timestamp

        g.db.execute("INSERT INTO hosts (ip,port,country,added) VALUES (?,?,?,?)",(ip,port,country,timestamp) )
        g.db.commit()
        return "OK"
    except:
        return "Error"


@app.errorhandler(404)
def page_not_found(error):
    return 'La pagina no existe', 404

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
