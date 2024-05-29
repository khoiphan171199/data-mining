CSCI 4502 Final Project
Lily Chen, Khoi Phan

mine_data.py: Mines Twitter data using Twitter API and stores in Redis database
load_data.py: Retrieves data from Redis database and does preprocessing, converts to Pandas dataframes, saves dataframes to CSV
visualize_data.py: Retrieves dataframes from CSV and plots them
naive_bayes: Naive bayes model from dataframes loaded from CSV
naive_bayes2: Seperate file we have for some reason for testing

read_tweet_ids.csv: CSV to keep track of which Tweets we've already read so we don't add the same Tweet we already have to our dataset
data.csv: CSV file with topic/keyword data converted to probability data
data_unconverted.csv: CSV with just topic/keyword frequency data
