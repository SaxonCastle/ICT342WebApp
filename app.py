"""
This python program is written for ICT342's Industry Project - Sponsored by RetinaVisions
It is designed to test protocol compatibility for servers in multiple countries when sending large multimedia files.

This program uses Flask to host a WebApp designed in the 'home.html' template.

It uses two libraries - ftplib and paramiko - to establish ssh connections to a selected server
using a selected protocol.

Authors
@Saxon Castle
@Mitch Regan
@James Grundoff
@Daniel Walsh
"""

# Import important libraries
from flask import Flask, render_template, request
import ftplib
import paramiko
from pythonping import ping
from scp import SCPClient
import time

# Define the name of the flask application
app = Flask(__name__)

# Define variables to be defined by the user through the WebApp
# What protocol is used
protocol = ""
# What server is used
# TODO: to persist with the protocol/server selection through tests
server = ""
# How big is the packet size
packet_size = 0
# Predefined file name
# TODO: create a method to pick up the file name BUT for the ftps & scp to work it'll need to pick up the file LOCATION
filename = 'picture.CR2'
# What is the ping to the server
ping_avg = 0
# Measurement of how long it takes to complete the transfer
time_taken_to_complete = 0.0


@app.route('/')
@app.route('/home')
def home():
    """
    This is the method for the flask landing page
    :return: a html based template for flask to return.
    """
    return render_template('home.html')



@app.route("/buttonClick/", methods=['POST'])
def begin_test():
    """
    This is the method for the altered landing page
    :return: the same template as the landing page, but interacts through POST method to update the values
    """
    #   Make variables global and set values accordingly to HTML webpage
    global protocol
    protocol = request.form['protocol']

    global server
    server = request.form['server']

    global packet_size
    packet_size = request.form['packet']

    global filename
    filename = filename

    global time_taken_to_complete
    time_taken_to_complete = 0.0

    # server == server selected by user in webapp
    if server == "172.105.191.25":
        server_location = "Sydney"

    elif server == "139.162.15.145":
        server_location = "Singapore"

    elif server == "45.33.27.236":
        server_location = "Texas"
    else:
        server_location = "Unknown"

    # Sends 5, 32 bit pings to the selected server and displays the average in the WebApp
    global ping_avg
    response_list = ping(server, size=32, count=5)
    ping_avg = response_list.rtt_avg_ms

    # protocol == protocol selected by user in webapp
    if protocol == "FTP":
        start = time.perf_counter()
        ftp()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)

    elif protocol == "FTPS":
        start = time.perf_counter()
        ftps()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)

    elif protocol == "FTPS_COMPRESSED":
        start = time.perf_counter()
        ftps_compressed()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)

    elif protocol == "SCP":
        start = time.perf_counter()
        scp()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)

    elif protocol == "SCP_COMPRESSED":
        start = time.perf_counter()
        scp_compressed()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)

    return render_template('home.html',
                           filename=filename,
                           running_test=time_taken_to_complete,
                           protocol=protocol,
                           server=server,
                           server_location=server_location,
                           packet_size=packet_size,
                           ping_avg=ping_avg)


def ftp():
    """A function that uses the ftplib library to ssh into the required server
        and sends the file via plain ftp to /root/ftpinbox/
    """
    try:
        print("Logging into FTP")
        session = ftplib.FTP()
        session.connect(server, 2121)
        session.login('user', 'password')
        print("Login to " + server + " Successful")
        print("Starting Transfer")
        session.storbinary('STOR ' + filename, open(filename, 'rb'))
        session.quit()
        print("\nTransfer complete")
    except:
        print("Unable to make a FTP connection")


def ftps():
    """A function that uses the paramiko library to ssh into the required server
            and sends the file via secure ftp to /root/ftpinbox/
    """
    try:
        print("Logging into FTPS")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=22, username='root', password='USC2020student', compress=False)
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        ftp_client = ssh.open_sftp()
        ftp_client.put(filename, '/root/ftpinbox/' + filename)
        ftp_client.close()
        print("Transfer complete")
    except:
        print("Unable to make a FTPS connection")


def ftps_compressed():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via secure ftp to /root/ftpinbox/
        """
    try:
        print("Logging into FTPS with compression")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=22, username='root', password='USC2020student', compress=True)
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        ftp_client = ssh.open_sftp()
        ftp_client.put(filename, '/root/ftpinbox/' + filename)
        ftp_client.close()
        print("Transfer complete")
    except:
        print("Unable to make a FTPS connection")


def scp():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via Secure Copy Protocol (SCP) to /root/ftpinbox/
    """
    try:
        print("Logging into SCP")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=22, username='root', password='USC2020student', compress=False)
        ssh.load_system_host_keys()
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        scp_put = SCPClient(ssh.get_transport())
        scp_put.put(filename, remote_path='/root/ftpinbox/' + filename)
        print("Transfer complete")
    except:
        print("Unable to make a SCP connection")


def scp_compressed():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via Secure Copy Protocol (SCP) to /root/ftpinbox/
    """
    try:
        print("Logging into SCP with compression")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=22, username='root', password='USC2020student', compress=True)
        ssh.load_system_host_keys()
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        scp_put = SCPClient(ssh.get_transport())
        scp_put.put(filename, remote_path='/root/ftpinbox/' + filename)
        print("Transfer complete")
    except:
        print("Unable to make a SCP connection")


if __name__ == '__main__':
    app.run(debug=True)
