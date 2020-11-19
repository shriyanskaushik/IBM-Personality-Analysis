#Importing all libraries
from tkinter import *
import praw
import tweepy
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from ibm_watson import PersonalityInsightsV3
import json
from stackapi import StackAPI
import praw
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
from PIL import ImageTk, Image

#Client details for Twitter API
consumer_key = "pZb2PizxEsB1eyMcMtPaiCKt0"
consumer_secret = "MLAIqKyYVkdykZ6eibeoWcPOX56gOgfV0vkWIVzmKEVxGQkaJu"
access_key = "3046753945-qtQ26I5KlW9Ng1LmX44OxdbJTQ8NAqjvpcDBPBE"
access_secret = "yxNsmJMzxB7WumR5u2HB9NYM5Cdftj3gbJpRSwwaxQCTw"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Client details for Personality Insight API
url1 = "https://gateway-lon.watsonplatform.net/personality-insights/api"
apikey="rRAw3UeMSph-ClMJ-LNwa0D8HHrBdHQnqHpglaa7QhKt"

service = PersonalityInsightsV3(url=url1, iam_apikey=apikey ,version="2017-10-13")

#Client details for Reddit API
reddit = praw.Reddit(client_id = "bqa8wgD7IjEhQw",
                         client_secret = "e-nSLf7A6gP1U4XOU4K15BoArM8",
                         password= "thisispassword",
                         username="donotthrowaway123",
                         user_agent="training",)

#Client details for SpeechToText API
speech_to_text = SpeechToTextV1(
    iam_apikey="2GLz9FSNQKpCutmiRtpVMG3AJQPh_DItUe89rTwy4QJC",
    url="https://gateway-lon.watsonplatform.net/speech-to-text/api"
    )


#Code for the main Window
root=Tk()
frame=Frame(root)
try:
    path = join(dirname(__file__), 'stack_howto.jpg')
    img=Image.open(path)
    img=img.resize((574, 148), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
except Exception:
    pass
#Code for functioning of "Checking Personality"
def window1():
    first_window=Toplevel(frame, width=400, height=300)

    def personality():
        #taking input from text fields
        twitteruser = e1.get()
        reddituser = e2.get()

#Code for extracting User's Input Twitter data
        tmp=[]
        b = ""
        thetweet = []
        #in case there's no input
        if len(twitteruser)==0 and len(reddituser)==0:
            c=Label(first_window).config(text="")
            c=Label(first_window, text = "Enter at least one ID")
            c.grid(row=2, columnspan=3)
        else:
            if len(twitteruser)>0:
                number_of_tweets=200
                try:
                    #calling API
                    tweets = api.user_timeline(screen_name=twitteruser, count=number_of_tweets, tweet_mode="extended")
                    tweets_for_csv = [tweet.full_text for tweet in tweets]
                    #making the tweets into coherent sentences
                    for j in tweets_for_csv:
                        thetweet = j.split()
                        thetweet.pop(-1)
                        for word in thetweet:
                            b = b + " " + str(word)
                    tmp.append(b)
                    twerror=False
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Make sure that the ID you entered is correct")
                    c.grid(row=2, columnspan=3)
                    twerror=True
            else:
                twerror=False

    #Code for extracting User's Input data
            commentvar = ""
            if len(reddituser)>0:
                try:
                    #calling Reddit's API
                    for comment in reddit.redditor(reddituser).comments.new(limit=None):
                        commentvar = commentvar + " " + str(comment.body)
                    rederror=False
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Make sure that the ID you entered is correct")
                    c.grid(row=2, columnspan=3)
                    rederror=True
            else:
                rederror=False
            #join words from both reddit and twitter
            text = str(tmp) + " " + commentvar

    #Code for the functioning of Personality Insight using Extarcted Data for Checking Personality
            if twerror==False and rederror==False:
                try:
                    #calling Personality Insight API
                    profile = service.profile(text, accept='application/json').get_result()
                    #putting the json data in dictionary
                    visd = {main5['name']:main5['percentile'] for main5 in profile['personality']}
                    #visualising the data
                    df = pd.DataFrame.from_dict(visd, orient = 'index')
                    df.reset_index(inplace=True)
                    df.columns=['Personality', 'Percentile']

                    plt.figure(figsize=(15,5))
                    sns.barplot(x="Personality", y="Percentile", data = df)
                    plt.show()
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Not enough words to scan, please enter ID of a different person")
                    c.grid(row=2, columnspan=3)

            else:
                pass
#Code for "Checking Personality" GUI Window
    a = Label(first_window,text="Twitter Username")
    a.grid(row=0, column=0)
    b = Label(first_window,text="Reddit Username")
    b.grid(row=1, column=0)
    c = Label(first_window, text="")
    c.grid(row=2, columnspan=3)
    e1 = Entry(first_window)
    e2 = Entry(first_window)

    e1.grid(row=0, column=2, pady=10, padx=15)
    e2.grid(row=1, column=2)

    Button(first_window,text='Check personality', command=personality).grid(row=3,sticky=W,pady=4,column=2,padx=20)

#Code for the functioning of "Compare two people"
def window2():
    second_window=Toplevel(frame)

#Code for "Compare two people" GUI Window excluding Buttons
    p1twitterlab=Label(second_window, text="Enter first person's Twitter username")
    p1twitterlab.grid(row=0, column=0, padx=10, pady=10)
    p1twittertf=Entry(second_window)
    p1twittertf.grid(row=0, column=1, padx=10, pady=10)
    p1redditlab=Label(second_window, text="Enter first person's Reddit username")
    p1redditlab.grid(row=1, column=0, padx=10, pady=10)
    p1reddittf=Entry(second_window)
    p1reddittf.grid(row=1, column=1, padx=10, pady=10)
    p2twitterlab=Label(second_window, text="Enter second person's Twitter username")
    p2twitterlab.grid(row=0, column=3, padx=10, pady=10)
    p2twittertf=Entry(second_window)
    p2twittertf.grid(row=0, column=4, padx=10, pady=10)
    p2redditlab=Label(second_window, text="Enter second person's Reddit username")
    p2redditlab.grid(row=1, column=3, padx=10, pady=10)
    p2reddittf=Entry(second_window)
    p2reddittf.grid(row=1, column=4, padx=10, pady=10)
    outputlabel=Label(second_window,text="")
    outputlabel.grid(row=2, column=2)
    twierror=Label(second_window, text="")
    twierror.grid(row=3, columnspan=5)

#Code for getting the User's Input data and using it for extracting Twitter and Reddit's data
    def getuserdata():
        p1twitterdata=p1twittertf.get()
        p1redditdata=p1reddittf.get()
        p2twitterdata=p2twittertf.get()
        p2redditdata=p2reddittf.get()
        #in case there's no input
        if len(p1twitterdata)==0 and len(p1redditdata)==0:
            outputlabel=Label(second_window).config(text="")
            outputlabel=Label(second_window, text = "Please enter at least one user ID for user 1")
            outputlabel.grid(row=3, column=2)
        elif len(p2twitterdata)==0 and len(p2redditdata)==0:
            outputlabel=Label(second_window).config(text="")
            outputlabel=Label(second_window, text = "Please enter at least one user ID for user 2")
            outputlabel.grid(row=3, column=2)
        else:
            number_of_tweets=200
            tmp=[]
            tmp2=[]
            b = ""
            c = ""
            thetweet = []
            if len(p1twitterdata)>0:
                number_of_tweets=200
                try:
                    #calling twitter API
                    tweets = api.user_timeline(screen_name=p1twitterdata, count=number_of_tweets, tweet_mode="extended")
                    tweets_for_csv = [tweet.full_text for tweet in tweets]
                    #making the tweets into coherent sentences
                    for j in tweets_for_csv:
                        thetweet = j.split()
                        thetweet.pop(-1)
                        for word in thetweet:
                            b = b + " " + str(word)
                    tmp.append(b)
                    twerror=False
                except Exception:
                    twierror=Label(first_window).config(text="")
                    twierror=Label(first_window, text = "Please make sure you have entered the correct ID")
                    twierror.grid(row=3, columnspan=5)
                    twerror=True
            else:
                twerror=False
            commentvar1 = ""
            if len(p1redditdata)>0:
                try:
                    #calling reddit API
                    for comment in reddit.redditor(p1redditdata).comments.new(limit=None):
                        commentvar1 = commentvar1 + " " + str(comment.body)
                    rederror=False
                except Exception:
                    twierror=Label(second_window).config(text="")
                    twierror=Label(second_window, text = "Please make sure you have entered the correct ID")
                    twierror.grid(row=3, columnspan=5)
                    rederror=True
            else:
                rederror=False
            #joining words from twitter and reddit api
            text = str(tmp) + " " + commentvar1
            if twerror==False and rederror==False:
                try:
                    #calling personality insight api
                    profile = service.profile(text, accept='application/json').get_result()
                    diffuser1 = {main5['name']:main5['percentile'] for main5 in profile['personality']}
                    p1execution=True
                except Exception:
                    twierror=Label(first_window).config(text="")
                    twierror=Label(first_window, text = "Not enough words to scan, please enter ID of a different person")
                    twierror.grid(row=3, columnspan=5)
                    p1execution=False
            else:
                p1execution=False
            if len(p2twitterdata)>0:
                number_of_tweets=200
                try:
                    #calling twitter api
                    tweets = api.user_timeline(screen_name=p2twitterdata, count=number_of_tweets, tweet_mode="extended")
                    tweets_for_csv = [tweet.full_text for tweet in tweets]
                    for j in tweets_for_csv:
                        thetweet = j.split()
                        thetweet.pop(-1)
                        for word in thetweet:
                            c = c + " " + str(word)
                    tmp2.append(c)
                    twerror=False
                except Exception:
                    twierror=Label(first_window).config(text="")
                    twierror=Label(first_window, text = "Please make sure you have entered the correct ID")
                    twierror.grid(row=3, columnspan=5)
                    twerror=True
            else:
                pass
            commentvar2 = ""
            if len(p2redditdata)>0:
                try:
                    #calling reddit api
                    for comment in reddit.redditor(p2redditdata).comments.new(limit=None):
                        commentvar2 = commentvar2 + " " + str(comment.body)
                    rederror=False
                except Exception:
                    twierror=Label(first_window).config(text="")
                    twierror=Label(first_window, text = "Please make sure you have entered the correct ID")
                    twierror.grid(row=3, columnspan=5)
                    rederror=True
            else:
                pass
            text2 = str(tmp2) + " " + commentvar2

#Code for the functioning of Personality Insight using Extarcted Data for Comparing two person's personality
            if twerror==False and rederror==False:
                try:
                    profile = service.profile(text2, accept='application/json').get_result()
                    diffuser2 = {main5['name']:main5['percentile'] for main5 in profile['personality']}
                    p2execution=True
                except Exception:
                    twierror=Label(first_window).config(text="")
                    twierror=Label(first_window, text = "Not enough words to scan, please enter ID of a different person")
                    twierror.grid(row=3, columnspan=5)
                    p2execution=False
            else:
                p2execution=False
            if p1execution==True and p2execution==True:
                list_of_keys=[i for i in diffuser1.keys()]
                difference_dictionary={}
                difference_list=[]
                #Similarity algorithm
                for j in list_of_keys:
                    if diffuser1.get(j)-diffuser2.get(j)<0:
                        new=(diffuser1.get(j)-diffuser2.get(j))*-1
                        difference_list.append(1-new)
                        difference_dictionary[j]=1-new
                    else:
                        difference_list.append(1-(diffuser1.get(j)-diffuser2.get(j)))
                        difference_dictionary[j]=1-(diffuser1.get(j)-diffuser2.get(j))
                #visualising similarity data
                df = pd.DataFrame.from_dict(difference_dictionary, orient = 'index')
                df.reset_index(inplace=True)
                df.columns=['Values', 'Similarity']
                plt.figure(figsize=(15,5))
                sns.barplot(x="Values", y="Similarity", data = df)
                plt.show()
            else:
                pass

#Code for Submit Button and it's command
    enterbutt=Button(second_window, text="Submit", command=getuserdata)
    enterbutt.grid(row=2, column=2, padx=10, pady=10)




#Code for "Checking your Interest" using Stack Overflow data
def window3():
    third_window=Toplevel(frame)

#Code for "Check your Interest" GUI Window excluding Button

    stackidlabel=Label(third_window, text="Enter Stackoverflow Id")
    stackidlabel.grid(row=0, column=0, padx=10, pady=10)
    stackidentry=Entry(third_window)
    stackidentry.grid(row=0, column=2, padx=10, pady=10)
    exceptionlabel=Label(third_window)
    exceptionlabel.grid(row=2, column=1)
    try:
        panel = Label(third_window, image = img)
        panel.grid(row=3, columnspan=3)
    except Exception:
        pass    
    def getuserdatastack():

#Code for getting User Input's data and extracting data from Stack Overflow with Try Exception Handling
        stackiddata=stackidentry.get()
        try:
            stackiddata = int(stackiddata)
            SITE = StackAPI('stackoverflow')
            Stags = SITE.fetch('/users/{}/tags'.format(stackiddata), site='stackoverflow')
            questions = SITE.fetch('/users/{}/questions'.format(stackiddata), site='stackoverflow')
            tagsnum=0
            tagslist=[]
            tagsstr=""
            #converting JSON data into coherent data
            for i in questions['items']:
                tagsnum = tagsnum+1
            for i in range(int(tagsnum)):
                a = (questions['items'][i]['tags'])
                for j in a:
                    tagslist.append(j)
            tagsdict={}
            for i in tagslist:
                tagsdict[i]=tagslist.count(i)
            newlist = sorted(tagsdict.items(), key=lambda x: x[1], reverse=True)
            var=0
            for s in newlist:
                var=var+1
            for i in range(var-5):
                newlist.pop()
            datadict = {k:v for k, v in newlist}
            #visualising your interests
            df = pd.DataFrame.from_dict(datadict, orient = 'index')
            df.reset_index(inplace=True)
            df.columns=['Personality', 'Percentile']
            plt.figure(figsize=(15,5))
            sns.barplot(x="Personality", y="Percentile", data = df)
            plt.show()
        except Exception:
                exceptionlabel=Label(third_window).config(text="")
                exceptionlabel=Label(third_window, text="Please make sure you have entered a number")
                exceptionlabel.grid(row=2, column=1)

#Code for Submit Button and it's command
    enterstackdata=Button(third_window, text="Submit", command=getuserdatastack)
    enterstackdata.grid(row=1, column=1, padx=10, pady=10)



#Code for the functioning of "Analyze via Audio"
def window4():
    fourth_window=Toplevel(frame)



#Code for "Analyze via Audio" GUI Window excluding Button
    audiolabel=Label(fourth_window, text="Please enter the file path for your audio file")
    audiolabel.grid(row=0, column=0, padx=10, pady=10)
    errortext=Label(fourth_window, text="")
    errortext.grid(row=1)
    filepath=Entry(fourth_window)
    filepath.grid(row=0, column=2, padx=10, pady=10)
    wait=Label(fourth_window, text="Please wait patiently after clicking Submit, transcribing audio will take as long as the audio is")
    wait.grid(row=2, columnspan=4)
    def transcribe():

#Code for getting the Audio file and coverting the speech into text and then analyzing it using Personality Insight with Try Exception Handling
        script=filepath.get()
        try:
            with open(script,
            'rb') as audio_file:
                prof = speech_to_text.recognize(audio_file, content_type="audio/mp3").result

            a = json.dumps(prof, indent = 4)
            z=0
            y=0
            for i in prof['results']:
                z=z+1
            trlist=[]
            for i in range(z):
                transcripts = prof['results'][i]['alternatives'][0]['transcript']
                trlist.append(transcripts)
            trstr=""
            for j in trlist:
                trstr = trstr + " " + j
            words=trstr.split()
            for k in words:
                y=y+1
            if y>100:
                #calling personality insight api
                profile = service.profile(trstr, accept='application/json').get_result()
                #putting the data into dictionaries
                visd = {main5['name']:main5['percentile'] for main5 in profile['personality']}
                vise = {main5['name']:main5['percentile'] for main5 in profile['needs']}
                visf = {main5['name']:main5['percentile'] for main5 in profile['values']}
                #visualising the data
                df = pd.DataFrame.from_dict(visd, orient = 'index')
                df.reset_index(inplace=True)
                df.columns=['Personality', 'Percentile']

                plt.figure(figsize=(15,5))
                sns.barplot(x="Personality", y="Percentile", data = df)

                df = pd.DataFrame.from_dict(visf, orient = 'index')
                df.reset_index(inplace=True)
                df.columns=['values', 'Percentile']

                plt.figure(figsize=(15,5))
                sns.barplot(x="values", y="Percentile", data = df)

                df = pd.DataFrame.from_dict(vise, orient = 'index')
                df.reset_index(inplace=True)
                df.columns=['needs', 'Percentile']

                plt.figure(figsize=(15,5))
                sns.barplot(x="needs", y="Percentile", data = df)

                plt.show()
            else:
                errortext=Label(fourth_window).config(text="")
                errortext=Label(fourth_window, text="Too few words in audio, please select a longer track")
                errortext.grid(row=2, column=1)
        except Exception:
            errortext=Label(fourth_window).config(text="")
            errortext=Label(fourth_window, text="Error in finding file, please make sure the path is correct and the format is mp3")
            errortext.grid(row=2, column=1)

#Code for Submit button and it's command
    speechtotext=Button(fourth_window, text="Submit", command=transcribe)
    speechtotext.grid(row=1, column=1, padx=10, pady=10)



#Code for the functioning of "Your friend's personality type"
def window5():
    fifth_window=Toplevel(frame)

    def personality():

#Code for getting User Input's data and using it for extracting Twitter and Reddit's data
        twitteruser = e1.get()
        reddituser = e2.get()
        tmp=[]
        b = ""
        thetweet = []
        if len(twitteruser)==0 and len(reddituser)==0:
            c=Label(fifth_window).config(text="")
            c=Label(fifth_window, text="Please enter at least one ID")
            c.grid(row=4, columnspan=3)
        else:
            if len(twitteruser)>0:
                number_of_tweets=200
                try:
                    tweets = api.user_timeline(screen_name=twitteruser, count=number_of_tweets, tweet_mode="extended")

                    tweets_for_csv = [tweet.full_text for tweet in tweets]

                    for j in tweets_for_csv:
                        thetweet = j.split()
                        thetweet.pop(-1)
                        for word in thetweet:
                            b = b + " " + str(word)
                    tmp.append(b)
                    twerror=False
                except Exception:
                    c=Label(fifth_window).config(text="")
                    c=Label(fifth_window, text="Please make sure you have entered the correct ID")
                    c.grid(row=4, columnspan=3)
                    twerror=True
            else:
                twerror=False

            commentvar = ""
            if len(reddituser)>0:
                try:
                    for comment in reddit.redditor(reddituser).comments.new(limit=None):
                        commentvar = commentvar + " " + str(comment.body)
                    rederror=False
                except Exception:
                    c=Label(fifth_window).config(text="")
                    c=Label(fifth_window, text="Please make sure you have entered the correct ID")
                    c.grid(row=4, columnspan=3)
                    rederror=True
            else:
                rederror=False

            text = str(tmp) + " " + commentvar
            if rederror==False and twerror==False:
                try:
                    profile = service.profile(text, accept='application/json').get_result()
                    visd = {main5['name']:main5['percentile'] for main5 in profile['personality']}
                    friendexec=True
                except Exception:
                    c=Label(fifth_window).config(text="")
                    c=Label(fifth_window, text="Not enough words to scan, please select a different ID")
                    c.grid(row=4, columnspan=3)
                    friendexec=False
            else:
                friendexec=False

    #Code for different personality type
            if friendexec==True:
                if visd['Openness'] >= 0.5:
                    trait1_para = """ Openness, as a personality trait defines a person’s ability to think about complex stuff in abstract ways People who score high \n in openness are comfortable in talking and thinking about concepts and hypothesis which may not be 100% true.\n They appreciate innovative possibilities and creative ideas for the future.\n
                As a person high in openness, you are open to new imaginative ideas rather than traditional practical ideas. You enjoy spending time simply \nconsidering work of art. You are well suited for jobs which require creative thinking and flexible aptitude. You like talking\n about ‘what-could-be’ rather than stress about ‘what-is’.\n\n
                """
                    ini1='O'
                elif visd['Openness'] < 0.5:
                    trait1_para = """Openness, as a personality trait defines a person’s ability to think about complex stuff in abstract ways, while people low in openness \n think straightforward. People who score low in openness prefer theories and concepts which have application in the real world.\n
                You don’t like to spend time watching art, rather you like to work on things which will have a practical effect in your life. You prefer \n to put your effort in things which will have a quantifiable positive result, like cooking, and exercising.\n You think that if something doesn’t have a practical output, it is unnecessary and wasteful.
                \n\n """
                    ini1='o'
                if visd['Conscientiousness'] >= 0.5:
                    trait2_para = """Conscientiousness refers to a person’s ability to stay determined and focused on a particular goal. People who score high \n in conscientiousness are hard and persistent workers. They take up responsibilities and use their high willpower to \n fulfill them. It’s easy for them to ignore distractions and focus on their goal.
                As a person with high conscientiousness score, you are very good at ignoring distractions and not giving in \n to impulses.You always finish what you started in a very disciplined manner. You like to stay organised and do things a certain \n way. You carefully analyse and weigh the pros and cons of every situation so that you make less mistakes
                \n\n """
                    ini2='C'

                elif visd['Conscientiousness']<0.5:
                    trait2_para = """Conscientiousness refers to a person’s ability to stay determined and focused on a particular goal. People who score less conscientiousness \n have a hard time ignoring the distractions, most of the time they give in and waste their time instead of working and being productive.\n They are spontaneous instead of planning long term. They abandon their work easily and are not very well organised in their tasks.
                As a person with low conscientiousness, you often find yourself missing deadlines and being late for appointments. Still, you don’t fret about\n time-keeping and stay relaxed. You tend to act on your impulses more than well thought out decision. For example, you are more likely \n to buy a new phone if you stumble upon it rather than comparing it with all the options available in the market.
                \n\n """
                    ini2='c'
                if visd['Extraversion']>=0.5:
                    trait3_para="""Extraversion is when a person regains their mental energy while being around people and socialising with others, and drain their energy \n when spending time alone. People who score high in extraversion are called ‘extroverts’, they are energetic, friendly, and like \n to go out. They express themselves more and are easy to talk to.
                As an extrovert, you like to be around people rather than spend time alone. The possibility of excitement and stimulation in adventurous \n situation thrills you and pushes you to pursue them. You like to be the center of attention. You are affected \n more by positive emotions than the average person.
                \n\n """
                    ini3='E'
                elif visd['Extraversion']<0.5:
                    trait3_para="""Opposite of extraversion, introversion is a personality trait in which people regain their energy by spending time alone and drain it by \n socialising with other people. Introverts are reserved and calm. They can be easily overwhelmed by packed environment.
                You, as an introvert, tend to feel drained after socialising. You prefer to spend time alone, reading a book or watching a movie, or just \n enjoying your own thoughts. You prefer to listen than talk, and you don’t talk very much with your peers.
                \n\n """
                    ini3='e'
                if visd['Agreeableness']>=0.5:
                    trait4_para="""Agreeableness, as a personality trait defines a person’s altruism. They are very considerate of others, and tend to get along very well. They put \n social harmony at a greater priority than their own goals and accomplishments. They often compromise to reach \n for the sake of others.
                As an agreeable person, you think that it is very important for you to get along with others. People perceive you as a very \n friendly and helpful person. You often compromise on your behalf for the benefit of everyone else. You are generous and like to help others.\n You are someone who is trustworthy and honest
                \n\n """
                    ini4='A'
                elif visd['Agreeableness']<0.5:
                    trait4_para="""Agreeableness, as a personality trait defines a person’s altruism. They are very considerate of others, and tend to get along very well. \n People who score low in agreeableness mostly prioritise their own benefit over the harmony of society. They are competitive and try to \n pursue their own goals with little to no regards to other people around them.
                As someone low in agreeableness, you tend to give priority to achieving your own goals over rather than compromising on \n them for the sake of others. You are a good negotiator and get a good deal most of the time. Your compassion and empathy are reserved for \n those who are in your immediate social circle like friends and family.
                \n\n """
                    ini4='a'
                if visd['Emotional range']>=0.5:
                    trait5_para="""Emotional range is a personality trait which describes a person’s emotional reaction to a stressful situation. People who score high\n in emotional range are more likely to feel negative emotions like anxiety, depression, anger, stress when subjected\n to a stressful situation.
                As someone with high emotional range, you are emotionally very reactive.You are deeply affected by situations which normally would not phase \n an average person. You easily feel threatened. You sometimes find it hard to cope with stress and your ability to think clearly becomes clouded.
                \n\n """
                    ini5='N'
                elif visd['Emotional range']<0.5:
                    trait5_para="""Emotional range is a personality trait which describes a person’s emotional reaction to a stressful situation. People who score low in \n emotional range don’t experience negative emotions as much as a highly neurotic person.
                As someone with low emotional range, you are highly resilient and emotionally strong. You don’t find dangerous situations \n threatening. In uncertain situations, you keep working without fearing the negative consequences. You don’t feel anxious in \n situations which would make an average person anxious.
                \n\n """
                    ini5='n'

                personality_trait= "Your personality trait is " + ini1+ini2+ini3+ini4+ini5+'\n\n'+trait1_para+trait2_para+trait3_para+trait4_para+trait5_para

                c=Label(fifth_window).config(text="")
                c=Label(fifth_window, text=personality_trait)
                c.grid(row=4, columnspan=3)

                df = pd.DataFrame.from_dict(visd, orient = 'index')
                df.reset_index(inplace=True)
                df.columns=['Personality', 'Percentile']

                plt.figure(figsize=(15,5))
                sns.barplot(x="Personality", y="Percentile", data = df)
                plt.show()
            else:
                pass

#Code for "Your friend's personality type" GUI Window
    a = Label(fifth_window,text="Twitter Username").grid(row=0, column=0)
    b = Label(fifth_window,text="Reddit Username").grid(row=1, column=0)
    c = Label(fifth_window, text="")
    c.grid(row=4, columnspan=3)

    e1 = Entry(fifth_window)
    e2 = Entry(fifth_window)

    e1.grid(row=0, column=2, pady=10, padx=15)
    e2.grid(row=1, column=2)

    classify_personality=Button(fifth_window,text='Classify personality', command=personality)
    classify_personality.grid(row=3,sticky=W,pady=4,column=2,padx=20)

#Code for the main GUI Window
checkpersonality=Button(frame, text="Check Personality", command=window1)
checkpersonality.grid(row=0, column=0, padx=10, pady=10)
comparetwopeople=Button(frame, text="Compare two people", command=window2)
comparetwopeople.grid(row=0, column=1, padx=10, pady=10)
checkyourinterest=Button(frame, text="Check your interest", command=window3)
checkyourinterest.grid(row=0, column=2, padx=10, pady=10)
analyzeaudio=Button(frame, text="Analyze via audio", command=window4)
analyzeaudio.grid(row=0, column=3, padx=10, pady=10)
friendspersonalitytype=Button(frame, text="Your  friend's personality type", command=window5)
friendspersonalitytype.grid(row=0, column=4, padx=10, pady=10)
cleargraph=Label(frame, text="If there are any graph open, please close them before preeceding")
cleargraph.grid(row=1,columnspan=5)
frame.pack()

root.mainloop()
