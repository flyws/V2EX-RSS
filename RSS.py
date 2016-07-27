import feedparser
import re
import os
import requests
import time
import calendar
from Tkinter import *
import webbrowser


class Application(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()

		# Create the graphic interface
		self.url = Entry(self, width = 50)
		self.url.pack()

		self.button = Button(self, text='Enter',command=self.get_input)
		self.button.pack()

		self.contents = StringVar()
		self.url.config(textvariable=self.contents)

	# create a canvas inside the frame
	def create_scrollbar(self):
		def myfunction(event):
			self.canvas.configure(scrollregion=self.canvas.bbox('all'),width=1000,height=500)

		self.canvas = Canvas(self)
		self.frame = Frame(self.canvas)
		self.myscrollbar = Scrollbar(self, orient='vertical',command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.myscrollbar.set)
		self.myscrollbar.pack(side='right',fill='y')
		self.canvas.pack(side='left')
		self.canvas.create_window((0,0),window=self.frame,anchor='nw')
		self.frame.bind('<Configure>',myfunction)

		
	# to add 'http://' prefix to those who are lazy
	def error_handler(self):
		str = self.contents.get()
		if re.match(r'http://', str, flags=0) == None:
			url = 'http://' + str
			try:
				requests.request('GET', url)
				return url
			except:
				Label(self, text='Not A Valid Address!',
					relief=RAISED).pack()
		else:
			url = str
			try:
				requests.request('GET', url)
				return url
			except:
				Label(self, text='Check your Address Spelling!',
					relief=RAISED).pack()

	# captures the user input and return the url
	def get_input(self):
		global user_input
		user_input = self.error_handler()
		text = self.print_input(user_input)
		return user_input

	# print the RSS result in the frame, and it would also create a 
	# hyperlink in the title.
	def print_input(self, input):
		text = parser(input)
		text = text.get_text()
		self.create_scrollbar()
		for key, value in text.items():
			t = Label(self.frame, text = key, fg="blue", cursor="hand2")
			# t.bind('<Button-1>', callback)
			t.bind('<Button-1>', lambda self,value=value: callback(value))
			t.pack()

	# this function is for print_input above
	global callback
	def callback(link):
		webbrowser.open(link)


class parser(object):
	"""this class would take the url input and get 50 newest post
		from the website, and create a dictionary that contains the 
		title and the link. I might consider putting more elements in
		it if I have the future need.
	"""
	def __init__(self, url):
		self.url = url
		self.feed = feedparser.parse(self.url)
		global lenItem
		lenItem = len(self.feed.entries)

	def get_text(self):
		content = {}
		for i in range(0, lenItem):
			title = self.feed.entries[i].title
			link = self.feed.entries[i].link
			# description = self.feed.entries[i].description
			# author = self.feed.entries[i].author
			pubDate = self.feed.entries[i].published
			pubTime = time.strptime(pubDate, '%Y-%m-%dT%H:%M:%SZ')
			timeStamp = calendar.timegm(pubTime)
			pubTime = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(timeStamp))

			title = title.encode('utf8')
			# description = description.encode('utf8')
			# author = author.encode('utf8')
			link = link.encode('utf8')
			title = title + '  ' + pubTime
			content[title]=link
		return content
		

if __name__ == '__main__':

	root = Application()
	root.master.title('Input Web Address?')
	root.master.minsize(400,40)
	root.mainloop()





