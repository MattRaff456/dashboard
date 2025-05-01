#Visual code for the Dashboard

import tkinter as tk
import asyncio #to wrap and run the async functions
from tkinter import messagebox, simpledialog
#from functions import get_fav_stocks, get_weather, get_marvel_characters #import the functions from my other python file
from functions import get_weather, grab_char_from_user
from matplotlib.figure import Figure #matplotlib is used for plotting graphs, and Figure is used to create a container for the plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #tkagg is used to display the plot in the tkinter window

import yfinance as yf

from PIL import Image, ImageTk

#wrapper function for the async weather function
#need a wrapper function because tkinter does not support async functions
#placing functions at the top because there were some errors being thrown
def call_weather():
    try:
        weather = asyncio.run(get_weather())
        weather_label.config(text="Temperature: {}°F\nDescription: {}".format(weather[0], weather[1])) #configuring the weather_label which is already initialized to display the temperature and description
        weather_label.config(bg="black") #change the background color of the weather_label to black to make it easier to read
    except Exception as e:
        weather_label.config(text=f"Error: {str(e)}")
    
    image_path = weather_image() #kept the functions separate to make it easier for debugging
    if image_path:
        try:
            image = Image.open(image_path)

            #below is a bunch of test cases
            #image = Image.open("sunny.png")     
            #image = Image.open("cloudy.png")
            #image = Image.open("rain.jpg")
            #image = Image.open("snow.jpg")

            image = image.resize((100, 100), Image.LANCZOS) #resize the image to make it not ruin the layout of the dashboard
            #Image.LANCZOS is the antialiasing filter for the image. It was changed from Image.ANTIALIAS because it was deprecated

            weather_image2 = ImageTk.PhotoImage(image) #convert the image to a PhotoImage for tkinter
            image_label.config(image=weather_image2) #configure the image_label to display the image
            image_label.image = weather_image2 #change the name because weather_image throws an unboundlocal error
        except Exception as e:
            image_label.config(text=f"Error: {str(e)}")

#function to get the weather image
#need to use the weather description to get the image
def weather_image():
    words_to_match = {"sunny": "sunny.png", "cloudy": "cloudy.png", "rain": "rain.jpg", "snow": "snow.jpg", "storm": "storm.jpg"} #python-weather has other descriptions, but I do not want to use an
    #image for every single one, so I just try to match the description to the words in the dictionary
    
    try:
        weather = asyncio.run(get_weather())
        for words in words_to_match:
            if words in weather[1].lower(): #if the keywords are in the weather description (undercase), then return the image path
                return words_to_match[words]
    except Exception as e:
        print(f"Error loading weather image: {e}")
    return None #if an error does not occur, and there is no image for the weather description, then return None

def get_fav_stocks():
    fav_stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "QQQ", "NVDA", "META", "GE", "VGT", "PLTR", "WMT", "BTC-USD"]
    index = [0] #we need to be able to change the index of the stock, so we need to make it mutable

    def update_stock():
        stock_symbol = fav_stocks[index[0]] #grab the stock symbol from the set
        try:
            stock = yf.Ticker(stock_symbol) #grab the info on the stock
            data = stock.history(period="6mo")

            ax.clear() #everytime the plot is updated, clear the previous plot
            ax.plot(data["Close"], label=f" Stock Price") #plot the stock price | 'Close' is the closing price of the stock
            ax.set_title(f"{stock_symbol} Stock Price in the Last 6 Months")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price $")
            ax.legend() #adds a visual key to the plot
            canvas.draw() #draws the plot on the canvas
        except Exception as e:
            print(f"Error loading stock data: {e}")

    def next(): #method to change the plot to the next stock
        if index[0] < len(fav_stocks) - 1: #check if the index is less than the length of the list
            index[0] += 1 #increment the index and update the stock
            update_stock()
    
    def previous(): #method to change the plot to the next stock
        if index[0] > 0: #check if the index is greater than 0
            index[0] -= 1 #decrement the index and update the stock
            update_stock()

    figure = Figure(figsize=(6, 4)) #size of the figure
    ax = figure.add_subplot(111) #number of rows, columns, and index of the subplot (1 for each, not 111)

    canvas = FigureCanvasTkAgg(figure, master=root) #canvas is the container for the figure, master is the root window
    canvas_widget = canvas.get_tk_widget() #widget to be displayed in the tkinter window
    canvas_widget.grid(row=7, column=0, columnspan=3, pady=10) #grid layout for the widget

    button_frame = tk.Frame(root) #frame for the button
    button_frame.grid(row=8, column=0, columnspan=3, pady=10) #grid layout for the button frame

    prev_button = tk.Button(button_frame, text="Previous", command=previous) #buttons to change the plot
    prev_button.pack(side="left", padx=10)

    next_button = tk.Button(button_frame, text="Next", command=next) #button to change the plot
    next_button.pack(side="left", padx=10)

    #update the stock plpot
    update_stock()

#root window section
root = tk.Tk() #initialize the root window for the dashboard
root.title("Dashboard")
root.geometry("{}x{}-1+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#^ This line sets the window size to fit someone's entire screen. Mine appears to be slightly off, hence the -1, but you can change the -1 to a +0 if yours is not appearing correctly.

#configuring a grid layout for the buttons
root.columnconfigure(0, weight=1) #weight determines how much each column will take up
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

#button initialization section
button = tk.Button(root, text="Weather", activebackground="blue", activeforeground="white", bg="black", fg="white", width=20, height=2, font=("Arial", 16), command=call_weather)
#activebackground and activeforeground are the colors of the button and the text when it is clicked. bg and fg are the colors of the button and the text when it is not clicked.
#the command is the function that the button will call when clicked.
#^ I want the buttons to have a black background with white text. I also want the background and text to change color when the button is clicked.
button.grid(row=0, column=0, pady=10) #set the location of the button i.e. row 0 with y-axis padding

weather_label = tk.Label(root, text="", fg="white", font=("Arial", 16)) #initialize the weather label for the weather information
weather_label.grid(row=1, column=0, columnspan=1, pady=10) #I set the weather_label to exist in the row beneath the button, and I make it span across the entire column

image_label = tk.Label(root) #initialize the image_label for the weather image
image_label.grid(row=2, column=0, pady=10) #^ I do this by making a grid layout for the image_label which is where the image will go. I make the image_label not overlap with
#the text of the weather by putting it in a different row

button2 = tk.Button(root, text="Stocks", activebackground="blue", activeforeground="white", bg="black", fg="white", width=20, height=2, font=("Arial", 16), command=get_fav_stocks)
button2.grid(row=0, column=1, pady=10)

stock_label = tk.Label(root, text="") #initialize the stock_label for the stock information
stock_label.grid(row=2, column=2, pady=10)

button3 = tk.Button(root, text="Marvel Characters", activebackground="blue", activeforeground="white", bg="black", fg="white", width=20, height=2, font=("Arial", 16), command=lambda: grab_char_from_user(root))
#^ have to use a lambda function to pass the root window into the command because you cannot pass a parameter in the command argument
button3.grid(row=0, column=2, pady=10)

root.mainloop() #run the main loop for the tkinter window / dashboard