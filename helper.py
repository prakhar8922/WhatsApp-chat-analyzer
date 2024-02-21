from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract=URLExtract()
def fetch_stats(selected_user, df):
    # Check if a specific user is selected, filter DataFrame accordingly
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Calculate the number of messages
    num_messages = df.shape[0]

    # Extract words from each message and calculate the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Count the number of media messages
    media_mess = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Extract links from each message and calculate the total number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    # Return the calculated statistics
    return num_messages, len(words), media_mess, len(links)


def most_busy_user(df):
    # Count the number of messages per user and retrieve the top users (default: top 5)
    x = df['user'].value_counts().head()

    # Calculate the percentage of messages each user contributed to the total
    user_percentages = round((df['user'].value_counts() / df.shape[0]) * 100, 2)

    # Reset the index to make 'user' a column and rename columns for clarity
    df_percentage = user_percentages.reset_index().rename(columns={'index': 'name', 'user': 'percent'})

    # Return the top users and their message percentages
    return x, df_percentage

# Function to create a WordCloud for a selected user based on their messages in the DataFrame
def create_wc(selected_user, df):
    # Open and read the stop words file 'stop_hinglish.txt'
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # Check if a specific user is selected, filter DataFrame accordingly
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages from the DataFrame
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Define a function to remove stop words from a message
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # Create a WordCloud object with specified settings
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    # Apply the remove_stop_words function to each message in the DataFrame
    temp['message'] = temp['message'].apply(remove_stop_words)

    # Generate the WordCloud from the processed messages
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    # Return the generated WordCloud object
    return df_wc


def most_common_words(selected_user,df):
    # Open and read the stop words file 'stop_hinglish.txt'
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # Check if a specific user is selected, filter DataFrame accordingly
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages from the DataFrame
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Initialize an empty list to store words
    words = []

    # Iterate through messages, convert to lowercase, split into words, and filter out stop words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create a DataFrame with the most common 20 words and their frequencies
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    # Return the DataFrame with the most common words
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Initialize an empty list to store emojis
    emojis = []

    # Iterate through messages in the 'message' column of the DataFrame
    for message in df['message']:
        # Extend the 'emojis' list with emojis found in the message
        # The list comprehension filters characters that are emojis using the EMOJI_DATA dictionary
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA.keys()])

        # Explanation:
        # Counter(emojis): Count the occurrences of each emoji in the 'emojis' list.
        # most_common(len(Counter(emojis))): Retrieve the most common emojis along with their counts.
        # Create a DataFrame from the resulting list of tuples, where each tuple is (emoji, count).
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by year, month_num, and month, count messages, and reset index
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Format month-year strings and add a new 'time' column to the DataFrame
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by only_date and count messages, then reset index
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count the occurrences of each day_name
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    # Filter DataFrame based on the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count the occurrences of each month
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create a pivot table with rows as 'day_name', columns as 'period', and values as the count of messages
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    # Explanation:
    # - df.pivot_table(...): Create a pivot table from the DataFrame.
    # - index='day_name': Set 'day_name' as the index of the pivot table.
    # - columns='period': Set 'period' as the columns of the pivot table.
    # - values='message': Set 'message' as the values to be aggregated.
    # - aggfunc='count': Use the count function to aggregate message counts.
    # - fillna(0): Replace NaN values with 0.

    return user_heatmap
