# -*- coding: utf-8 -*-
from tkinter import * 
from Fileop import File
from config_tk import *
from tkinter import ttk , filedialog as fd ,messagebox as msg

import sys , os , re , threading ,json
from _entry import scroll_text , _text
from PIL import Image , ImageTk
import subprocess as subp
import argparse

root = Tk()
root.title("Cosmo")
root.geometry(geo)
# root.iconbitmap(icon)
root['bg'] = "#1A1E23" 

with open('static/shell.json') as j_file :
	data = json.load(j_file)

def regular_ex(e):
	'''regular Expression'''
	try:
		file_n , file_e = os.path.basename(f_name).split('.')
		if file_e == 'py':
			defs = Extra[0]
			withs = Extra[1]
			text_lines = text.get(0.0 , END)
			regd = re.compile("def\t?[^a-zA-Z]+" , re.M)
			regw = re.compile("with\t?[^a-zA-Z]+" , re.M)
			with_match = regw.search(text_lines)
			if  with_match:

				text.insert(INSERT , withs)

			elif regd.search (text_lines) :
				text.insert(INSERT , defs)
		elif file_e == 'html':
			text_lines = text.get(0.0 , END)
			regd = re.compile("html" , re.M)
			html_match = regd.search(text_lines)
			if html_match:
				text.insert(INSERT , Extra[3])			
	except :
		pass

def delete(event):
	'''clean the screen'''
	text.delete(0.0, END)	

def Open(e = None):
	'''open a file & set its content in scroll_text'''
	global f_name
	
	f_name = fd.askopenfilename(initialdir = Extra[4])
	try:

		show_case['text'] = f_name

		text.delete(0.0, END)	
		os.chdir(os.path.dirname(f_name))
		root.title("PROCESS %s" % os.getcwd())
		with open(f_name , "rb") as f :
			data = f.read()
		text.insert(INSERT , data)

		with open(f_name , "rb") as f2 :
			for i ,line in enumerate(f2.readlines()) :
				state_bar['text'] = 'Line %s' % i
				
	except:
		pass

def save():
	'''save a file with file dialog'''
	global f_name
	f_name = fd.asksaveasfilename(initialdir = Extra[4])
	try:
		with open(f_name , "wb") as data :
			f_data =  text.get(0.0 , END)
			data.write(f_data)
	except :
		pass

def save_e(e=None):
	'''save a file with alt+s'''
	try:
		with open(f_name , "wb") as data :
			f_data =  text.get(0.0 , END)
			data.write(f_data)
	except :
		save()

def new_file(e = None):
	global f_name
	try:
		f_name = fd.asksaveasfilename(initialdir = Extra[4])
		with open(f_name , 'wb') as f :
			f.write(text.get(0.0 , END))
		text.delete(0.0 , END)
		show_case['text'] = f_name
	except :
		pass
def run(event = 0):
	global show
	'''run a python file'''
	try:
		show = scroll_text(panel , bg = bg , fg = "#fff" ,  relief="flat" , font = font)
		show.place(relx = 0 , rely = 1)
		panel.add(show)
		shell = data["python_shell"]
		out=subp.check_output('%s %s' % ( shell , f_name) , shell = True,stderr = True)
		show.insert(INSERT , out)
	except Exception as e:
		show.insert(INSERT , e)
		


def run_html():

	shell = data["html_shell"]

	os.system('%s "%s" '% (shell , f_name ))

def run_js(e = None):
	shell = data["js_shell"]
	try:
		out=subp.check_output('%s "%s"' % ( shell , f_name) , shell = True)
		show = scroll_text(panel , bg = bg , fg = "#fff" ,  relief="flat" , font = font)
		show.place(relx = 0 , rely = 1)
		panel.add(show )
		show.insert(INSERT , out)
	except Exception as e:
		msg.showerror('Error' , e)

def bright () :
	try:
		show['bg'] ='#000'
		show['fg'] ='#fff'
	except :
		pass

	root['bg'] = "#fff"
	panel['bg'] ='#fff'
	frame['bg'] = '#fff'
	items = [show_case , state_bar , text , menu_theme , menu_sub , menu_sub2]
	for item in items : 
		item["bg"] = "#fff"
		item["fg"] = "#000"
	with open('%s/theme.con' % sys.argv[0][:-8] , "wb") as f :
		f.write("bright")

def black () :
	try:
		show['bg'] ='#000'
	except :
		pass
	root['bg'] = "#000"
	panel['bg'] ='#000'
	frame['bg'] = '#1A1E23'
	items = [show_case , state_bar , text , menu_theme , menu_sub , menu_sub2]
	for item in items : 
		item["bg"] = "#000"
		item["fg"] = "#fff"
	with open('%s/theme.con' % sys.argv[0][:-8] , "wb") as f :
		f.write("black")

def Orignal():
	try:
		show['bg'] =bg
	except :
		pass
	root['bg'] = "#1A1E23"
	panel['bg'] ="#000"
	frame['bg'] = "#1A1E23"
	items = [text , menu_theme , menu_sub , menu_sub2]
	for item in items : 
		item["bg"] = "#343D46"
		item["fg"] = "#fff"

	for item in [show_case , state_bar]:
		item["bg"] = "#1A1E23"
		item["fg"] = "#fff"

	with open('%s/theme.con' % sys.argv[0][:-8], "wb") as f :
		f.write('dark')
	print(sys.argv[0][:-8])

def about_page():
		
	myself = """\
cosmo 1.1.0
for information contact :
author : abderrahim mokhnache
email :abderrahimokhnache@gmail.com
	"""
	# question, or warning
	msg._show("about" , myself ,"info" ,"ok")
def help_page():
	
	help_msg = Extra[3]
	msg.showinfo("help" , help_msg)

"""menu bar"""
img = ImageTk.PhotoImage(Image.open(images[0]))
img_new = ImageTk.PhotoImage(Image.open(images[1]))
img_Save = ImageTk.PhotoImage(Image.open(images[2]))
img_open = ImageTk.PhotoImage(Image.open(images[3]))
img_file = ImageTk.PhotoImage(Image.open(images[4]))

menu_bar = Menu(root , tearoff = 0 )
menu_sub2 = Menu(root , tearoff = 0 , bg = root_bg , fg = fg)
menu_sub2.add_command( label = 'New File   Alt-n'  , command = new_file,
	image = img_new , compound = 'left' )
menu_sub2.add_command( label = 'Open File  Alt-o'  , command = Open ,
	image = img_open , compound = 'left')
menu_sub2.add_command(label = 'Save       Alt-s' , command = save,
	image = img_Save , compound = 'left')
menu_bar.add_cascade(label = 'File' ,menu  = menu_sub2)
menu_sub = Menu(root , tearoff = 0 , bg = root_bg , fg = fg)
menu_sub.add_command(label = 'Python  F5' , command = lambda:threading.Thread(target = run).start(),
	image = img , compound = 'left')
menu_sub.add_command(label = 'Node    F2' , command = run_js,
	image = img_file , compound = 'left')
menu_sub.add_command(label = 'text' , command = lambda: os.startfile(f_name),
	image = img_file , compound = 'left')
menu_sub.add_command(label = 'html' , command = run_html,
	image = img_file , compound = 'left')
menu_sub.add_command(label = 'shell' , command = lambda: os.startfile(f_name),
	image = img_file , compound = 'left')
menu_bar.add_cascade(label = 'Build' ,menu  = menu_sub)
menu_theme = Menu(root , tearoff = 0 , bg = root_bg , fg = fg)
menu_theme.add_command( label = 'bright Theme'  , command = bright )
menu_theme.add_command( label = 'black Theme'  , command = black )
menu_theme.add_command( label = 'dark Theme'  , command = Orignal)
menu_bar.add_cascade(label = "Theme" , menu = menu_theme)
menu_bar.add_command(label = "about" , command = about_page)
menu_bar.add_command(label = "help" , command = help_page)
"""main text Editor """
show_case = Label(root , bg = "#1A1E23" , fg= 'lightgreen' ,font= font)
state_bar = Label(root ,text ="Line 0",bg = '#1A1E23' , anchor = 'w' , fg= '#fff' ,font = font, justify = "left")
frame = Frame(bg = "#1A1E23" ,relief= relief )
panel = PanedWindow(frame,relief = 'flat' , bg = '#000' , orient = VERTICAL)
text = scroll_text(panel ,bg = bg , font = font, fg = fg ,  relief = 'flat')
text.focus_set()
show_case.pack()
frame.place(relx = 0  , rely = 0.05  , relwidth = 0.999 , relheight = 0.9)
panel.pack(fill = BOTH , expand = True)
panel.add(text) 
state_bar.place(relx = 0, rely = 0.92 , relwidth = 0.999 , relheight = 0.1 ) 
"""Events"""

root.bind("<F5>" ,lambda : threading.Thread(target = run).start())
root.bind("<F2>" , run_js)
root.bind("<Control-d>" ,delete)
root.bind("<Control-s>" ,save_e)
root.bind("<Control-o>" ,Open)
root.bind("<Control-n>" ,new_file)
root.bind("<Control-w>" ,lambda e :root.quit())
text.bind("<Tab>" , regular_ex)

try:
	with open('theme.con' , "rb") as f :
		theme = f.read()
	if theme == "black":
		black()
	elif theme == "bright":
		bright()
	elif theme == "dark":
		Orignal()
except :
	pass


try:
	parser = argparse.ArgumentParser()
	parser.add_argument("file" , help= 'file to open')
	args = parser.parse_args()

	text.delete(0.0, END)	
	root.title(title)
	with open(args.file , "rb") as f :
		data = f.read()
	text.insert(INSERT , data)
except :
	pass
	
"""looping"""
root.config(menu = menu_bar)
root.mainloop()

