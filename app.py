from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from utils.whereClauseFormatter import check_clauses

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
    return render_template('index.html')

# pokemon list
@app.route('/pokemon_list')
def pokemon_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Pokemon")
    pokemon = cur.fetchall()
    cur.close()
    return render_template('pokemon_list.html', pokemon=pokemon)


# typings list
@app.route('/typings_list')
def typings_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Typings")
    typings = cur.fetchall()
    cur.close()
    return render_template('typings_list.html', typings=typings)

# abilities list
@app.route('/abilities_list')
def abilities_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Abilities")
    abilities = cur.fetchall()
    cur.close()
    return render_template('abilities_list.html', abilities=abilities)

# query DB
@app.route('/query')
def query():
    return render_template("query.html")

# typings matchup query
@app.route('/typing_matchup', methods=["GET", "POST"])
def typing_matchup():
    cur = mysql.connection.cursor()

    NationalPokedexNum = request.form.get("NationalPokedexNum")

    cur.execute(f"SELECT * FROM Pokemon WHERE NationalPokedexNum = {NationalPokedexNum}")
    pokemon = cur.fetchall()

    cur.execute(f"SELECT * FROM Typings WHERE Typing = '{pokemon[0][2]}'")
    typing_matchup = cur.fetchall()

    cur.close()
    if typing_matchup:
        return render_template('typing_matchup.html', typing_matchup=typing_matchup)
    else:
        return render_template('unsuccessful_query.html')

# abilities info query
@app.route('/ability_info', methods=["GET", "POST"])
def ability_info():
    cur = mysql.connection.cursor()

    NationalPokedexNum = request.form.get("NationalPokedexNum")

    cur.execute(f"SELECT * FROM Pokemon WHERE NationalPokedexNum = {NationalPokedexNum}")
    pokemon = cur.fetchall()

    print(f"\n\n\n{pokemon[0][3]}\n\n\n")

    cur.execute(f"SELECT * FROM Abilities WHERE Ability = '{pokemon[0][3]}'")
    ability_info = cur.fetchall()

    print(f"\n\n\n{ability_info}\n\n\n")

    cur.close()
    if ability_info:
        return render_template('ability_info.html', ability_info=ability_info)
    else:
        return render_template('unsuccessful_query.html')

@app.route('/results', methods= ['GET', 'POST'], )
def results():
    cur = mysql.connection.cursor()

    NationalPokedexNum = request.form.get("NationalPokedexNum")
    Pokemon = request.form.get("Pokemon").capitalize()
    Typing = request.form.get("Typing")
    Abilities = request.form.get("Abilities")
    BST = request.form.get("BaseStatTotal")

    query = f"""SELECT * FROM Pokemon WHERE 
                        {"NationalPokedexNum = '" + NationalPokedexNum + "'" if NationalPokedexNum else ''}
                        {check_clauses(NationalPokedexNum) + "Pokemon = '" + Pokemon + "'" if Pokemon else ''}
                        {check_clauses(NationalPokedexNum, Pokemon) + "Typing LIKE '" + Typing + "'" if Typing else ''}
                        {check_clauses(NationalPokedexNum, Pokemon, Typing) + "Abilities LIKE '" + Abilities + "'" if Abilities else ''}
                        {check_clauses(NationalPokedexNum, Pokemon, Typing, Abilities) + "BaseStatTotal > " + BST if int(BST) != 0 else ''};"""

    # I know I probably overengineered this, and I should use another method fo querying but I'm just worried about turning it in on time right now, I'll probably add things later

    results = cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return render_template('successful_query.html', results = results)

if __name__ == '__main__':
    app.run(debug=True)