from connect import *
from wiki_UFCEvents import *
from fighter_list import *
from config import config

def main():
    event = get_fights()[0][0]
    fights = get_fights()[1]
    fights.reverse()

    print(f'Inserting {event}')
    for fight in fights:
        print(f"""Inserting the fight: {fight}""")
    insert_fights(event, fights) 
    

def get_fights():
    fights = UFC()
    ufc_events = fights.get_all_ufc_events()
    current_event = ufc_events[0]
    current_event_fights, red_corner, blue_corner, fighters = fights.get_current_event_fights(ufc_events)

    return current_event, current_event_fights, red_corner, blue_corner, fighters


if __name__ == '__main__':
    main()



"""
Event:  
        {
            Name,
            Date
        },
Fights:
        {
            Red Corner,
            Blue Corner
        }
Fighters: 
        {
            Fighter Name
        }
"""