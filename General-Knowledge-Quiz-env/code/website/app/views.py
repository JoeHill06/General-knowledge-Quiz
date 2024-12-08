from flask import Flask, render_template, request, session, redirect
from app import app, questions

global questionSet
questionSet = []

global current_game

global current_team_index
current_team_index = 0

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

@app.route("/start-game", methods=["POST"])
def start_game():
    global questionSet, current_game

    teams = session.get('teams', [])
    category = request.form.get("category")

    if not teams or not category:
        return "Teams or category not provided. Please set up the game correctly.", 400

    current_game = questions.Game(teams, category)
    questionSet = current_game.get_questions()

    # Debugging
    print("Question Set in start_game:", questionSet)

    return redirect("/gamePage.html")


@app.route("/gamePage.html/<answer>")
@app.route("/gamePage.html", methods=["GET", "POST"])
def deliver_questions(answer=None):
    global questionSet, current_game, current_team_index

    # Initialize the current team index if it doesn't exist
    if 'current_team_index' not in globals():
        current_team_index = 0

    # Check if current_game is defined
    if 'current_game' not in globals() or current_game is None:
        return redirect("/")  # Redirect to the homepage or an appropriate error page

    if not questionSet:
        return render_template("gamePage.html", game=current_game, question=None, message="Game Over! No more questions.")

    # Handle GET requests
    if request.method == "GET":
        question = questionSet[0]
        postableQ = [question[3], questions.question_answer_mixer(question)]
        team = current_game.teams[current_team_index]
        return render_template("gamePage.html", game=current_game, question=postableQ, team=team)

    # Handle POST requests for answers
    if request.method == "POST":
        print("POST Data:", request.form)  # Debugging
        answer = request.form.get("answer")  # Get the answer from the form
        print("Answer Received:", answer)

        if not answer:
            return "No answer submitted. Please try again.", 400

        question = questionSet[0]
        postableQ = [question[3], questions.question_answer_mixer(question)]

        # Get the current team
        team = current_game.teams[current_team_index]

        # Validate the answer
        if answer == question[4]:
            team[2] += 1
            message = f"{team[1]}'s answer was correct! Your score is now {team[2]}"

            print("Answer is correct!")
        else:
            message = f"{team[1]}'s answer was incorrect! Your score is still {team[2]}"
            print(f"Answer is incorrect!")

        # Move to the next question
        questionSet = questionSet[1:]  # Remove the current question

        # Move to the next team (wrap around if needed)
        current_team_index = (current_team_index + 1) % len(current_game.teams)

        # Check if there are more questions
        if not questionSet:
            return render_template("gamePage.html", game=current_game, question=None, message=message + " Game Over!")

        # Get the next question
        next_question = questionSet[0]
        next_postableQ = [next_question[3], questions.question_answer_mixer(next_question)]

        return render_template(
            "gamePage.html",
            game=current_game,
            message=message,
            question=next_postableQ,
            team=current_game.teams[current_team_index]  # Pass the next team's turn
        )