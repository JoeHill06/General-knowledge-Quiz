from flask import Flask, render_template, request
from app import app




# Route for selecting team or player mode
@app.route('/', defaults={'solo': None})
def index(solo):
    return render_template("teamsOrPlayers.html")

@app.route('/teamsOrPlayer/<int:solo>')
@app.route('/teamsOrPlayers', defaults={'solo': None})
def teams(solo):
    if solo is None:
        return render_template("teamsOrPlayers.html")

    mode = "Team" if solo == 0 else "Player"
    teams = []  # Start with an empty list of teams
    return render_template("createTeamsPlayers.html", mode=mode, teams=teams)

# Route to handle adding a new team
@app.route('/add-team', methods=['POST'])
def add_team():
    # Get the current list of teams from the form
    existing_teams = request.form.getlist('teams')  # List of 'id:name' strings
    teams = [team.split(':') for team in existing_teams]  # Convert back to [id, name] format
    
    # Get the new team name from the form
    new_team_name = request.form.get('new_team_name', '').strip()
    if new_team_name:
        new_team_id = len(teams) + 1
        #print([str(new_team_id), new_team_name])
        teams.append([str(new_team_id), new_team_name])  # Add the new team
        print(teams)

    # Re-render the page with the updated list of teams
    return render_template("createTeamsPlayers.html", mode="Team", teams=teams)