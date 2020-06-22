import requests
import bs4
import pandas as pd
import http.client
import logging
import re

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

http.client._MAXHEADERS = 1000

HOME_ENGLISH_URL = 'https://conjugator.reverso.net/conjugation-english.html'
HOME_SPANISH_URL = 'https://conjugator.reverso.net/conjugation-spanish.html'
HOME_PORTUGUESE_URL = 'https://conjugator.reverso.net/conjugation-portuguese.html'
HOME_FRENCH_URL = 'https://conjugator.reverso.net/conjugation-french.html'
HOME_GERMAN_URL = 'https://conjugator.reverso.net/conjugation-german.html'
HOME_ITALIAN_URL = 'https://conjugator.reverso.net/conjugation-italian.html'


VERBS_LINKS_INDEX = '.suggestion-index a'
VERB_LINKS = '.index-content a'
VERB_BLOCKS = '.word-wrap-row .wrap-three-col'
SENTENCE = 'li'


def regex(string):
    """This function receive a string and find the pattern"""
    text = string
    pattern = re.compile(r'\-(\w+)+\.html')
    regex = re.search(pattern, text)
    language = regex.group(1)
    return language
    

def join_words(sentence):
    """This function return a complete sentence, because sometimes the scraper 
    returns them without spaces"""
    if len(sentence) == 5:
        return f'{sentence[0]} {sentence[1]} {sentence[2]} {sentence[3]} {sentence[4]}'
    elif len(sentence) == 4:
        return f'{sentence[0]} {sentence[1]} {sentence[2]} {sentence[3]}'
    elif len(sentence) == 3:
        return f'{sentence[0]} {sentence[1]} {sentence[2]}'
    elif len(sentence) == 2:
        return f'{sentence[0]} {sentence[1]}'
    elif len(sentence) == 1:
        return f'{sentence[0]}'
    elif len(sentence) == 0:
        return f'NaN'


def verb_content(url):
    """This function return each verb tense and each person"""
    html_verb = parse_page(url)
    verb_blocks = html_verb.select(VERB_BLOCKS)
    len_verb_blocks = len(verb_blocks)
    counter = 0
    verb_dic = {}
    while counter < len_verb_blocks:
        try:
            sentences = []
            for block_sentence in verb_blocks[counter].select(SENTENCE):
                sentence = []
                for word in block_sentence:
                    try:
                        sentence.append(word.text)
                    except:
                        logging.warning('Sentence not found')
                sentences.append(join_words(sentence)) 
            TENSE_TITLE = verb_blocks[counter].select('.blue-box-wrap')[0].get('mobile-title')
            verb_dic[TENSE_TITLE] = sentences
            counter += 1
        except:
            logging.warning('Sentences not found')
    return verb_dic


def verbs_links(verbs_index):
    """This function return 2000 verb links"""
    verbs_list_2000 = []
    logging.info('Getting links...')
    for link_index in verbs_index:
        try:
            html_verbs_250 = parse_page(link_index)
            verb_list_250 = html_verbs_250.select(VERB_LINKS)
            for verb in verb_list_250:
                try:
                    verb_link = verb.get('href')
                    url_part = 'https://conjugator.reverso.net/'
                    verbs_list_2000.append(url_part + verb_link)
                except:
                    logging.warning('Verb link not found')
        except:
            logging,warning('Some verbs links not found ')
    logging.info('List of 2000 links obtained')
    return verbs_list_2000
        

def link_groups(html):
    """"This functions return 8 links, each link contains url with 250 links"""
    verbs_index = []
    links = html.select(VERBS_LINKS_INDEX)
    for link in links:
        try:
            verbs_index.append(link.get('href'))
        except:
            logging.warning('href not found')
    return verbs_index
    
    
def parse_page(url):
    """This function receives a url parses it, and returns a soup object"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = bs4.BeautifulSoup(response.text, 'html.parser')
            return html
        else:
            print(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run(url):
    """This function receives a URL from our variables HOME_LANGUAGE_URL,
    then starts our scraper and creates a csv file of the scraped 
    information"""
    home = parse_page(url)
    language = regex(url)
    links_index = link_groups(home)
    verbs_2000 = verbs_links(links_index)
    data = []
    counter_verbs = 0
    for verb in verbs_2000:
        try:
            data.append(verb_content(verb))
            counter_verbs += 1
            logging.info(f'{counter_verbs} : {verb}')
        except:
            logging.warning(f"We couldn't scrape: {counter_verbs} : {verb}")
    logging.info('Scraping completed')
    df = pd.DataFrame(data)
    df.to_csv(f'{language}_verbs.csv', encoding='ISO-8859-1')
    logging.info('Saved to CSV')


if __name__ == '__main__':
    run(HOME_PORTUGUESE_URL)