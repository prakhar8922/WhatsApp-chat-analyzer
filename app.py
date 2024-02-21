import matplotlib.pyplot as plt
import streamlit as st
import  seaborn as sb
import helper
import preprocessed
st.sidebar.title('Whatsapp Chat Analyzer')

# Allow user to upload a file in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")

# If a file is uploaded:
if uploaded_file is not None:
    # Read the file as bytes and decode it to UTF-8
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # Preprocess the data using a function named 'preprocess' from the 'preprocessed' module
    df = preprocessed.preprocess(data)


    # Get unique user names from the 'user' column, remove 'group_notification', sort, and insert 'Overall' at the beginning
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Allow the user to select a user for analysis using a selectbox in the sidebar
    selected_user = st.sidebar.selectbox("Show analysis wrt to", user_list)

    # Check if the 'Show Analysis' button is clicked in the sidebar
    if st.sidebar.button('Show Analysis'):
        # Call the fetch_stats function from the helper module and get the statistics
        num_mess, words, media_mess, len_links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        # Create 4 columns for displaying the statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_mess)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Messages')
            st.title(media_mess)

        with col4:
            st.header('Links Shared')
            st.title(len_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()

        # Generate a heatmap using Seaborn's heatmap function
        ax = sb.heatmap(user_heatmap)

        st.pyplot(fig)

        # Check if the selected user is 'Overall'
        if selected_user == 'Overall':
            st.title('Most Busy Users')

            # Call the most_busy_user function from the helper module and get the top users and percentages
            x, new_df = helper.most_busy_user(df)

            # Create a bar chart for the top users
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Display a DataFrame with user names and their message percentages
            with col2:
                st.dataframe(new_df)

        # WordCloud
        # Display a title for the WordCloud section
        st.title("Wordcloud")

        # Call the create_wc function from the helper module to generate a WordCloud
        df_wc = helper.create_wc(selected_user, df)

        # Create subplots for displaying the WordCloud
        fig, ax = plt.subplots()

        # Display the WordCloud on the subplot
        ax.imshow(df_wc)

        # Display the subplot using st.pyplot() in Streamlit
        st.pyplot(fig)

        # Call the most_common_words function from the helper module to get the most common words DataFrame
        most_common_df = helper.most_common_words(selected_user, df)

        # Create subplots for displaying the horizontal bar chart
        fig, ax = plt.subplots()

        # Create a horizontal bar chart using the most_common_df DataFrame
        ax.barh(most_common_df[0], most_common_df[1])

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation='vertical')

        # Display a title for the section
        st.title('Most common words')

        # Display the horizontal bar chart using st.pyplot() in Streamlit
        st.pyplot(fig)

        # Call the emoji_helper function from the helper module to get the emoji analysis DataFrame
        emoji_df = helper.emoji_helper(selected_user, df)

        # Display a title for the Emoji Analysis section
        st.title("Emoji Analysis")

        # Create two columns for displaying the DataFrame and a pie chart
        col1, col2 = st.columns(2)

        # Display the emoji analysis DataFrame in the first column
        with col1:
            st.dataframe(emoji_df)

        # Create subplots for displaying a pie chart in the second column
        with col2:
            fig, ax = plt.subplots()

            # Create a pie chart using the first few rows of emoji_df DataFrame
            # emoji_df[1].head(): Extract the counts column (second column) of emoji_df and select the top rows.
            # emoji_df[0].head(): Extract the emojis column (first column) of emoji_df and select the top rows.
            # autopct="%0.2f": Display percentage labels on the pie chart with two decimal places.
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

            # Display the pie chart using st.pyplot() in Streamlit
            st.pyplot(fig)

