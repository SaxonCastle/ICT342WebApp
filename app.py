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
import datetime
import time
from time import strftime, gmtime
import csv

# Define the name of the flask application
app = Flask(__name__)

# Define variables to be defined by the user through the WebApp
# What protocol is used
protocol = ""
# What server is used
# TODO: to persist with the protocol/server selection through tests
server = ""
server_location = ""
bulk = ""
# How big is the packet size
packet_size = 0
# Predefined file name (Only need to update it once right here, nowhere else in the program)
filename = ""
# What is the ping to the server
ping_avg = 0
# Measurement of how long it takes to complete the transfer
time_taken_to_complete = 0.0
# Set the date of the test
date = ""
# Set the current time of the test
current_time = ""


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

    global bulk
    bulk = request.form['bulktest']
    global bulk_repeat
    bulk_repeat = request.form['bulk_repeat']
    if bulk == "False":
        """
        This is the method for the altered landing page
        :return: the same template as the landing page, but interacts through POST method to update the values
        """
        #   Make variables global and set values accordingly to HTML webpage
        global protocol, time_taken_to_complete
        protocol = request.form['protocol']

        global server
        server = request.form['server']

        global date
        date = strftime("%a, %d %b %Y")

        global current_time
        current_time = strftime("%X")

        global server_location
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
            write_to_csv()

        elif protocol == "FTP_TLS":
            start = time.perf_counter()
            ftp_tls()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()

        elif protocol == "SFTP":
            start = time.perf_counter()
            sftp()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()

        elif protocol == "SFTP_COMPRESSED":
            start = time.perf_counter()
            sftp_compressed()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()

        elif protocol == "SCP":
            start = time.perf_counter()
            scp()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()

        elif protocol == "SCP_COMPRESSED":
            start = time.perf_counter()
            scp_compressed()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()

        return render_template('home.html',
                               filename=filename,
                               running_test=time_taken_to_complete,
                               protocol=protocol,
                               server=server,
                               server_location=server_location,
                               packet_size=packet_size,
                               ping_avg=ping_avg)
    if bulk == "FTP":

        #   Define variables for Sydney
        protocol = "FTP"
        date = strftime("%a, %d %b %Y")
        server = "172.105.191.25"
        server_location = "Sydney"
        response_list = ping(server, size=32, count=5)
        ping_avg = response_list.rtt_avg_ms
        # FTP
        current_time = strftime("%X")
        start = time.perf_counter()
        ftp()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)
        write_to_csv()

        #   Define variables for Singapore
        server = "139.162.15.145"
        server_location = "Singapore"
        response_list = ping(server, size=32, count=5)
        ping_avg = response_list.rtt_avg_ms
        # FTP
        current_time = strftime("%X")
        start = time.perf_counter()
        ftp()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)
        write_to_csv()

        #   Define variables for Texas
        server = "45.33.27.236"
        server_location = "Texas"
        response_list = ping(server, size=32, count=5)
        ping_avg = response_list.rtt_avg_ms
        # FTP
        current_time = strftime("%X")
        start = time.perf_counter()
        ftp()
        end = time.perf_counter()
        time_taken_to_complete = round(end - start, 3)
        write_to_csv()

        return render_template('home.html',
                               filename=filename,
                               running_test="N/A",
                               protocol="FTP",
                               server="N/A",
                               server_location="N/A",
                               packet_size="N/A",
                               ping_avg="N/A")

    if bulk == "Repeat":
        #   Define variables
        protocol = "FTP"
        date = strftime("%a, %d %b %Y")

        server = request.form['server']

        # server == server selected by user in webapp
        if server == "172.105.191.25":
            server_location = "Sydney"
        elif server == "139.162.15.145":
            server_location = "Singapore"
        elif server == "45.33.27.236":
            server_location = "Texas"
        else:
            server_location = "Unknown"

        response_list = ping(server, size=32, count=5)
        ping_avg = response_list.rtt_avg_ms

        counter = 0
        bulk_repeat = int(request.form['bulk_repeat'])

        while counter < bulk_repeat:
            start = time.perf_counter()
            ftp()
            end = time.perf_counter()
            time_taken_to_complete = round(end - start, 3)
            write_to_csv()
            counter += 1

        return render_template('home.html',
                               filename=filename,
                               running_test="N/A",
                               protocol="FTP",
                               server=server,
                               server_location=server_location,
                               packet_size="N/A",
                               ping_avg=ping_avg)


def ftp():
    """A function that uses the ftplib library to ssh into the required server
        and sends the file via plain ftp to /root/ftpinbox/
    """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into FTP")
        session = ftplib.FTP()
        session.connect(server, 2121)
        session.login('user', 'password')
        session.storbinary('STOR ' + filename, open(filename, 'rb'))
        session.quit()
        print("Transfer complete")

    except:
        print("Unable to complete using FTP connection")


def ftp_tls():
    """A function that uses the ftplib library to ssh into the required server
        and sends the file via ftp tls to /root/ftpinbox/
    """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into FTP TLS")
        session = ftplib.FTP_TLS()
        session.connect(server, 2121)
        session.sendcmd('USER user')
        session.sendcmd('Pass password')
        print("Login to " + server + " Successful")
        session.storbinary('STOR ' + filename, open(filename, 'rb'))
        session.quit()
        print("Transfer complete")

    except:
        print("Unable to complete using FTP TLS connection")


def sftp():
    """A function that uses the paramiko library to ssh into the required server
            and sends the file via secure ftp to /root/ftpinbox/
    """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into SFTP")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server,
                    port=22,
                    username='root',
                    password='USC2020student',
                    compress=False)
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        ftp_client = ssh.open_sftp()
        ftp_client.put(filename, '/root/ftpinbox/' + filename)
        ftp_client.close()
        print("Transfer complete")

    except:
        print("Unable to complete using SFTP connection")


def sftp_compressed():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via secure ftp to /root/ftpinbox/
        """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into SFTP with compression")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server,
                    port=22,
                    username='root',
                    password='USC2020student',
                    compress=True)
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        ftp_client = ssh.open_sftp()
        ftp_client.put(filename, '/root/ftpinbox/' + filename)
        ftp_client.close()
        print("Transfer complete")

    except:
        print("Unable to complete using SFTP-C connection")


def scp():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via Secure Copy Protocol (SCP) to /root/ftpinbox/
    """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into SCP")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server,
                    port=22,
                    username='root',
                    password='USC2020student',
                    compress=False)
        ssh.load_system_host_keys()
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        scp_put = SCPClient(ssh.get_transport())
        scp_put.put(filename, remote_path='/root/ftpinbox/' + filename)
        print("Transfer complete")

    except:
        print("Unable to complete using SCP connection")


def scp_compressed():
    """A function that uses the paramiko library to ssh into the required server
                and sends the file via Secure Copy Protocol (SCP) to /root/ftpinbox/
    """
    try:
        global filename
        filename = request.form['filename']

        print("Logging into SCP with compression")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server,
                    port=22,
                    username='root',
                    password='USC2020student',
                    compress=True)
        ssh.load_system_host_keys()
        print("Login to " + server + " Successful")

        print("Starting Transfer")
        scp_put = SCPClient(ssh.get_transport())
        scp_put.put(filename, remote_path='/root/ftpinbox/' + filename)
        print("Transfer complete")

    except:
        print("Unable to complete using SCP-C connection")


def write_to_csv():
    with open('results.csv', mode='a', newline='') as results_file:
        results_writer = csv.writer(results_file,
                                    delimiter=',',)

        results_writer.writerow([date, current_time, time_taken_to_complete, protocol, ping_avg, "Saxon", "Desktop", filename, server_location])


if __name__ == '__main__':
    app.run(debug=True)
