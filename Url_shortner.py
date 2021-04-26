import pyperclip
import tkinter
import requests
import json
from urllib.request import urlopen
from urllib.error import HTTPError,URLError

#GUI
def window():
    #Defining global access and intialising variables
    global root
    global url
    global tag
    global url_address
    global message
    global success
    root=tkinter.Tk()
    url=tkinter.StringVar()
    tag=tkinter.StringVar()
    url_address=tkinter.StringVar()
    message=tkinter.StringVar()
    success=tkinter.StringVar()
    #Window Properties
    root.geometry("335x250")
    root.title("URL Shortener")
    root.configure(bg="turquoise")
    #Defining positions
    tkinter.Label(root,text="URL*",width=20,font=("bold",10),bg="turquoise").place(x=10,y=20)
    tkinter.Entry(root,textvariable=url).place(x=150,y=21)
    tkinter.Label(root,text="Custom tag",width=20,font=("bold",10),bg="turquoise").place(x=10,y=50)
    tkinter.Entry(root,textvariable=tag).place(x=150,y=51)
    tkinter.Label(root,text="",textvariable=message,bg="turquoise",fg="red",font=("bold",10)).place(x=122,y=80)
    tkinter.Button(root,text="Generate Short URL",command=urlshortener).place(x=110,y=110)
    tkinter.Label(root,text="Shortened URL",width=20,font=("bold",10),bg="turquoise").place(x=10,y=150)
    tkinter.Entry(root,textvariable=url_address).place(x=150,y=151)
    tkinter.Button(root,text="Copy URL",command=copyurl).place(x=130,y=180)
    tkinter.Label(root,text="",textvariable=success,bg="turquoise",font=('Helvetica', 18, 'bold')).place(x=2,y=210)
    root.mainloop()

#Shorten the URL
def urlshortener():
    #Fetch data entered
    link=url.get()
    back=tag.get()
    #Clear old data
    url_address.set('')
    message.set('')
    success.set('')
    #Required data for Api
    if back=='':
        linkRequest = {
            "destination": link
          , "domain": { "fullName": "rebrand.ly" }
              }
    else:
        linkRequest = {
            "destination": link
          , "domain": { "fullName": "rebrand.ly" }
          , "slashtag": back
              }
    requestHeaders = {
        "Content-type": "application/json",
        "apikey": "cc9d22cb14704b3f9871cf16ceb665f0",
        }
    try:
        #Checking validity of api
        urlopen(link)
        #Sending request via Api
        r = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest),
            headers=requestHeaders)
        #Check if the custom tag already exists
        if (back!='' and (r.json()["errors"][0].get('code')=="AlreadyExists")):
            message.set("Domain taken")
    except (HTTPError,URLError):
        message.set(("Invalid Url Key"))
    except KeyError:
        display(r)
    else:
        #Display shortened url
        display(r)

def display(res):
    if (res.status_code == requests.codes.ok):
        short = res.json()
        url_address.set(short["shortUrl"])
        success.set("URL Shortened Successfully")

#For copying URL to Clipboard        
def copyurl():
    url_short=url_address.get()
    pyperclip.copy(url_short)
    
window()

