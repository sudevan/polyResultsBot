# importing the required libraries and functions  
from telegram.ext.updater import Updater  
from telegram.update import Update  
from telegram.ext.callbackcontext import CallbackContext  
from telegram.ext.commandhandler import CommandHandler  
from telegram.ext.messagehandler import MessageHandler  
from telegram.ext.filters import Filters  
from telegram import InlineKeyboardButton, InlineKeyboardMarkup ,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext import ConversationHandler
import os
import glob 
import pandas as pd
import math
from telegram.ext import *
from tabill import TABill
# adding different functions to the bot  
import json
import shutil
from datetime import datetime, timedelta
import threading





BASIC_PAY,DA_PAY,FROM_DATE,TO_DATE = range(4)

userChatTrack = {}


the_updater = Updater("6130511154:AAHGEFniMwFebWiFEHgdz7VQf06wVy4X1wQ",  
                use_context = True)  

dispatcher = the_updater.dispatcher

# def sendoptions(update):
#    chat_id = update.message.chat_id
#    if userChatTrack.has_key(chat_id):
#       instance = userChatTrack[chat_id]
#    else:
#        update.message.reply_text( "Could not track the message please start over")
#        return
#     #send the  option messsage with respect to the state of the chat History
#    if (instance.state == "initial"):
#       #send the option to get start date
#       instance.state = "startdate"
#       pass
#    elif(instance.state == "startdate"):
#       instance.startdate = update.message.text
#       instance.state = "enddate"
#    else:
#       update.message.reply_text( "Could not track the message please start over")
  
def sendhelpmsg(update):
    update.message.reply_text(  
        "Hello sir, Welcome to the TABill Generator Bot. For any support contact @sudevank. /start to get started")  
    print(update.message.text)

def the_start(update: Update, context: CallbackContext):
   update.message.reply_text(
       """
       Hello sir, Welcome to the TABill Generator Bot. For any support contact @sudevank @sheheeralins.\n/help to get started
       """)
   

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
  try:
        chatid = str(update.message.chat_id)
        with open(chatid+"/"+chatid+".json", "r") as infile:
         data = json.load(infile)
        update.message.reply_text("Updating....") 
        templatefile="TATemplate.pdf"
        newbill = TABill(file,templatefile,data)
        newbill.saveBill(outputfilename)
        send_document(update,context,outputfilename)
        return
  except FileNotFoundError:
       os.remove(file)
       update.message.reply_text("Please Configure your data first\n /configure to start")


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
       outputfilename=folder+"/"+folder+"_updated.pdf"
    #    handleTAFile(update,context,filepath,outputfilename)
       handleTAFileThread = threading.Thread(target=handleTAFile, args=(update,context,filepath,outputfilename))
       handleTAFileThread.start()
    else:
       update.message.reply_text(  
        "Unknown File format '%s'" % ext ) 
       
def isNaN(string):
    return string != string

def send_document(update, context,file):
    chat_id = update.message.chat_id
    document = open(file, 'rb')
    context.bot.send_document(chat_id, document)


# My Handler Functions

def user_helper(update,context):
   update.message.reply_text(
     """
     List of Commands:
     Update Details /update
     Upload TA Bill /uploadTA
     Download Modified TA Bill /download
     Delete Data  /delete

     """
   )


def start(update, context):
    if update.message.chat_id not in userChatTrack:
       userChatTrack.setdefault(update.message.chat_id, {})
    print(update.message.text)
    """Starts the conversation and asks for the user's basic pay"""
    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Hi! Please enter your basic pay or type /cancel to stop:',
        reply_markup=ReplyKeyboardRemove()
    )
    # Move to next state
    return BASIC_PAY


  
def get_basic_pay(update, context):
    if update.message.chat_id not in userChatTrack:
       userChatTrack.setdefault(update.message.chat_id, {})
    try:
        basic_pay = float(update.message.text)
    except ValueError:
        update.message.reply_text('Please enter a valid number \n /cancel to stop')
        return BASIC_PAY
    
    context.user_data['basic_pay'] = basic_pay
    userChatTrack[update.message.chat_id]['basic_pay'] = basic_pay

    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Please enter DA per day \n /cancel to stop:',
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    # Move to next state
    return DA_PAY


def get_da_pay(update,context):
    if update.message.chat_id not in userChatTrack:
        userChatTrack.setdefault(update.message.chat_id, {})
    try:
        da_pay = float(update.message.text)
    except ValueError:
        update.message.reply_text('Please enter a valid number \n /cancel to stop')
        return DA_PAY
    
    context.user_data['da_pay'] = da_pay
    userChatTrack[update.message.chat_id]['da_pay'] = da_pay

    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Please Enter the From Date \n /cancel to stop:',
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    # Move to next state
    return FROM_DATE


def get_from_date(update, context):
    print(update.message.text)
    try:
        from_date = datetime.strptime(update.message.text, "%d/%m/%Y")
        x = datetime.strptime(update.message.text, "%d/%m/%Y")  # Convert string to datetime object
        userChatTrack[update.message.chat_id]['from_date'] = update.message.text
        incremented_date = from_date - timedelta(days=1)  # Increment the date by one day
        before_date = incremented_date.strftime("%d/%m/%Y") 
        userChatTrack[update.message.chat_id]['before_date'] = before_date

        reply_keyboard = [['Cancel']]
        update.message.reply_text(
            'Please Enter the To Date \n /cancel to stop:',
            # reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)
        )

        # Move to next state
        return TO_DATE

    except ValueError:
        update.message.reply_text('Please enter a valid date \n /cancel to stop')
        return FROM_DATE
    

def get_to_date(update, context):

    try:

        # convert the user input to datetime object
        to_date = datetime.strptime(update.message.text, "%d/%m/%Y")

        # increment the date by one day
        incremented_date = to_date + timedelta(days=1)  # Increment the date by one day
        string = incremented_date.strftime("%d/%m/%Y") 

        # update to date in userChatTrack  in strings
        userChatTrack[update.message.chat_id]['to_date'] = update.message.text
        # update after date in userChatTrack   in strings
        userChatTrack[update.message.chat_id]['after_date'] = string


        diff = to_date - datetime.strptime(userChatTrack[update.message.chat_id]['from_date'], "%d/%m/%Y")
        userChatTrack[update.message.chat_id]['days'] = diff.days + 2


        data = userChatTrack[update.message.chat_id] 

        folder = str(update.message.chat_id)
        if ( not os.path.exists(folder) ):
            os.makedirs(folder)

        with open(folder+"/"+str(update.message.chat_id)+".json",'w') as outfile:
            json.dump(data,outfile)

        reply_keyboard = [['Cancel']]
        update.message.reply_text(
            "Data Saved Successfully\n Please upload TA Bill \n"
            # reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)
        )
        # Move to next state
        return ConversationHandler.END

    except ValueError:
        update.message.reply_text('Please enter a valid date \n /cancel to stop')
        return TO_DATE





def cancel(update, context):
    """Ends the conversation"""
    update.message.reply_text('Conversation canceled.',)
    return ConversationHandler.END

def getData(update,context):
    chatid = str(update.message.chat_id)

    try:
        with open(chatid+"/"+chatid+".json", "r") as infile:
         data = json.load(infile)
        update.message.reply_text(data)
    except FileNotFoundError:
       update.message.reply_text("Please update your details\n /update to start")
      
def downloadTABill(update,context):
    chat_id = str(update.message.chat_id)
    try:
       document = open(chat_id+"/"+chat_id+"_updated.pdf", 'rb')
       context.bot.send_document(chat_id, document)
    except FileNotFoundError:
       update.message.reply_text("Please upload your TA Bill\n /uploadTA to start")   

def uploadTABill(update,context):
   
   update.message.reply_text(
      'Upload the TABill without Modification'
   )

def deleteData(update,context):
   chat_id = str(update.message.chat_id)
   if os.path.exists(chat_id):
    shutil.rmtree(chat_id)
    update.message.reply_text(
       "Data Deleted from the server"
    )
   else:
    print("The file does not exist")
    update.message.reply_text(
       "Data not found"
    )
    
   


        


# adding the handler to handle the messages and commands  
dispatcher.add_handler(CommandHandler('start', the_start))  
dispatcher.add_handler(MessageHandler(Filters.document, downloader)) 


# My handlers

# dispatcher.add_handler(CommandHandler('configure',configure))
dispatcher.add_handler(CommandHandler('getdata',getData))
dispatcher.add_handler(
       ConversationHandler(
        entry_points=[CommandHandler('update', start)],
        states={
            BASIC_PAY: [MessageHandler(Filters.text & ~Filters.command, get_basic_pay)],
            DA_PAY: [MessageHandler(Filters.text & ~Filters.command, get_da_pay)],
            FROM_DATE: [MessageHandler(Filters.text & ~Filters.command, get_from_date)],
            TO_DATE: [MessageHandler(Filters.text & ~Filters.command, get_to_date)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    )

dispatcher.add_handler(CommandHandler('uploadTA',uploadTABill))

dispatcher.add_handler(CommandHandler('delete', deleteData))  
dispatcher.add_handler(CommandHandler('download', downloadTABill))  


# # Filtering out unknown messages  
dispatcher.add_handler(MessageHandler(Filters.text, user_helper))  
dispatcher.add_handler(MessageHandler(Filters.command,user_helper))
dispatcher.add_handler(CommandHandler('help',user_helper))





#the_updater.add_error_handler(error)
# running the bot  
the_updater.start_polling() 

