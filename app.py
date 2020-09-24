from flask import Flask, render_template, request
import ftplib
import paramiko
from pythonping import ping
from scp import SCPClient

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

#   Make varibles global and set values accoridly to HTML webpage
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
    elif protocol == "SFTP":
        start = time.perf_counter()
        ftps()
        end = time.perf_counter()
        time_taken = end - start
        running_test = round(time_taken, 3)
    elif protocol == "SCP":
        start = time.perf_counter()
        scp()
        end = time.perf_counter()
        time_taken = end - start
        running_test = round(time_taken, 3)

    return render_template('home.html', filename=filename, running_test=running_test, protocol=protocol, server=server,
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


def ftps():
    print("Logging into FTPS")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username='root', password='USC2020student')
    print("Log in Successful")

    print("Starting Transfer")
    ftp_client = ssh.open_sftp()
    ftp_client.put(filename, '/root/ftpinbox/' + filename)
    ftp_client.close()
    print("Transfer complete")


def scp():
    print("Logging into SCP")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port=22, username='root', password='USC2020student')
    ssh.load_system_host_keys()
    print("Log in Successful")

    print("Starting Transfer")
    scp_put = SCPClient(ssh.get_transport())
    scp_put.put(filename, remote_path='/root/ftpinbox/'+ filename)
    print("Transfer complete")

#def ping():
#    global ping_avg
#    response_list = ping(server, size=32, count=3)
#    ping_avg = response_list.rtt_avg_ms
#    print(ping_avg)


if __name__ == '__main__':
    app.run(debug=True)
