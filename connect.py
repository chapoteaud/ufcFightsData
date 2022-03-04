import psycopg2
from config import config


def insert_fighter(fighter):
    conn = None
    fighter_id = None
    try:
       params = config()
       
       print('Connecting to Fights Database') 
       conn = psycopg2.connect(**params)

       cur = conn.cursor()

       print('Inserting fighter: {fighter}') 

       sql = f"INSERT INTO fighters(fighter_name) VALUES ($${fighter}$$) RETURNING fighter_id"
       cur.execute(sql, (fighter, ))  
       fighter_id = cur.fetchone()[0]
       conn.commit()
       
       cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('DB connection closed')

    return fighter_id

def insert_all_fighters(fighter_list):
    conn = None

    try:
       params = config()
       
       print('Connecting to Fights Database') 
       conn = psycopg2.connect(**params)

       cur = conn.cursor()

       print('Inserting fighters: ')

       for fighter in fighter_list:
           sql = f"INSERT INTO fighters(name) VALUES ($${fighter}$$)"
           cur.execute(sql, (fighter,))

       conn.commit() 
        
       print('Fighters inserted? Closing cursor. ')
       cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('DB connection closed')

def insert_events(event_list: list):
    conn = None

    try:
       params = config()
       
       print('Connecting to Fights Database') 
       conn = psycopg2.connect(**params)

       cur = conn.cursor()

       print('Inserting events: ')

       for event in event_list:
           sql = f"INSERT INTO ufc_event(event_name, event_date) VALUES ($${event[0]}$$, $${event[1]}$$)"
           cur.execute(sql, (event[0], event[1]))

       conn.commit() 
        
       print('Events inserted. Closing cursor. ')
       cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('DB connection closed')

def insert_fights(event, fights):
    for fighters in fights:
        for fighter in fighters:
            conn = None
            fighter_id = None
            try:
                params = config()
                print('Checking to see if fighter exists') 
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(f"SELECT fighter_id from fighters where fighter_name = $${fighter}$$")
                fighter_id = cur.fetchone()
                cur.close()
                if not fighter_id:
                    print(f"{fighter} was not found. Inserting fighter into database")
                    insert_fighter(fighter)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()


    for fighters in fights:
        sql = f"INSERT INTO fights(red_corner, blue_corner, event_name) values ($${fighters[0]}$$, $${fighters[1]}$$, $${event}$$)"
        conn = None
        try:
            params = config()
            print('Inserting event fight data (fighter 1 vs. fighter 2 and which event)') 
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (fighters[0], fighters[1], event))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    '''
    Look up fighter to make sure fighter exists in fighter table
        if fighter exists, insert name into fight: red or fight: blue column
        if fighter doesn't exists, populate fighter table first then insert into fight
    # insert into fights (red_corner, blue_corner, event_name) values \
    # (
    #   (select fighter_name from fighters where name in () {current_event[0]}),
    #   (select fighter_name from fighters where name = {current_event[1]}), 
    #   (select event_name from ufc_event where event_name = {fighter_name}),
    #   12.34
    # );
    '''


if __name__ == '__main__':
    insert_fighter()
    insert_all_fighters()
    insert_events()
    insert_fights()

