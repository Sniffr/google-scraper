import sqlite3


def save_to_db(group_dict):

    print("saving to a db called mydabtabase ")
    # create a connection to the database
    conn = sqlite3.connect('mydatabase.db')

    # create a table in the database
    conn.execute('CREATE TABLE IF NOT EXISTS urls (header text, url text ,catgeory text)')

    # iterate over the dictionary and insert the values into the database
    for key, urls in group_dict.items():

        for url in urls:
            conn.execute('INSERT INTO urls (header, url,catgeory) VALUES (?, ? ,?)', (url['header'], url['url'], key))

    # save changes to the database
    conn.commit()

    print("results saved successfully")
