from app import app
from flask import request,render_template
import dbmanager
import os

@app.route("/", methods=['GET'])
def home_get():
    return render_template('speedtest.html')

@app.route("/about", methods=['GET'])
def about_get():
    return render_template('about.html')

@app.route("/upload", methods=['POST'])
def uploadfile():
    msg = "Request via post\n sus parametros son: \n"
    print request
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
def speedtest_get(mo_size):
    if mo_size > 100:
        return 'File too big', 413
    print "download speedtest"
    return download_speedtest(mo_size)

@app.route("/speedtest/", methods=['POST'])
def speedtest_post():
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
    print request.headers
    #print dir(request)
    #pprint.pprint(request)
    b = request.data
    return "OK"

def create_random_binary_file(bytes_size):
    mbytes = bytes_size/(1024**2)
    filepath = 'app/static/speedtest_files/' + str(mbytes) + "Mo.dat"
    with open(filepath, 'wb') as fout:
        fout.write(os.urandom(bytes_size))
    return fout

@app.route("/activeServers/", methods=['get'])
def active_servers_get():
    return dbmanager.getActiveServers()

@app.route("/activeServers/", methods=['post'])
def activeServers_post():
    return dbmanager.addActiveServer(request)

@app.route("/request/")
def get_request_details():
    return str(request.environ)

@app.route("/status/")
def get_server_status():
    return "OK", 200

@app.errorhandler(404)
def page_not_found(error):
    return 'La pagina no existe', 404
