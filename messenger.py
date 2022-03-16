import smtplib

class Person():
    def __init__(self,first,last,phoneNumber,carrier = 'att') -> None:
        self.firstName = str(first)
        self.lastName = str(last)
        self.number = phoneNumber
        self.carrier = carrier
    def get_name(self):
        return self.firstName + " "+ self.lastName
    def get_phone_number(self):
        return self.number
    def get_carrier(self):
        return self.carrier


class Messenger():
    def __init__(self) -> None:
        self.carriers = {
            'att':    '@mms.att.net',
            'tmobile':' @tmomail.net',
            'verizon':  '@vtext.com',
            'sprint':   '@page.nextel.com'
        }
        
        self.username = "BOT EMAIL HERE"
        self.password = "BOT EMAIL PASSWORD HERE"

    def add_receipient(self,person):
        self.mailList.append(person)

    def send(self,person,message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
        to_number = str(person.get_phone_number())+self.carriers[person.get_carrier()]
        print(to_number)
        auth = (self.username, self.password)

        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login(auth[0], auth[1])

        formatted = "Dear {}".format(person.get_name()) + ",\n" + message
        print(formatted)
        # Send text message through SMS gateway of destination number
        server.sendmail( auth[0], to_number,formatted)
    def generate_message(self,ticker_list):
        s = "The following candidates have been identified today:\n\n"
        for i in ticker_list:
            s+= "ticker: " + str(i[0]) +  "\nname: " + str(i[1]) + "\n\n"
        return s
 
