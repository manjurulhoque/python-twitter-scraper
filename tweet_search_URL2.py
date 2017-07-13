# struttra: ID / LANG / USER / TEXT / DATE
# -*- coding: utf-8 -*-

import oauth2
import twitter
import csv
from operator import itemgetter
import time
from xml.dom import minidom


def search_tweets(tag, language_list, keyword, k):
    tweet_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]

    breaks = []
    if k == 0:
        tweet_list_f = open(percorso + tag + '_tweets.csv', "w")
    else:
        tweet_list_f = open(percorso + tag + '_tweets.csv', "a")
    tweet_list_w = csv.writer(tweet_list_f, delimiter='\t')

    i = 0
    n_query = 0
    # print(keyword)
    for language in language_list:

        search = api.GetSearch(term=keyword, lang=language, count=100, result_type='recent')
        n_query += 1
        for result in search:
            # try:
            if str(result.id) not in tweet_list[0]:
                # This loop does nothing... char is a local literal and won't change in the result's text
                for char in result.text:
                    if (char == '\t') or (char == '\n'):
                        char = ' '
                try:
                    tweet_id = result.id
                except:
                    tweet_id = ''
                try:
                    lang = result.user.lang
                except:
                    lang = ''
                try:
                    screen_name = result.user.screen_name.encode('ascii', 'replace')
                    screen_name = screen_name.decode("utf-8")
                except:
                    screen_name = ''
                try:
                    text = result.text.encode('ascii', 'replace')
                    text = text.decode("utf-8")
                except:
                    text = ''

                # This block *was* probably the cause of all your problems:
                try:
                    if result.in_reply_to_status_id == None:
                        in_reply_to_status_id_str = 'null'
                        reply_content = "null"
                    else:
                        in_reply_to_status_id_str = result.in_reply_to_status_id
                        repliedMessage = api.GetStatus(in_reply_to_status_id_str)
                        reply_content = repliedMessage.text
                except:
                    in_reply_to_status_id_str = 'null'
                    reply_content = "null"
                # the try part can NEVER succeed as 'in_reply_to_status_id_str'
                # isn't declared anywhere - therefore it doesn't exist and you can't call a non
                # existent object method (.encode).
                # Becuase it always fails, the except block is always reached
                # Thus the in_reply_to_status_id_str variable is declared as 'null' every time


                try:
                    datetime = result.created_at
                except:
                    datetime = ''
                try:
                    retweet_count = result.retweet_count
                except:
                    result.retweet_count = ''
                try:
                    favorite_count = result.favorite_count
                except:
                    result.favorite_count = ''
                try:
                    followers_count = result.user.followers_count
                except:
                    followers_count = ''
                try:
                    friends_count = result.user.friends_count
                except:
                    friends_count = ''
                try:
                    statuses_count = result.user.statuses_count
                except:
                    statuses_count = ''
                try:
                    time_zone = result.user.time_zone.encode('ascii', 'replace')
                    time_zone = time_zone.decode("utf-8")
                except:
                    time_zone = ''
                try:
                    created_at = result.user.created_at.encode('ascii', 'replace')
                    created_at = created_at.decode("utf-8")
                except:
                    created_at = ''
                try:
                    location = result.user.location.encode('ascii', 'replace')
                    location = location.decode("utf-8")
                except:
                    location = ''
                try:
                    description = result.user.description.encode('ascii', 'replace')
                    for char in description:
                        if (char == '\t') or (char == '\n'):
                            char = ' '
                except:
                    description = ''
                try:
                    name = result.user.name.encode('ascii', 'replace')
                except:
                    name = ''
                try:
                    source = result.source.encode('ascii', 'replace')
                except:
                    source = ''
                try:
                    urls = ''
                    for url in result.urls:
                        urls = urls + url.expanded_url + ' '
                    url_list = urls
                except:
                    url_list = ''
                try:
                    hashtags = ''
                    for hashtag in result.hashtags:
                        hashtags = hashtags + '#' + hashtag.text.encode('ascii', 'replace') + ' '
                    hashtag_list = hashtags
                except:
                    hashtag_list = ''

                tweet_list_w.writerow(
                    [tweet_id] + [lang] + [screen_name] + [text] + [str(in_reply_to_status_id_str) + "HERE!!!"] + [
                        datetime] + [retweet_count] + [favorite_count] + [followers_count] + [friends_count] + [
                        statuses_count] + [time_zone] + [created_at] + [location] + [description] + [name] + [
                        source] + [url_list] + [hashtag_list])

                i = i + 1

                # print str(result.id)+'  '+keyword.encode('ascii','replace')+'    '+ str(i)+'   '+result.created_at + " " + str(in_reply_to_status_id_str) + " " + reply_content
                # except: print 'ERROR ON RESULT #'+str(i)
        try:
            last_id = result.id
        except:
            print('ERROR ON KEYWORD ' + keyword + ' WITH LANGUAGE ' + language)
            break

        for i in range(4):
            print('Sleep -' + str(i))
            time.sleep(5)

        for page in range(1, (
                    n_results // 100)):  # /(len(keyword_list)*len(language_list))):#-len(keyword_list)*len(language_list)+1):
            print(n_query)
            try:
                search = api.GetSearch(term=keyword, lang=language, count=100, result_type='recent',
                                       max_id=last_id - 1)
            except Exception as searchErr:
                print("A failure occured during a GetSearch call. Sleeping for 30 seconds as recorvery time")
                print("Error message: " + str(searchErr.message))
                print("Moving on to next page - skipping erroneous page")
                print("Recovery Sleep - 0")
                for i in range(6):
                    time.sleep(5)
                    print("Recovery Sleep - " + str((i + 1) * 5))
                n_query += 1
                continue

            n_query += 1
            for result in search:
                try:
                    if str(result.id) not in tweet_list[0]:
                        for char in result.text:
                            if (char == '\t') or (char == '\n'):
                                char = ' '

                        try:
                            tweet_id = result.id
                        except:
                            tweet_id = ''
                        try:
                            lang = result.user.lang
                        except:
                            lang = ''
                        try:
                            screen_name = result.user.screen_name.encode('ascii', 'replace')
                            screen_name = screen_name.decode("utf-8")
                        except:
                            screen_name = ''
                        try:
                            text = result.text.encode('ascii', 'replace')
                            text = text.decode("utf-8")
                        except:
                            text = ''

                        # This block *was* probably the cause of all your problems:
                        try:
                            if (result.in_reply_to_status_id == None):
                                in_reply_to_status_id_str = 'null'
                                reply_content = "null"
                            else:
                                in_reply_to_status_id_str = result.in_reply_to_status_id
                                repliedMessage = api.GetStatus(in_reply_to_status_id_str)
                                reply_content = repliedMessage.text
                        except:
                            in_reply_to_status_id_str = 'null'
                            reply_content = "null"
                        # the try part can NEVER succeed as 'in_reply_to_status_id_str'
                        # isn't declared anywhere - therefore it doesn't exist and you can't call a non
                        # existent object method (.encode).
                        # Becuase it always fails, the except block is always reached
                        # Thus the in_reply_to_status_id_str variable is declared as 'null' every time


                        try:
                            datetime = result.created_at
                        except:
                            datetime = ''
                        try:
                            retweet_count = result.retweet_count
                        except:
                            result.retweet_count = ''
                        try:
                            favorite_count = result.favorite_count
                        except:
                            result.favorite_count = ''
                        try:
                            followers_count = result.user.followers_count
                        except:
                            followers_count = ''
                        try:
                            friends_count = result.user.friends_count
                        except:
                            friends_count = ''
                        try:
                            statuses_count = result.user.statuses_count
                        except:
                            statuses_count = ''
                        try:
                            time_zone = result.user.time_zone.encode('ascii', 'replace')
                            time_zone = time_zone.decode("utf-8")
                        except:
                            time_zone = ''
                        try:
                            created_at = result.user.created_at.encode('ascii', 'replace')
                            created_at = created_at.decode("utf-8")
                        except:
                            created_at = ''
                        try:
                            location = result.user.location.encode('ascii', 'replace')
                        except:
                            location = ''
                        try:
                            description = result.user.description.encode('ascii', 'replace')
                            for char in description:
                                if (char == '\t') or (char == '\n'):
                                    char = ' '
                        except:
                            description = ''
                        try:
                            name = result.user.name.encode('ascii', 'replace')
                        except:
                            name = ''
                        try:
                            source = result.source.encode('ascii', 'replace')
                        except:
                            source = ''
                        try:
                            urls = ''
                            for url in result.urls:
                                urls = urls + url.expanded_url + ' '
                            url_list = urls
                        except:
                            url_list = ''
                        try:
                            hashtags = ''
                            for hashtag in result.hashtags:
                                hashtags = hashtags + '#' + hashtag.text.encode('ascii', 'replace') + ' '
                            hashtag_list = hashtags
                        except:
                            hashtag_list = ''

                        tweet_list_w.writerow(
                            [tweet_id] + [lang] + [screen_name] + [text] + [in_reply_to_status_id_str] + [
                                datetime] + [retweet_count] + [favorite_count] + [followers_count] + [
                                friends_count] + [statuses_count] + [time_zone] + [created_at] + [description] + [
                                name] + [source] + [url_list] + [hashtag_list])

                        i = i + 1
                        # print str(result.id)+'  '+keyword.encode('ascii','replace')+'    '+ str(i)+'   '+result.created_at + " " + str(in_reply_to_status_id_str) + " " + reply_content
                        last_id = result.id
                except:
                    print('ERROR ON RESULT #' + str(i))
        for i in range(4):
            print("Sleep 2 -" + str(i))
            time.sleep(5)
    err = 0
    #   for i in range(0, len(tweet_list[0])):
    #        try: tweet_list_w.writerow([tweet_list[0][i]] + [tweet_list[1][i]] + [tweet_list[2][i]]+[tweet_list[3][i]] + [tweet_list[4][i]] + [tweet_list[5][i]] + [tweet_list[6][i]] + [tweet_list[7][i]] + [tweet_list[8][i]] + [tweet_list[9][i]] + [tweet_list[10][i]] + [tweet_list[11][i]] + [tweet_list[12][i]] + [tweet_list[13][i]])
    #        except: pass

    tweet_list_f.close()
    print(err)
    print(breaks)


# ************* M A I N ****************************************************************

# formato percorso: 'C:/xxxxx/yyyyy/'

percorso = ''

# il file avrà nome: tag_tweets.csv
tag = 'URL2'

# scegli se ricercare tutte le lingue inserendo ['all'] o delle specifiche lingue inserendo i relativi codici ISO (es. ['en', 'it', 'fr', 'de', 'es', 'ru']
language_list = ['en']
keyword_list = []
with open('keywords.txt', 'r') as file:
    for line in file:
        # print(line)
        keyword_list.append(line)

doc = minidom.parse("account_fiverr.xml")
accounts = doc.getElementsByTagName("account")
k = 0
for account in accounts:
    consumer_key = account.getElementsByTagName("consumerKey")[0]
    consumer_secret = account.getElementsByTagName("consumerSecret")[0]
    access_key = account.getElementsByTagName("accessToken")[0]
    access_secret = account.getElementsByTagName("accessTokenSecret")[0]
    # print(consumer_key.firstChild.data)

    # inserisci le keyword da ricercare (es. ['love', 'loving', '<3'])
    # keyword_list = [
    #     'https://www.thesun.co.u/news/3566116/jeremy-corbyn-says-he-would-surrender-to-eus-outrageous-demand-for-a-e100bn-brexit-divorce-bill-if-he-becomes-prime-minister/',
    #     'https://www.thesun.co.uk/news/3566344/shocking-moment-angry-voter-yells-in-theresa-mays-face-over-cuts-to-disability-benefits/']

    # inserisci il numero di tweet massimo desiderato; non è possibile recuperare tweet più vecchi di una settimana circa; la velocità di raccolta è 70k/h circa
    n_results = 2000000000

    CONSUMER_KEY = consumer_key.firstChild.data
    CONSUMER_SECRET = consumer_secret.firstChild.data

    ACCESS_KEY = access_key.firstChild.data
    ACCESS_SECRET = access_secret.firstChild.data

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)
    try:
        length = keyword_list.__len__()
        # print(length)
        if k < length:
            # print(keyword_list[k])
            search_tweets(tag, language_list, keyword_list[k], k)
        else:
            print("Only one account can use one keyword from the keyword list")
            break
    except Exception as e:
        print("FAILURE")
        print(e)
    print('end')
    k += 1
print('Finally end')
# _______________________________________________________________________________________
