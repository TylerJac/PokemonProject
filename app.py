from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = ' pokemondb.cl06m4ie8jy6.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'NinjaSexParty'
app.config['MYSQL_DB'] = 'PokemonDB'

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pokemon")
    pokemon = cur.fetchall()
    cur.close()
    return render_template('index.html', pokemon=pokemon)

# Add new Pokémon route
@app.route('/add_pokemon', methods=['POST'])
def add_pokemon():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pokemon (name, type) VALUES (%s, %s)", (name, type))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
