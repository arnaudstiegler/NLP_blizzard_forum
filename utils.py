import urllib.request
from bs4 import BeautifulSoup
import re
import multiprocessing as mp
import logging


#Stream to file ?


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
            to_remove += list(soup.find_all('a', {'class':"onebox"}))
            #for comments on previous answers
            temp = list(soup.find_all('aside'))
            comments += len(temp)
            to_remove+=temp

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
        except:
            searching=False

    logging.info("Scraping: %s", thread_url)
    logging.info("There are %s pages for the thread", i)
    logging.info('There are %s comments for this thread',len(thread))
    logging.info('There are %s answers to comments for this tread',comments)
    if(multiprocessing_bucket is None):
        return thread
    else:
        multiprocessing_bucket.append(thread)

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
