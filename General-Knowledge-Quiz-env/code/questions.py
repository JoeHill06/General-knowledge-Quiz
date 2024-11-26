import requests
import pandas as pd

# Fetch questions from the API
url = "https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple"  # Explicit category and difficulty
response = requests.get(url)
data = response.json()

# Extract and convert the 'results' field into a DataFrame
questions = data.get("results", [])
df = pd.DataFrame(questions)
# Ensure Pandas doesn't truncate column display
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 1000)  # Avoid line wrapping for wide DataFrames


# Filter for easy general knowledge questions
filtered_questions = df[(df["difficulty"] == "easy") & (df["category"] == "General Knowledge")]

# Display the filtered DataFrame
print(filtered_questions)