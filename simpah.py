import tweepy
import time
import datetime

#from flask import Flask, request

consumer_key = "OWY4eJSFWaqHz8fUlk0kHDJkq"
consumer_secret = "cSgwGG2pEmLc9VpvyLB7b3vt0bXK0O2W8NTw3NTFmi4stKR2Dp"
access_token = "1231371118050570240-gHoeIg5YGCkiPpy3bRfmgIJqPkQECi"
access_token_secret = "FOorwurC6HxGNrKF7ob67joSUbgXemnb8WbFwsQceegn0"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

friend_objs = api.friends()
friends = []
for friend in friend_objs:
    friends.append(str(friend.id))
    #print(friend.id)



simp_words = { #maps simp words to their values, used in threshold calculation to determine if simping
    "coochie": 4,
    "hot": 1,
    "sexy": 2,
    "makeup": 1,
    "only fans": 5,
    "onlyfans": 5,
    "smell": 3,
    "blacked": 1,
    "pretty": 1,
    "I have": 2,
    "feelings": 3,
    "pain": 2,
    "hey": 1,
    "heyy": 2,
    "heyyy": 4,
    "cute": 1,
    "smash": 3,
    "DM": 3,
    "dm": 3,
    "piss on me": 500,
    "damn": 2,
    "I want you": 4,
    "ass": 1,
    "😩": 2,
    "🍆": 3,
    "💦": 3,
    "fart": 3
}

threshold = 7 #we will converge on good value

replyguytweets = []

while(True):

    public_tweets = api.home_timeline()


    cap = 0
    new_reply_guy_tweets = []

    #TODO: put this in an infinite loop so it gets called on a delay of like 10 minutes so it polls constantly for simps
    for tweet in public_tweets:
        if not cap < 50:
            break

        user_id = str(tweet.user.id) #who sent this tweet
        cap+=1 #we cap so we don't run out of api calls
        #print(user_id)
        if user_id not in friends: #filters this tweet to shit from people we follow
            #print(tweet.user.screen_name)
            continue
            
        id_str = str(tweet.id_str) #gets the tweet id
        replies = api.search(str(tweet.user.screen_name), since_id=str(tweet.id_str), show_user=True) #grabs the tweet's replies - CALL
        #print(len(replies))
        for reply in replies:
            if "RT @" not in reply.text and str(reply.user.id) not in friends and reply not in replyguytweets: #filters the replies on whether it is a reply and not a quote tweet or a retweet, and whether it is a reply to self
                #print(user_id)
                #print(reply.text)
                #print(reply.user.id)
                new_reply_guy_tweets.append((reply, tweet.user.screen_name, tweet.id))

    #NOW WE BLACKLIST THE SIMPS AND SEND SHOTS AT THE REPLYGUYS
    for reply in new_reply_guy_tweets:

        if reply[0] in replyguytweets:
            continue

        print("\n\n *** Checking ***")
        print(str(reply[0].text))
        #go through each simp word, compute sum
        reply_text = str(reply[0].text.lower())
        simp_score = 0
        
        for simp_word in simp_words.keys():
            if simp_word in reply_text:
                simp_score += simp_words[simp_word]
        
        if simp_score >= 5:
            print("SIMP DETECTED")
            print("REPLY GUY: " + str(reply[0].user.screen_name))
            #original_tweet_id = str(reply[0].in_reply_to_status_id)
            ts = time.time()
            api.update_status("@" + reply[0].user.screen_name + " You are a simp. Detected at: " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f'), in_reply_to_status_id=str(reply[0].id))
            api.update_status("@" + reply[1] + " I apologize for the simp known as @" + reply[0].user.screen_name + ". I would like to encourage you to begin coding at www.codecademy.com. Have a day.", in_reply_to_status_id=str(reply[2]))
        
        replyguytweets.append(reply)
        
    time.sleep(60)
        
    
    #if above threshold
        #add simp to blacklist
        #send randomized message to replyguy - 3 options

#SIMP DETECTOR
#Parameters: have a dict of words and weights
#if surpass a threshold, he is simp
#comment simp
#save @, add to list
#running list on flask page












            


