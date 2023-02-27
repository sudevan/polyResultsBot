# importing the required libraries and functions  
from telegram.ext.updater import Updater  
from telegram.update import Update  
from telegram.ext.callbackcontext import CallbackContext  
from telegram.ext.commandhandler import CommandHandler  
from telegram.ext.messagehandler import MessageHandler  
from telegram.ext.filters import Filters  
import os
import glob 
import pandas as pd
import math
from telegram.ext import *
from tabill import TABill
# adding different functions to the bot  

the_updater = Updater("5900809165:AAEkFGQwgJfcg9Cyi5GsBMNlmejNGrVpGQk",  
                use_context = True)  

def sendhelpmsg(update):
    update.message.reply_text(  
        "Hello sir, Welcome to the SBTE Result Analysis. Please send the zip(with password 1234)/csv file downloaded from sbte without any modification. For any support contact @sudevank"  
        )  
    print(update.message.text)
def the_start(update: Update, context: CallbackContext):  
    sendhelpmsg(update) 
def the_help(update: Update, context: CallbackContext):  
    sendhelpmsg(update) 
  
def unknownCommmand(update: Update, context: CallbackContext):  
    sendhelpmsg(update) 
def unknownText(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "Unfortunately, the system cannot recognize you, you said '%s'" % update.message.text  
        )  
def handleZipFile(update,context,file):
  pass
def handleCsvFile(update,context,file):
  pass
def handleTAFile(update,context,file,outputfilename):
  update.message.reply_text("Updating....") 
  newtabill = TABill(file)
  newtabill.saveBill(outputfilename)
  send_document(update,context,outputfilename)
  return


def downloader(update, context):
    #context.bot.get_file(update.message.document).download()

    print("file downloaded",update.message.document.file_name)

    filename = update.message.document.file_name
    chat_id = update.message.chat_id
    folder = str(chat_id)
    if ( not os.path.exists(folder) ):
      os.makedirs(folder)
    filepath=folder+"/"+filename
    # writing to a custom file
    with open(filepath, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    update.message.reply_text("Processing Please Wait....")
    filenamewoext =  os.path.splitext(filename)[0]
    ext =  os.path.splitext(filename)[1]
    print (filepath,ext)
    if (ext == ".zip"):
      handleZipFile(update,context,filepath)
    elif(ext == ".csv"):
        handleCsvFile(update,context,filepath)
    elif(ext == ".pdf"):
       #this is a TA file
       outputfilename=folder+"/"+filenamewoext+"_updated.pdf"
       handleTAFile(update,context,filepath,outputfilename)
    else:
       update.message.reply_text(  
        "Unknown File format '%s'" % ext ) 
def isNaN(string):
    return string != string

def send_document(update, context,file):
    chat_id = update.message.chat_id
    document = open(file, 'rb')
    context.bot.send_document(chat_id, document)
# adding the handler to handle the messages and commands  
the_updater.dispatcher.add_handler(CommandHandler('start', the_start))  
the_updater.dispatcher.add_handler(MessageHandler(Filters.text, unknownCommmand))  
 # Filtering out unknown commands  
the_updater.dispatcher.add_handler(MessageHandler(Filters.command, unknownCommmand))  
  
# Filtering out unknown messages  
the_updater.dispatcher.add_handler(MessageHandler(Filters.text, unknownText))  

the_updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader)) 
#the_updater.add_error_handler(error)
# running the bot  
the_updater.start_polling() 


