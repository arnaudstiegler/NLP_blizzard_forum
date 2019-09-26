import urllib.request
from bs4 import BeautifulSoup
import re
import multiprocessing as mp
import logging
import json


def json_dump(filename, data, thread_name_list, url_list):
    json_data=[]

    for i in range(len(data)):
        json_data.append({
            'url': url_list[i],
            'thread_name': thread_name_list[url_list.index(data[i][0])],
            'init_post': data[i][1][0],
            'comments': data[i][1][1:]
        })
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    return


#Using more than 2 processes leads to empty request from urllib
def scrape_thread_multiprocessing(url_list, num_process=2):
    logging.basicConfig(filename='logs/scraping_thread.log',level=logging.DEBUG,
                    format='%(asctime)s %(message)s', filemode="w+") # get the root logger
    logging.info('<----- Starting multiprocessing scraping ----->')
    pool = mp.Pool(processes=num_process)
    manager = mp.Manager()

    L= manager.list()

    [pool.apply_async(scrape_thread, args=[url,L]) for url in url_list]
    pool.close()
    pool.join()

    return list(L)




def scrape_thread(thread_url, multiprocessing_bucket=None):

    searching = True
    i=1
    thread = []
    url=thread_url + '?page='
    comments = 0
    patterns = ['<br.>','<em>','<.em>','\n']
    withdrawn_flag = '(post withdrawn by author, will be automatically deleted in 24 hours unless flagged)'

    while(searching):
        try:
            fp = urllib.request.urlopen(url+str(i))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            soup = BeautifulSoup(mystr, 'html.parser')
            texts = soup.find_all('div', {'itemprop':'articleBody'})
            to_remove = []
            #comments from the server
            to_remove += list(soup.find_all('strong'))
            #for emojis
            to_remove += list(soup.find_all('img', {'class':'emoji'}))
            #for gif
            to_remove += list(soup.find_all('a'))
            #for code
            to_remove += list(soup.find_all('code'))
            #for comments on previous answers
            temp = list(soup.find_all('aside'))
            comments += len(temp)
            to_remove+=temp
            #For hashtags
            to_remove += list(soup.find_all('span', {'class':'hashtag'}))

            for elem in to_remove:
                elem.extract()
            for text in texts:

                processed_text = ''
                splitted_text = list(text.find_all('p'))
                for seq in splitted_text:
                    for elem in patterns:
                        seq = re.sub(elem,"",str(seq))
                    processed_text = processed_text + str(seq).replace('<p>','').replace('</p>','')
                if(processed_text != withdrawn_flag): #If the user has removed his comment
                    thread.append(processed_text)
            fp.close()
            i+=1
        except Exception as e:
            if(e != "HTTP Error 404: Not Found"):
                logging.warning("Exception in while loop of scrape_thread: {}".format(e))
            searching=False

    logging.info("Scraping: %s", thread_url)
    logging.info("There are %s pages for the thread", i)
    logging.info('There are %s comments for this thread',len(thread))
    logging.info('There are %s answers to comments for this tread',comments)

    ### The reason for returning both the thread and the thread url is that
    ### because of the multiprocessing, the list of threads might not be following
    ### the same order as the list of urls so we use the thread_url as an id

    if(multiprocessing_bucket is None):
        return (thread_url,thread)
    else:
        multiprocessing_bucket.append((thread_url,thread))

def retrieve_thread_url(number_thread=50):
    ###Finding the top yearly threads

    page_id = 101
    searching = True
    url='https://us.forums.blizzard.com/en/wow/c/community/general-discussion/l/top/yearly?no_subcategories=false&amp;page={}&amp;per_page=50'

    name_to_remove = ['Community', 'General Discussion', '← previous page \xa0','next page →']

    thread_name_list = []
    url_list = []

    while(searching and len(url_list) < number_thread):
        try:
            search_url = url.format(page_id)
            fp = urllib.request.urlopen(search_url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            soup = BeautifulSoup(mystr, 'html.parser')
            name_list = list(map(lambda x: x.get_text(),list(soup.find_all("span", {"itemprop":"name"}))))
            name_list = [thread_name for thread_name in name_list if thread_name not in name_to_remove]
            thread_name_list += name_list
            url_list += [meta_line['content'] for meta_line in list(soup.find_all("meta", {"itemprop":"url"}))]
            fp.close()
            page_id +=1
        except:
            searching=False

    return url_list, thread_name_list


if __name__ == '__main__':
	import pandas as pd

	#Scrape the list of urls from the website
	url_list, thread_name_list = utils.retrieve_thread_url(number_thread = 10000)
	data = utils.scrape_thread_multiprocessing(url_list,num_process=2)

	utils.json_dump('data/10000_posts.json', data, thread_name_list, url_list)
