import sqlite3
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon (if not already installed)
nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Connect to the SQLite database (replace with your actual database file path)
conn = sqlite3.connect('right.db')

# Query the feedback data (assuming your table is named 'feedback' with columns 'id' and 'comment')
query = "SELECT id, comment FROM feedback"
feedback_data = pd.read_sql(query, conn)

# Function to classify sentiment using VADER
def get_sentiment(feedback):
    sentiment_scores = sia.polarity_scores(feedback)
    compound_score = sentiment_scores['compound']
    
    # Classify sentiment based on the compound score
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Apply sentiment analysis to each feedback entry
feedback_data['sentiment'] = feedback_data['comment'].apply(get_sentiment)

# Output the results (you can also choose to print or store them)
print(feedback_data)

# Optional: Save the sentiment results back into the database
# Create a new table or update the existing one with the sentiment analysis
feedback_data[['id', 'comment', 'sentiment']].to_sql('feedback_with_sentiment', conn, if_exists='replace', index=False)

# Commit changes (important when modifying the database) and close the connection
conn.commit()
conn.close()

# Save the DataFrame to an Excel file
feedback_data[['id', 'comment', 'sentiment']].to_excel('feedback_with_sentiment.xlsx', index=False)

# Print message to confirm that the Excel file has been created
print("Sentiment analysis results saved to 'feedback_with_sentiment.xlsx'")
