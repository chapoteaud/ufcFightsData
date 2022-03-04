# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 17:46:10 2020

@author: chapo
"""
import requests as req
from bs4 import BeautifulSoup
html_parser = 'html.parser'
from datetime import datetime
import pandas as pd



class UFC():

    def get_all_ufc_events(self):
        '''
        Pull list of all ufc events. 
        '''
        # Get requests to get HTML data from List of UFC Events Wiki
        ufc_events = req.get("https://en.wikipedia.org/wiki/List_of_UFC_events").text
        wiki = BeautifulSoup(ufc_events, html_parser)
        
        # Extract Tables from wiki page
        events_table = wiki.find('table',{'id':'Scheduled_events'})

        # Pull all event and date tags into a list 
        scheduled_events = events_table.find_all('a')
        scheduled_dates = events_table.find_all('span')

        # Creating date objects out of date information for use later
        date_objects = []
        dates = []
        for date in scheduled_dates:
            datetime_obj = datetime.strptime(date.contents[0], '%b %d, %Y')
            date_objects.append(datetime_obj.date())

        # id = title contains all event names. Creating a list out of those tags
        events = [event.get('title') for event in scheduled_events if event.get('title') is not None]

        # Scrub list to only show UFC related events (table also contained location, date, and venue) 
        list_of_ufc_events = [event for event in events if 'UFC' in event]
        
        # Need to format dates to insert into db
        for date in date_objects:
            dates.append((date.strftime('%Y-%m-%d')))

        # Reversing the list order to show upcoming first
        list_of_ufc_events = list_of_ufc_events[::-1]
        dates = dates[::-1]

        # Scrub list because 'UFC' Apex is an arena and will be in list 
        for i in range(list_of_ufc_events.count('UFC Apex')):
            list_of_ufc_events.remove('UFC Apex')
        events_with_dates = zip(list_of_ufc_events, dates)
            
        return list(events_with_dates)

    def get_current_event_fights(self, list_of_events):
        # Add underscores to eventID to create URL to pull from current event wiki
        eventid = list_of_events[0][0].replace(" ","_")
        fight = req.get("https://en.wikipedia.org/wiki/"+ eventid).text
        fight_page = BeautifulSoup(fight, html_parser)

        
        # Extract fights from wiki event page
        fight_table = fight_page.find('table',{'class': 'toccolours'})
        fight_table_test = fight_page.find_all('table')
        

        # Create a list of fights on card. Fighter names are listed in title...some names have 'fighter' appended so removing that to add clean names to db
        scheduled_fights = fight_table.find_all('a')
        # fighters = [fight.get('title').replace('(fighter)', '').strip() for fight in scheduled_fights if fight.get('title') is not None]

        trs = fight_table.find_all('tr')

        ignore = [
            'Main card', 'Main card (ESPN+)', 'Preliminary card (ESPN+)',
            'Weight class', 'Method', 'Round', 'Notes', 
            '(c)', 
            '[a]', '[b]', '[c]', '[d]', '[e]', '[f]', '[g]', '[h]', '[i]', '[j]', '[k]', '[l]', '[m]', '[n]', '[o]',
            'vs.',
            'Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight', 'Women\'s Strawweight', 'Women\'s Flyweight', 'Women\'s Bantamweight', 'Women\'s Featherweight', 'Catchweight (129 Ib)', 'Catchweight (160 lb)',
            'Time'   
            ]
        
        fighters = [tr for tr in fight_table.stripped_strings if tr not in ignore and 'card' not in tr]
        # First fighter listed is always the red corner. DB fighter table is segmented by Blue/Red corner so created a bucket for each
        for i in range(len(fighters)): # Time complexity here is O(n**2). Might want to refactor to optmize later (if needed)
            red_corner = [fighter for fighter in fighters if fighters.index(fighter) % 2 == 0]
            blue_corner = [fighter for fighter in fighters if fighters.index(fighter) % 2 != 0]
        event_fights = zip(red_corner, blue_corner)

        return list(event_fights), red_corner, blue_corner, fighters



if __name__ == '__main__':
    fights = UFC()
    ufc_events = fights.get_all_ufc_events()
    fights.get_current_event_fights(ufc_events)
