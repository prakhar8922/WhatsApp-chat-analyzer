# WhatsApp Chat Analyzer

## Overview
WhatsApp Chat Analyzer is a Python application that allows users to analyze group or individual WhatsApp chats. The application extracts insights such as total messages, total words, media messages, links shared, and provides visualizations like monthly and daily usage timelines, activity maps, weekly activity maps, most busy users on a bar graph, word clouds of most frequent words, and their corresponding pie charts. Additionally, the application analyzes the most frequently occurring emojis and presents them in a pie chart.

## Features

### Data Processing
The application utilizes a preprocessed file generated for machine learning purposes using Jupyter Notebook. This file contains the necessary information to perform efficient analyses.

### Statistics
- Total Messages
- Total Words
- Media Messages
- Links Shared

### Visualizations
- Monthly and Daily Usage Timeline
- Activity Map
- Weekly Activity Map
- Most Busy Users (Bar Graph)
- Wordcloud of Most Frequent Words
- Pie Chart for Most Frequent Words
- Most Frequently Occurring Emoji
- Pie Chart for Most Frequently Occurring Emoji

## Usage
1. Manually export the WhatsApp chat you want to analyze.
2. Ensure you have the preprocessed file available.
3. Run the application by executing the main script.
4. Select the exported WhatsApp group or individual chat file.
5. Explore the generated statistics and visualizations.

## Exporting WhatsApp Chats
To export a WhatsApp chat:
- Open the chat in WhatsApp.
- Tap the three dots in the top-right corner.
- Select "More" and choose "Export chat."
- Choose whether to include media files.
- Share the exported chat file to your device or cloud storage.

## Technologies Used
- Python
- Pandas
- Matplotlib
- Seaborn
- WordCloud
- Streamlit


