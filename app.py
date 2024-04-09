from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'pokemondb.cl06m4ie8jy6.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'NinjaSexParty'
app.config['MYSQL_DB'] = 'PokemonDB'

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Pokemon")
    pokemon = cur.fetchall()
    cur.close()
    return render_template('index.html', pokemon=pokemon)

@app.route('/typings_list')
def typings_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Typings")
    typings = cur.fetchall()
    cur.close()
    return render_template('typings_list.html', typings=typings)

if __name__ == '__main__':
    app.run(debug=True)