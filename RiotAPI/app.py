from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv
from riot import Summoner
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

numberOfRows = 0
players = {}
names = []
data = ""



@app.before_request
def before_request():
    """
    Setting up the session defaults
    """
    session.setdefault('numberOfRows', 0)
    session.setdefault('players', {})
    session.setdefault('names', [])
    session.setdefault('data', "")

@app.route('/')
def home():
    return render_template('jinja.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    players = session['players']
    session['players'] = Summoner.addPlayerToDictionary(username, players)
    if not str(session['players'][username]['Level']).isnumeric():
        del session['players'][username]
        return "bad"
    print(f"Received username: {username}")
    return username

@app.route('/process', methods=['POST'])
def process_form():
    username = add_user()
    if username == "bad":
        return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data="Summoner Not Found"
                           )
    session['numberOfRows'] += 1
    session['names'].append(username)

    return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data="Summoner Found")

@app.route('/sortUser', methods=['POST'])
def sort_leaderboard():
    sorted = None
    if session['data'] == "Sorted Alphabetically":
        session['data'] = "Sorted Descending Alphabetically"
        sorted = Summoner.sortDictionary('namesRev', session['players'])
    else:
        session['data'] = "Sorted Alphabetically"
        sorted = Summoner.sortDictionary('names', session['players'])
    session['players'] = sorted
    username = next(iter(session['players']))
    session['names'] = list(session['players'].keys())
    # Return HTML content 
    return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data=session['data'])

@app.route('/sortLevel', methods=['POST'])
def sort_leaderboard_levels():
    sorted = None
    if session['data'] == "Sorted By Level":
        session['data'] = "Sorted By Level Descending"
        sorted = Summoner.sortDictionary('levelsRev', session['players'])
    else:
        session['data'] = "Sorted By Level"
        sorted = Summoner.sortDictionary('levels', session['players'])
    session['players'] = sorted
    username = next(iter(session['players']))
    session['names'] = list(session['players'].keys())
    # Return HTML content 
    return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data=session['data'])

@app.route('/sortRank', methods=['POST'])
def sort_leaderboard_rank():
    sorted = None
    if session['data'] == "Sorted By Rank":
        session['data'] = "Sorted By Rank Descending"
        sorted = Summoner.sortDictionary('rankRev', session['players'])
    else:
        session['data'] = "Sorted By Rank"
        sorted = Summoner.sortDictionary('rank', session['players'])
    session['players'] = sorted
    username = next(iter(session['players']))
    session['names'] = list(session['players'].keys())
    # Return HTML content 
    return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data=session['data'])

@app.route('/sortWin', methods=['POST'])
def sort_leaderboard_winRate():
    sorted = None
    if session['data'] == "Sorted By WinRate":
        session['data'] = "Sorted By WinRate Descending"
        sorted = Summoner.sortDictionary('winRateRev', session['players'])
    else:
        session['data'] = "Sorted By WinRate"
        sorted = Summoner.sortDictionary('winRate', session['players'])
    session['players'] = sorted
    username = next(iter(session['players']))
    session['names'] = list(session['players'].keys())
    # Return HTML content 
    return render_template('result_template.html', 
                           username=username, 
                           numberOfRows=session['numberOfRows'], 
                           players=session['players'],
                           names=session['names'],
                           data=session['data'])
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)

