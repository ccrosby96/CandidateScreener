import sqlite3

con = sqlite3.connect("screenerDB.db")

cur = con.cursor()
#cur.execute("Drop TABLE IF EXISTS hold_list")
#Creating ticker table
cur.execute(''' CREATE TABLE IF NOT EXISTS ticker
                (symbol VARCHAR PRIMARY KEY NOT NULL,
                 name VARCHAR NOT NULL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS hold_list
                (symbol VARCHAR NOT NULL,
                 date_added DATE NOT NULL DEFAULT (DATE()),
                 FOREIGN KEY (symbol) REFERENCES ticker (symbol))''')

cur.execute('''CREATE TABLE IF NOT EXISTS carrier
                (carrier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR NOT NULL,
                 address VARCHAR NOT NULL)''')

#cur.execute("DROP TABLE IF EXISTS mail_list")

cur.execute('''CREATE TABLE IF NOT EXISTS mail_list
                (persond_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name VARCHAR NOT NULL,
                 last_name VARCHAR NOT NULL,
                 phone_number VARCHAR NOT NULL,
                 carrier_id INTEGER NOT NULL,
                 FOREIGN KEY (carrier_id) REFERENCES carrier (carrier_id))''')

def hold_trigger():
    cur.execute('''CREATE TRIGGER IF NOT EXISTS update_hold_list
                        AFTER INSERT ON ticker
                    BEGIN
                        INSERT INTO hold_list (symbol) VALUES (NEW.symbol);
                    END
                     ''')
#hold_trigger()


#cur.execute('''INSERT INTO carrier (name,address) VALUES ('att', '@mms.att.net')''')
#cur.execute('''INSERT INTO carrier (name,address) VALUES ('tmobile', '@tmomail.net')''')
#cur.execute('''INSERT INTO carrier (name,address) VALUES ('verizon', '@vtext.com')''')
#cur.execute('''INSERT INTO carrier (name,address) VALUES ('sprint', '@page.nextel.com')''')

#cur.execute('''INSERT INTO mail_list (first_name,last_name,phone_number,carrier_id) VALUES ('Calvin', 'Crosby', '2033824777', 1)''')
#cur.execute('''INSERT INTO mail_list (first_name,last_name,phone_number,carrier_id) VALUES ('Richard', 'Crosby', '9179521795', 3)''')
#cur.execute('''INSERT INTO mail_list (first_name,last_name,phone_number,carrier_id) VALUES ('Eddy', 'Gozdz', '2035051230', 3)''')

for row in cur.execute('''SELECT * FROM carrier;'''):
    print(row)

for row in cur.execute('''SELECT * FROM mail_list;'''):
    print(row)

con.commit()

con.close()

carriers = {
            'att':    '@mms.att.net',
            'tmobile':' @tmomail.net',
            'verizon':  '@vtext.com',
            'sprint':   '@page.nextel.com'
        }





         


