from flask import Flask, render_template, request
import ftplib
import time

#domain name or server ip:
try:
    session = ftplib.FTP()
    session.connect('139.162.15.145', 2121)
    session.login('user', 'password')
    print("Login to " + str(139) + " Successful")
except:
    print("Login Failed")


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/buttonClick/", methods=['POST'])
def begin_test():
    protocol = request.form['protocol']
    server = request.form['server']
    packet_size = request.form['packet']
    running_test = 0.0


    if server == "172.105.191.25":
        server_location = "Sydney"

    elif server == "139.162.15.145":
        server_location = "Singapore"

    elif server == "45.33.27.236":
        server_location = "Texas"
    else:
        server_location = "Unknown"

    # if protocol == "":
    filename = 'texttest.txt'
    start = time.perf_counter()
    session.storbinary('STOR ' + filename, open(filename, 'rb'))
    end = time.perf_counter()
    session.quit()
    time_taken = end - start
    running_test = round(time_taken, 3)


    return render_template('home.html', running_test=running_test, protocol=protocol, server=server,
                               server_location=server_location, packet_size=packet_size)

    # elif protocol == "STCP":
    #     filename = 'texttest.txt'
    #
    # else:
    #     filename = 'texttest.txt'



if __name__ == '__main__':
    app.run(debug=True)
