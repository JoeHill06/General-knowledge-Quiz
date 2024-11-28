from flask import Flask, render_template, request, session
from app import app, questions


# Route for selecting team or player mode
@app.route('/')
def index():
    return render_template("teamsOrPlayers.html")

@app.route('/teamsOrPlayer/<int:solo>')
@app.route('/teamsOrPlayers', defaults={'solo': None})
def teams(solo=None):
    if solo is None:
        return render_template("teamsOrPlayers.html")

    mode = "Team" if solo == 0 else "Player"
    session['mode'] = mode  # Store mode in session
    session['teams'] = []  # Initialize teams in session
    return render_template("createTeamsPlayers.html", mode=mode, teams=session['teams'])

@app.route('/add-team', methods=['POST'])
def add_team():
    # Retrieve current list of teams from session
    teams = session.get('teams', [])
    mode = session.get('mode', "Team")

    # Get the new team name from the form
    new_team_name = request.form.get('new_team_name', '').strip()

    # Check for duplicate names
    if new_team_name:
        for _, name in teams:
            if new_team_name == name:
                message = f"This {mode}'s name already exists! Pick another name."
                return render_template("createTeamsPlayers.html", mode=mode, teams=teams, message=message)

        # Add the new team
        new_team_id = len(teams) + 1
        teams.append([str(new_team_id), new_team_name])
        session['teams'] = teams  # Update session with the new list

    # Re-render the page with the updated list of teams
    return render_template("createTeamsPlayers.html", mode=mode, teams=teams, categorys=questions.get_categorys())

@app.route("/start-game", methods=['POST'])
def start_game():
    # Retrieve teams and category from the session/form
    teams = session.get('teams', [])
    category = request.form.get("category")

    # Initialize the game
    current_game = questions.Game(teams, category)  # Assuming 'game' has a 'Game' class
    print(current_game.teams, current_game.category, current_game.url)
    questionSet = current_game.get_questions()
    print(questionSet)
    # Redirect or render a game page
    return render_template("gamePage.html", game=current_game)