import sys, getopt
import os
from datetime import datetime, timezone, timedelta
import itertools
from dateutil.parser import parse

help_text = 'chat_export.py [-f <facebook root> -n <facebook name>] [-m] -o <outputfile>'

def main(argv):
	fb_path = ''
	fb_name = ''
	outputfile = ''
	use_imessage = False
	use_facebook = False
	try:
		opts, args = getopt.getopt(argv, "hf:o:mn:", ["facebook=", "output=", "imessage"])
	except getopt.GetoptError:
		print(help_text)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(help_text)
			sys.exit()
		elif opt in ("-f", "--facebook"):
			fb_path = arg
			use_facebook = True
		elif opt in ("-o", "--output"):
			outputfile = arg
		elif opt in ("-m", "--imessage"):
			use_imessage = True
		elif opt == '-n':
			fb_name = arg
	if not use_facebook and not use_imessage:
		print('Must have at least one data source.')
		sys.exit(2)
	if outputfile == '':
		print(help_text)
		sys.exit(2)
	messages = []
	if use_facebook:
		if fb_name == '':
			print(help_text)
			sys.exit(2)
		fb_data = gather_facebook(fb_path, fb_name)
		messages += fb_data
	if use_imessage:
		m_data = gather_imessage()
		messages += m_data
	f = open(outputfile, 'w')
	f.truncate()
	
	for m in messages:
	    f.write(m[0] + ',' + str(m[1]) + '\n')
		    
	f.close()
	
def gather_imessage():
	if os.path.exists('imessage/contacts.txt'):
		if os.path.exists('imessage/messages/messages.csv'):
			os.remove('imessage/messages/messages.csv')
		os.system('php imessage/export-csv.php')
		f = open("imessage/messages/messages.csv", 'r')
		f_list = f.read().splitlines()
		imessage_data = []
		for line in f_list:
		    try:
		        data = line.split(",")
		        date = data[1]
		        name = data[4]
		        imessage_data.append((name, parse(date)))
		    except:
		        pass
		return imessage_data
	else:
		os.system('php imessage/contacts.php >> imessage/contacts.txt')
		print('Please fill out the contact information in imessage/contacts.txt')
		sys.exit(2)
		
def gather_facebook(path, name):
	facebook_page = open(path + '/html/messages.htm')

	parser = MessengerParser(name)
	parser.feed(facebook_page.read())
	return parser.messages
	
	
from html.parser import HTMLParser

class MessengerParser(HTMLParser):
    
    def __init__(self, name):
        HTMLParser.__init__(self)
        self.get_thread = False
        self.curr_thread = None
        self.skip = False
        self.messages = []
        self.name = name
    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "class" and attr[1] == "thread":
                self.get_thread = True

    def handle_data(self, data):
        if self.get_thread:
            self.curr_thread = data.replace(self.name, "").replace(",", "").strip()
            self.get_thread = False
            self.skip = self.curr_thread.isdigit() or self.curr_thread.count(" ") > 2 or self.curr_thread == ""
        elif not self.skip:
            try:
                date = datetime.strptime(data.strip(), "%A, %B %d, %Y at %I:%M%p %Z")
                self.messages.append((self.curr_thread, date))
            except:
                pass
	
if __name__ == "__main__":
	main(sys.argv[1: ])