import requests
import pandas as pd

categories = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32
}

difficulty_levels = ["easy", "medium", "hard"]

## Returns the list of category names
def get_categorys():
    return list(categories.keys())

class Game:
    def __init__(self, teams, category, difficulty="easy"):
        # Initialize teams with scores
        self.teams = [[team[0], team[1], 0] for team in teams]
        self.category = category
        self.difficulty = difficulty

        # Generate the URL
        self.url = self.create_url()


    def create_url(self):
        """Create the OpenTDB API URL."""
        category_id = categories[self.category]  # Get category ID from the dictionary
        return f"https://opentdb.com/api.php?amount=50&category={category_id}&type=multiple"

    def get_questions(self):
        response = requests.get(self.url)
        data = response.json()
        questions = data.get("results",[])
        df = pd.DataFrame(questions)

        pd.set_option("display.max_columns", None)  # Show all columns
        pd.set_option("display.width", 1000)  # Avoid line wrapping for wide DataFrames

        questionSet = df.values.tolist()
        
        return questionSet





#response = requests.get(url)
#data = response.json()

# Extract and convert the 'results' field into a DataFrame
#questions = data.get("results", [])
#df = pd.DataFrame(questions)
# Ensure Pandas doesn't truncate column display
#pd.set_option("display.max_columns", None)  # Show all columns
#pd.set_option("display.width", 1000)  # Avoid line wrapping for wide DataFrames



# Filter for easy general knowledge questions
#iltered_questions = df[(df["difficulty"] == "easy") & (df["category"] == "General Knowledge")]

# Display the filtered DataFrame
#print(filtered_questions)