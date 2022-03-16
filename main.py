import key 
from dbInterface import dbInterface
from messenger import Messenger,Person
from Screener import Screener

# The entry point of the Biotech Screener. This will be run on weekdays once before market close
def main():
    api_token = key.key
    sector = "Healthcare"

    # Screener Object
    screener = Screener(sector,30)
    # Wrapper object for Sqlite database
    db = dbInterface()
    # Messenger object for pushing out findings
    messenger = Messenger()

    ticker_list = screener.get_tickers()
    print("\nInitial Screen candidates: " + str(ticker_list))
    for ticker in ticker_list:
        # Check to see if this ticker is on hold and scrub it from list if so
        if db.check_for_hold(ticker[0]):
            ticker_list.remove(ticker)
    
    # Further filter by checking to see if candidates have options sufficient for buy/write strategy
    print("\nCandidates past hold list screen: " + str(ticker_list))
    candidates = screener.get_option_data(ticker_list)
    print("\nCandidates past option parameter screen: " + str(candidates))
    # Insert candidates into the ticker table. A trigger will place these in the hold_list table 
    # automatically.
    db.insert_ticker(candidates)

    # Message to be pushed to mailing list
    if candidates:
        tape = messenger.generate_message(candidates)

        for row in db.fetch_data("SELECT first_name,last_name,phone_number,carrier_id FROM mail_list"):
            carrier = db.con.execute('SELECT name FROM carrier WHERE carrier_id = ?',(row[-1],)).fetchone()[0]
            person = Person(row[0],row[1],row[2],carrier)
            messenger.send(person,tape)

        print("Vetted candidates: " + str(candidates))

    db.scrub_hold_list()
    db.close_connection()

if __name__ == "__main__":
    main()

