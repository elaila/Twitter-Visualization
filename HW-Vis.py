# Import statements
import unittest
import tweepy
import sqlite3
import twitter_info # still need this in the same directory, filled out
import matplotlib.pyplot as plt

## [PART 1]
# Finish writing the function getDayDict which takes a database cursor and returns a
# dictionary that has the days of the weeks as the keys (using "Sun", "Mon", "Tue",
# "Wed", "Thu", "Fri", "Sat") and the number of tweets on the named day as the values
#
# cur - the database cursor
def getDayDict(cur):
    dayDict = {'Sun':0, 'Mon':0, 'Tue':0, 'Wed':0, 'Thu':0, 'Fri':0, 'Sat':0}
    cur.execute(''' SELECT time_posted FROM Tweets''')
    for tweet in cur:
        day_of_week = tweet[0].split(' ')[0]
        dayDict[day_of_week] = dayDict.get(day_of_week) + 1
    cur.close()
    return dayDict


## [Part 2]
# Finish writing the function drawBarChart which takes the dictionary and draws a bar
# chart with the days of the week on the x axis and the number of tweets on the named day on
# the y axis.  The chart must have an x label, y label, and title.  Save the chart to
# "bar.png" and submit it on canvas.
#
# dayDict - a dictionary with the days of the week and the number of tweets per day
def drawBarChart(dayDict):

    plt.xlabel('Days of the Week')
    plt.ylabel('Number of Tweets')
    plt.title('Number of Tweets per Days of the Week Bar Chart')

    xvals = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    yvals = [dayDict['Sun'], dayDict['Mon'], dayDict['Tue'], dayDict['Wed'], dayDict['Thu'], dayDict['Fri'], dayDict['Sat']]

    plt.bar(xvals, yvals)
    plt.show()

## [Part 3]
## Create unittests to test the function
# Finish writing the unittests.  Write the setUp function which will create the database connection
# to 'tweets.sqlite' and the cursor.  Write the tearDown function which closes the database connection.
# Write the test_getDayDict function to test getDayDict by comparing the returned dictionary to the
# expected value.  Also call drawBarChart in test_getDayDict.
class TestHW10(unittest.TestCase):
    def setUp(self):
        consumer_key = twitter_info.consumer_key
        consumer_secret = twitter_info.consumer_secret
        access_token = twitter_info.access_token
        access_token_secret = twitter_info.access_token_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        self.conn = sqlite3.connect('tweets.sqlite')
        self.cur = self.conn.cursor()

    def test_getDayDict(self):
        strDict = getDayDict(self.cur)
        self.assertEqual(strDict['Tue'], 77)
        drawBarChart(strDict)

    def tearDown(self):
        self.conn.close()

# run the main method
if __name__ == "__main__":
    unittest.main(verbosity=2)
