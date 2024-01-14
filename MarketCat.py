#Special thanks to Youtubers who teach people how to code and how to implement specific functionalities to their projects!!!
#this scripts takes all the data from the included files and adds it to seachbox/Listbox for tkinter


from tkinter import *
import csv
import Analyzer
import json

root = Tk()
root.title("Analyzer")
root.geometry("500x500")

def update(data):
	#del everything
	my_list.delete(0,END)
	#add topping
	for item in data:
		my_list.insert(END,item)

def fillout(e):
	#del everything in entrybox
	my_entry.delete(0,END)

	#add clicked item 
	my_entry.insert(0,my_list.get(ACTIVE))


def check(e):
	#grab what was typed
	typed = my_entry.get()

	if typed == "":
		data = dataList
	else:
		data = []
		for item in dataList:
			if typed.lower() in item.lower():
				data.append(item)

	#update listbox with selected items
	update(data)

def displayData(stock):
	symbol = ""
	try:
		with open('nasdaq_screener_1704649993170.csv','r') as f:
			csv_reader = csv.reader(f)
			next(csv_reader)
			for line in csv_reader:
				if line[1] == stock:
					symbol = line[0]
				else:
					pass
		with open("SymbolsCrypt.json","r") as k:
			data = json.load(k)
			for i in range(len(data)):
				if list(data)[i] == stock:
					symbol = data.get(stock)
				else:
					pass
	except:
		pass
	Analyzer.displayStockData(symbol)

my_label = Label(root,text = "Choose the stock", font = ("Helvetica",14), fg = "grey")

my_label.pack(pady=20)

my_entry = Entry(root,font=("Helvetica",20))
my_entry.pack()

my_list = Listbox(root, width=50)
my_list.pack(pady=40)

#creating a list where the data will be included 
dataList = []

with open("nasdaq_screener_1704649993170.csv","r") as f:
	csv_reader = csv.reader(f)
	next(csv_reader)
	for line in csv_reader:
		dataList.append(line[1])
#adding there some crypto symbols which took time to have been filtered out :P 
with open("SymbolsCrypt.json","r") as j:
	data = json.load(j)
	for i in range(len(data)):
		dataList.append(list(data)[i])


update(dataList)
#create a binding on the listbox
my_list.bind("<<ListboxSelect>>",fillout)
#Create a binding on the entry
my_entry.bind("<KeyRelease>",check)

button = Button(root,text= "Analyze", command = lambda:displayData(my_entry.get()))
button.pack()
root.mainloop()
