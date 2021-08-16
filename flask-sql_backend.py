from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

#config db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        # Fetch Form data
        user_details = request.form
        name = user_details['name']
        email = user_details['email']
        cur = mysql.connection.cursor()
        cur.execute('insert into users(name, email) values (%s, %s)', (name, email))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    res = cur.execute('select * from users')
    if res > 0:
        users = cur.fetchall()
        render_template('user.html', userDetails=users)
if __name__ == '__main__':
    app.run(debug=True)