import requests as req
from bs4 import BeautifulSoup
html_parser = 'html.parser'

def get_all_ufc_fighters():
    '''
    Pull list of all ufc fighters. 
    '''
    # Only pulls fighters with Wiki page due to 'fn' (fighter name) .class
    ufc_fighters = req.get("https://en.wikipedia.org/wiki/List_of_current_UFC_fighters").text
    wiki = BeautifulSoup(ufc_fighters, html_parser)
    fighters_with_wiki = wiki.find_all('span', 'fn')
    fighter_list = set([tags.get_text() for tags in fighters_with_wiki])

    # Filters down page to find fighters that don't have a wiki page. They have no class so have to break down the contents to pull the specific fighter name
    # Column header 'Name' was included in list so added in step to remove multiple 'Names' from list
    trs = (wiki.find_all('tr'))
    tds = (wiki.find_all('td'))

    fighter_list_no_wiki = []
    for tr in trs:
        if len(tr) == 18 and tr.contents[3].string is not None and tr.contents[3].string is not 'Name':
            fighter_list_no_wiki.append(tr.contents[3].string.strip('\n'))
    
    fighter_list_no_wiki_removeName = set(fighter_list_no_wiki)
    fighter_list_no_wiki_removeName.remove('Name')

    fighter_list.union(fighter_list_no_wiki_removeName)
    
    return fighter_list, fighter_list_no_wiki_removeName


if __name__ == '__main__':
    get_all_ufc_fighters()



