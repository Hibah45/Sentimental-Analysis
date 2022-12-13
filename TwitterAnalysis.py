from PyQt5 import QtCore, QtGui, QtWidgets
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Ui_TwitterAnalysis(object):

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.polarities = []

    def sentimentAnalysis(self):

        try:
            kwd = self.kw.text()  #generate keywords
            nts = self.nt.text()  #number of tweets
            if kwd == "" or kwd == "null" or nts == "" or nts == "null":
                self.showMessageBox("Information", "Please fill out all fields")
            else:
                # authenticating
                consumerKey = '7zN6WvASiB5jZV2cFKQU5oR0F'
                consumerSecret = 'bKxoxxhEUMx6bk3HPcBf5sXvUf7zJfnisj2V9ObY2aDRIr6be9'
                accessToken = '1100727463011864577-vys9YeHGpK6GK2ihT5ITAC4fe5vShI'
                accessTokenSecret = '3ZJ5qF02SKG1dUL1G2M6uy7dbRIWfkd4QbLLwQ38Y4RMU'
                auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
                auth.set_access_token(accessToken, accessTokenSecret)
                api = tweepy.API(auth)

                # input for term to be searched and how many tweets to search
                searchTerm =kwd
                NoOfTerms =int(nts)

                # searching for tweets
                self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)

                # Open/create a file to append data to
                csvFile = open('result.csv', 'a')
                csvp = open('ty.csv', 'a')

                # Use csv writerpolari
                csvWriter = csv.writer(csvFile)
                csvWriter1 = csv.writer(csvp)

                # creating some variables to store info
                polarity = 0
                positive = 0
                wpositive = 0
                spositive = 0
                negative = 0
                wnegative = 0
                snegative = 0
                neutral = 0
                #print(len(self.tweets))
                # iterating through tweets fetched
                for tweet in self.tweets:
                    # Append to temp so that we can store in csv later. I use encode UTF-8
                   # print(tweet.text.encode('utf-8'))

                    # print (tweet.text.translate(non_bmp_map))    #print tweet's text

                    stopwords_set = set(stopwords.words("english"))

                    word_tokens = word_tokenize(self.cleanTweet(tweet.text))

                    filtered_sentence = [w for w in word_tokens if not w in stopwords_set]

                    filtered_sentence = []
                    for w in word_tokens:
                        if w not in stopwords_set:
                            filtered_sentence.append(w)

                    # self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                    new = ""

                    for kw in filtered_sentence:
                        new += kw + " "

                    self.tweetText.append(new)
                   # print(new)

                    analysis = TextBlob(new)
                    # print(analysis.sentiment)  # print tweet's polarity
                    polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
                    self.polarities.append(str(analysis.sentiment.polarity))

                    if (
                            analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                        neutral += 1
                    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                        wpositive += 1
                    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                        positive += 1
                    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                        spositive += 1
                    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                        wnegative += 1
                    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                        negative += 1
                    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                        snegative += 1

                # Write to csv and close csv file
                csvWriter.writerow(self.tweetText)
                csvFile.close()
                csvWriter1.writerow(self.polarities)
                csvp.close()

                # finding average of how people are reacting
                positive = self.percentage(positive, NoOfTerms)
                wpositive = self.percentage(wpositive, NoOfTerms)
                spositive = self.percentage(spositive, NoOfTerms)
                negative = self.percentage(negative, NoOfTerms)
                wnegative = self.percentage(wnegative, NoOfTerms)
                snegative = self.percentage(snegative, NoOfTerms)
                neutral = self.percentage(neutral, NoOfTerms)

                # finding average reaction
                polarity = polarity / NoOfTerms

                # printing out data
                print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
                print()
                print("General Report: ")

                if (polarity == 0):
                    print("Neutral")
                elif (polarity > 0 and polarity <= 0.3):
                    print("Weakly Positive")
                elif (polarity > 0.3 and polarity <= 0.6):
                    print("Positive")
                elif (polarity > 0.6 and polarity <= 1):
                    print("Strongly Positive")
                elif (polarity > -0.3 and polarity <= 0):
                    print("Weakly Negative")
                elif (polarity > -0.6 and polarity <= -0.3):
                    print("Negative")
                elif (polarity > -1 and polarity <= -0.6):
                    print("Strongly Negative")

                print()
                print("Detailed Report: ")
                print(str(positive) + "% people thought it was positive")
                print(str(wpositive) + "% people thought it was weakly positive")
                print(str(spositive) + "% people thought it was strongly positive")
                print(str(negative) + "% people thought it was negative")
                print(str(wnegative) + "% people thought it was weakly negative")
                print(str(snegative) + "% people thought it was strongly negative")
                print(str(neutral) + "% people thought it was neutral")

                self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                                  NoOfTerms)





        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
            print(e)
    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

        # function to calculate percentage

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                     noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(713, 585)
        Dialog.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 591, 91))
        self.label.setStyleSheet("\n"
"font: 20pt \"Franklin Gothic Heavy\";")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(80, 160, 341, 61))
        self.label_5.setStyleSheet("font: 12pt \"Franklin Gothic Heavy\";")
        self.label_5.setObjectName("label_5")
        self.kw = QtWidgets.QLineEdit(Dialog)
        self.kw.setGeometry(QtCore.QRect(80, 220, 311, 41))
        self.kw.setStyleSheet("font: 18pt \"Gabriola\";")
        self.kw.setObjectName("kw")

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(80, 300, 281, 20))
        self.label_6.setStyleSheet("font: 12pt \"Franklin Gothic Heavy\";")
        self.label_6.setObjectName("label_6")
        self.nt = QtWidgets.QLineEdit(Dialog)
        self.nt.setGeometry(QtCore.QRect(80, 330, 311, 41))
        self.nt.setObjectName("nt")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 420, 251, 41))
        self.pushButton.setStyleSheet("font: 16pt \"Franklin Gothic Heavy\";\n"
"color: rgb(170, 85, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.sentimentAnalysis)


        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(480, 190, 201, 261))
        self.label_2.setStyleSheet("image: url(../Twitter/images/tt.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sentiment Analysis "))
        self.label.setText(_translate("Dialog", "Sentiment Analysis using Twitter Dataset"))
        self.label_5.setText(_translate("Dialog", "Enter Keyword/HashTag to search about:"))
        self.label_6.setText(_translate("Dialog", "Enter how many tweets to search:"))
        self.pushButton.setText(_translate("Dialog", "Analysis"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_TwitterAnalysis()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

