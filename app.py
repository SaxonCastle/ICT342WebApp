from flask import Flask, render_template
import ftplib
import time

#domain name or server ip:
session = ftplib.FTP()
session.connect('45.33.27.236', 2121)
session.login('user','password')

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/buttonClick/", methods=['POST'])
def begin_test():
    filename = 'texttest.txt'
    start = time.perf_counter()
    session.storbinary('STOR '+filename, open(filename, 'rb'))
    end = time.perf_counter()
    session.quit()
    time_taken = end - start
    running_test = round(time_taken, 3)
    return render_template('home.html', running_test=running_test)


if __name__ == '__main__':
    app.run(debug=True)
