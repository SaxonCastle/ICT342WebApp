from flask import Flask, render_template, request
import ftplib
from pythonping import ping
import time

app = Flask(__name__)

#Define varibles
protocol = ""
server = ""
packet_size = 0
filename = 'texttest.txt'
ping_avg = 0
running_test = 0.0


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/buttonClick/", methods=['POST'])
def begin_test():

    #Make varibles global and set values accoridly to HTML webpage
    global protocol
    protocol = request.form['protocol']
    global server
    server = request.form['server']
    global packet_size
    packet_size = request.form['packet']
    global filename
    filename = 'texttest.txt'
    global running_test
    running_test = 0.0

    if server == "172.105.191.25":
        server_location = "Sydney"

    elif server == "139.162.15.145":
        server_location = "Singapore"

    elif server == "45.33.27.236":
        server_location = "Texas"
    else:
        server_location = "Unknown"

    #ping()
    global ping_avg
    response_list = ping(server, size=32, count=3)
    ping_avg = response_list.rtt_avg_ms
    print(ping_avg)

    if protocol == "FTP":
        start = time.perf_counter()
        ftp()
        end = time.perf_counter()
        time_taken = end - start
        running_test = round(time_taken, 3)
    elif protocol == "STCP":
        start = time.perf_counter()
        stcp()
        end = time.perf_counter()
        time_taken = end - start
        running_test = round(time_taken, 3)
    elif protocol == "SCP":
        start = time.perf_counter()
        scp()
        end = time.perf_counter()
        time_taken = end - start
        running_test = round(time_taken, 3)

    return render_template('home.html', running_test=running_test, protocol=protocol, server=server,
                           server_location=server_location, packet_size=packet_size, ping_avg=ping_avg)


def ftp():
    # domain name or server ip:
    try:
        session = ftplib.FTP()
        session.connect(server, 2121)
        session.login('user', 'password')
        print("Login to " + server + " Successful")
    except:
        print("Login Failed")

    session.storbinary('STOR ' + filename, open(filename, 'rb'))
    session.quit()


def stcp():
    #do something
    print("test")


def scp():
    #do something
    print("test")

#def ping():
#    global ping_avg
#    response_list = ping(server, size=32, count=3)
#    ping_avg = response_list.rtt_avg_ms
#    print(ping_avg)


if __name__ == '__main__':
    app.run(debug=True)
