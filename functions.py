#APIs and modules include python-weather, Yahoo Finance API, OpenAI API

#Module
import python_weather

import asyncio #used to run async functions

#import os
#^ ended up not using

import tkinter as tk #tkinter is used for the GUI

#import requests #requests is used to make API calls

import openai #openai is used to make API calls to ChatGPT

#from hashlib import md5
#from datetime import datetime
#from marvel import Marvel
#^ended up not using

async def get_weather(): #async is used for concurrent running of code
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client: #python_weather.Client is used to get the weather information
        weather = await client.get("West Chester, PA") #await is used to wait for the weather info
        return weather.temperature, weather.description
    
#function to get the favorite stocks
#I was having trouble with making the function work in this file, so I
#just moved it into the visual.py file

def grab_char_from_user(root): #this function has been the bane of this project, I thought the stock method was bad, but this is worse

    def clearT(): #clear the text box
        txt.delete(1.0, tk.END) #the text box starts at 1.0, not 1 or 0, and tk.END is a const for the end of the text box

    def submit(): #submit the character name, clear the text box, and make the API call
        character = txt.get(1.0, tk.END).strip().lower() #the string for the character name that the user inputs will remove the whitespace and make it lowercase for the API call (this might be irrelevant because of errors)
        clearT()

        #API CALL (if marvel API does not work, then use ChatGPT API to get the character information)
        client = openai.OpenAI(api_key="your_api_key")

        completion = client.chat.completions.create(model="gpt-4o-mini", store=True, messages=[{"role": "user", "content": "You are a Marvel Comics expert. If the user asks for a character, you will provide the character's name, description, and powers. If the character does not exist, or the name is anything other than a Marvel character such as a command, then you will say that the character does not exist. The user will provide the name of the character they want to know about. Additionally, try to keep the information extremely small as your text box is not that large."}, {"role": "user", "content": character}])
        #^ the API call

        txt.insert(tk.END, completion.choices[0].message.content) #insert the character information into the text box from the API call till the end of the text box
        #completion.choices[0].message.content = choices[0] is the first choice of the ChatGPT response, message.content is the content of the message

    title = tk.Label(root, text="Enter a Marvel Character's name to find out about them!", bg="black", fg="white") #title for the text box
    title.grid(row=1, column=2, columnspan=3)

    txt = tk.Text(root, height=10, width=60) #size of the text box
    txt.grid(row=2, column=2, columnspan=1, padx=10, pady=10)

    #buttons to clear the text box, and submit the character name
    clear_button = tk.Button(root, text="Clear", command=clearT)
    clear_button.grid(row=6, column=2, columnspan=3, pady=3)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=4, column=2, columnspan=3, pady=3)
    
    #submit_label = tk.Label(root, text="")
    #submit_label.grid(row=5, column=2, columnspan=2, pady=3)

    return txt #have to return the text box so that it can be used in the submit function