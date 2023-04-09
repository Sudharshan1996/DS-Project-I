# Importing libraries and modules for the project
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
from datetime import date

# Twitter Scraping header and sidebar
st.subheader ("Twitter Scraping")
st.sidebar.title("**:blue[:wave: Hello!!!]**")
st.sidebar.header("**:blue[Kindly enter the details to begin scrape the tweets]:point_down:**")

# Setting variables to be used below
maxTweets = 1000

# Variable declaraion for user inputs
hashtag = st.sidebar.text_input("Enter the keyword or hashtag :")
tweets_count = st.sidebar.number_input("Enter the number of tweets to scrape : ", min_value = 0, max_value = 1000,step = 1)
st.sidebar.subheader(":blue[Select the date range]:calendar:")
start_date = st.sidebar.date_input("Start date (YYYY-MM-DD) : ")
end_date = st.sidebar.date_input("End date (YYYY-MM-DD) : ")
today = str(date.today())

# Creating an empty list
tweets_list = []
# Enabling the Checkbox only when the hashtag is entered
if hashtag:
    st.sidebar.checkbox("**Scrape Tweets**")
    
    # Using for loop, TwitterSearchScraper and enumerate function to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{hashtag} since:{start_date} until:{end_date}").get_items()):
        if i >= tweets_count:
            break
        tweets_list.append([tweet.date,
                            tweet.id,
                            tweet.url,
                            tweet.rawContent,
                            tweet.user.username,
                            tweet.replyCount,
                            tweet.retweetCount,
                            tweet.likeCount,
                            tweet.lang,
                            tweet.source
                           ])
else:
    st.sidebar.checkbox("**Scrape Tweets**",disabled=True)
    
# Creating DataFrame with the scraped tweets
def data_frame(data):
    return pd.DataFrame(data, columns= ['datetime', 'user_id', 'url', 'tweet_content', 'user_name', 
                                        'reply_count', 'retweet_count', 'like_count', 'language', 'source'])

# Converting DataFrame to CSV file
def convert_to_csv(c):
    return c.to_csv().encode('utf-8')

# Converting DataFrame to JSON file
def convert_to_json(j):
    return j.to_json(orient='index')  

# Creating objects for dataframe and file conversion
df = data_frame(tweets_list)
csv = convert_to_csv(df)
json = convert_to_json(df)

# BUTTON 1 - To view the DataFrame (Using Streamlit)
if st.button("View DataFrame"):
    st.success("**:blue[DataFrame Fetched Successfully]**", icon="✅")
    st.write(df)
    
 # Bringing a connection with MongoDB.Atlas and Creating a new database(DS_PROJECT1) and collection (twitterscraping)
client = pymongo.MongoClient("mongodb+srv://sudharshan:Dharshan2896@cluster0.juonexu.mongodb.net/?retryWrites=true&w=majority")
db = client.DS_PROJECT1
collection = db.twitterscraping
scrap_data = {"Scraped_word" : hashtag,
            "Scraped_date" : today,
            "Scraped_data" : df.to_dict('records')
           }

# BUTTON 2 : To upload the data to Mongo DB - Atlas  (Using Streamlit)
if st.button("Upload the data to MongoDB"):
    try:
        collection.delete_many({}) #Deleting old records from the collection
        collection.insert_one(scrap_data)
        st.success('Upload Successfully!', icon="✅")

    except:
        st.error('You cannot upload an empty dataset. Kindly enter the details in leftside menu.', icon="🚨")
        
# Header Diff Options to download the dataframe (Using Streamlit)
st.subheader("**:blue[ To download the data use the below :arrow_down:]**")
       
# BUTTON 3 - To download data as CSV
st.download_button(label= "Download data as CSV",
                   data= csv,
                   file_name= 'scraped_tweets_data.csv',
                   mime= 'text/csv'
                  )
 
# BUTTON 4 - To download data as JSON    
st.download_button(label= "Download data as JSON",
                   data= json,
                   file_name= 'scraped_tweets_data.json',
                   mime= 'text/csv'
                  )   
    
# To run the project : streamlit run twitterscraping.py

