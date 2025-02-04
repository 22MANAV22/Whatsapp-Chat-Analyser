import streamlit as st
from matplotlib.pyplot import title
from pyexpat.errors import messages
import matplotlib.pyplot as plt
import preprocessor
import Helper
from Helper import most_busy_users, emoji_helper
from Helper import most_common_words
import seaborn as sns

st.sidebar.title("Whatsapp Chat analyser")

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)
    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words , num_media_messages,num_links = Helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1 , col2, col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        st.title('MONTHLY TIMELINE')
        timeline = Helper.monthly_timeline(selected_user,df)
        fig , ax = plt.subplots()
        ax.plot(timeline['time'] , timeline['message'] , color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title('DAILY TIMELINE')
        daily_timeline = Helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = Helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            busy_mon = Helper.monthly_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_mon.index,busy_mon.values , color = 'black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Weekly Activity Map')
        user_heatmap = Helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        if selected_user == 'Overall':
            st.title("MOST BUSIEST USER")
            x,new_df = most_busy_users(df)
            fig , ax = plt.subplots()

            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values , color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("WORD-CLOUD")
        df_wc = Helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("MOST_COMMON_WORDS")
        most_common_df = Helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)


        emoji_df = Helper.emoji_helper(selected_user,df)
        st.title("EMOJI-ANALYSIS")

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels = emoji_df[0])
            st.pyplot(fig)