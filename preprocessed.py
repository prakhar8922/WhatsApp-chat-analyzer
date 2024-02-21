import re
import pandas as pd

def preprocess(data):
    # f = open('WhatsApp Chat with Coding Activist Discussion.txt', 'r', encoding='utf-8')
    # data = f.read()
    # Regex pattern to match date and time patterns in the form of MM/DD/YYYY, HH:MM -
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # This pattern is designed for data files where each entry has a timestamp followed by content
    # It captures the timestamp part of each entry
    # Splitting the 'data' string using the specified regex pattern
    # This pattern is designed to match date and time patterns in the form of "MM/DD/YYYY, HH:MM -"
    # Result is a list of substrings, and [1:] is used to access content following all timestamps
    messages = re.split(pattern, data)[1:]
    # Using regex pattern to find all timestamps in the 'data' string
    # Pattern matches date and time patterns in the form of "MM/DD/YYYY, HH:MM -"
    # Result is a list of timestamps stored in the variable 'dates'
    dates = re.findall(pattern, data)
    # Creating a Pandas DataFrame from messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Converting 'message_date' column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    # Renaming 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # Initialize empty lists to store users and messages
    users = []
    messages = []

    # Iterate through 'user_message' column in the DataFrame
    for message in df['user_message']:
        # Split each message into user and content using regex pattern
        entry = re.split('([\w\W]+?):\s', message)

        # Check if user name is present, append user and message accordingly
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            # If no user name, consider it a group notification
            users.append('group_notification')
            messages.append(entry[0])

    # Update DataFrame with new 'user' and 'message' columns, and drop 'user_message'
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Initialize an empty list 'period' to store formatted time periods
    period = []

    # Iterate through rows of the DataFrame, considering columns 'day_name' and 'hour'
    for hour in df[['day_name', 'hour']]['hour']:
        # Check if the hour is 23, handle as a special case
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        # Check if the hour is 0, handle as a special case
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        # For other hours, create a formatted time period
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    # Add a new 'period' column to the DataFrame with the formatted time periods
    df['period'] = period

    # Explanation:
    # - Iterate through each row of the DataFrame using the 'hour' values from columns 'day_name' and 'hour'.
    # - Check for special cases where the hour is 23 or 0 and format the time periods accordingly.
    # - For other hours, create a formatted time period using the current hour and the next hour.
    # - Add a new 'period' column to the DataFrame with the formatted time periods.

    return df