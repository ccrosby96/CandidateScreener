import sqlite3
from textwrap import wrap
import traceback
import sys
import pandas as pd
from messenger import Person,Messenger
from datetime import date, datetime, time, timedelta
class dbInterface():
    '''This class provides creates a nice wrapper around a backend sqlite database for
        the stock screener. Upon instantiation, a dbInterface object has callable methods
         that can be used to easily connect the SQL databse with the rest of the application.
        '''
    def __init__(self, dbName = "screenerDB.db") -> None:
        self.con = self.create_db_connection(dbName)
        self.cursor = self.get_cursor()
        self.curr_date = datetime.today()
    
    def create_db_connection(self,db_name):
        '''This method establishes a connection with the Sqlite database.
            If the connection is successful, a Connection object is returned.'''
        connection = None
        try:
            connection = sqlite3.connect(db_name)
            print("Database connection successful")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

        return connection
    def get_cursor(self):
        '''get_cursor returns a cursor object to be used in querying and
            manipulating the Sqlite database.'''
        try:
            cursor = self.con.cursor()
    
        except sqlite3.Error as er:
            print("No connection to DB established")
        return cursor

    def execute_query(self, query):
        '''execute_query executes the inputted query on the database. Use this method
            for queries that don't return data, like insertions and deletions,
             and table creations.'''
        try:
            res = self.cursor.execute(query)
            self.con.commit()
            print("Query succesfully executed")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return res
    def fetch_data(self,query):
        '''fetch_data executes the inputted query on the database and returns the result as a list
            of tuples. '''
        data = None
        try:
            res = self.cursor.execute(query)
            data = res.fetchall()
            self.con.commit()
            print("Query succesfully executed")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return data
    def insert_ticker(self,rows):
        '''This method accepts a list of tuples and inserts the values into
            the ticker table. Each tuple in the list should have both
            a ticker symbol and the name of the company.'''
                               
        for record in rows:         #ticker symbol, name (MSFT, Microsoft)
            try:
                self.cursor.execute("INSERT INTO ticker VALUES (?,?)",record)
            except sqlite3.IntegrityError as e:
                print('duplicate ticker detected')
                pass
        self.con.commit()
      
    def check_for_hold(self,ticker):
        '''This method queries the hold_list table for a ticker. If present,
            the method returns True. False is returned otherwise.'''
        val = (ticker,)
        cur= self.cursor
        res = None
        try:
            res = cur.execute("SELECT EXISTS(SELECT 1 FROM hold_list WHERE symbol = ? LIMIT 1)",(val)).fetchone()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        if res[0]:
            return True
        return False
    def scrub_hold_list(self):
        '''This method removes stocks from the hold_list table when sufficient time has passed
            between their initial discovery and the present time. The hold_list table is 
            maintained to reduce API calls and remove repetitive work.'''

        self.execute_query("DELETE FROM hold_list WHERE date_added <= date('now', '-10 day')")


    def close_connection(self):
        '''This closes our connection ot the database'''
        self.con.close()


def main():
    wrapper = dbInterface()
    
    test = [("GME", "Gamestop Inc.")]
   # wrapper.con.execute("INSERT INTO ticker VALUES (?,?)",('ADGI','Adagio Therapeutics, Inc.'))
    wrapper.con.execute("INSERT INTO mail_list VALUES ('Eddy', 'Gozdz', '2035051230','3')")
   
    #wrapper.con.execute("INSERT INTO hold_list VALUES (?,?)", ('ALLK','2022-02-13'))
    t = [('FREQ','Frequency Therapeutics, Inc.'), ('MNMD','Mind Medicine (MindMed) Inc.')]
    #wrapper.insert_ticker(t)
    #wrapper.insert_ticker(test)
    
    hold = wrapper.check_for_hold('ALLK')
    if hold:
        print("On the hold list")
    else:
        print("not on hold list")
    
    me = wrapper.fetch_data("SELECT first_name,last_name,phone_number,carrier_id FROM mail_list WHERE first_name = 'Calvin'")[0]

    print(me)
    print(me[-1]);print(type(me[-1]))
    print(me[2]);print(type(me[2]))
    print(me[0])
    print(me[1])

    print(wrapper.fetch_data("SELECT * FROM hold_list"))
    print(wrapper.fetch_data("SELECT * FROM ticker"))

    testdata = [('ADGI', 'Adagio Therapeutics, Inc.'), ('ALLK', 'Allakos Inc.'), ('FREQ', 'Frequency Therapeutics, Inc.'), ('MNMD', 'Mind Medicine (MindMed) Inc.'), ('GME', 'Gamestop Inc.')]
    

    carrier = wrapper.con.execute('SELECT name FROM carrier WHERE carrier_id = ?',(me[-1],)).fetchone()[0]
    print(carrier)
    messenger = Messenger()
    mes = messenger.generate_message(testdata)
    person = Person(me[0],me[1],me[2],carrier)
    messenger.send(person,mes)
    wrapper.close_connection()

    #testd = wrapper.execute_query("SELECT date_added FROM hold_list WHERE ")
def view_tables():
    wrapper = dbInterface()
    print(wrapper.fetch_data("SELECT * FROM hold_list"))
    print(wrapper.fetch_data("SELECT * FROM ticker"))
    print(wrapper.fetch_data("SELECT * FROM mail_list"))
    print(wrapper.fetch_data("SELECT * FROM carrier"))
    wrapper.close_connection()

def add_adagio():
    wrapper = dbInterface()
    wrapper.execute_query("INSERT INTO hold_list (symbol) VALUES ('ADGI')")
if __name__ == "__main__":
    #add_eddy()
    view_tables()

    
    