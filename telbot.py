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
    update.message.reply_text(  
        """Available Commands :  
        /youtube - To get the youtube URL  
        /linkedin - To get the LinkedIn profile URL  
        /gmail - To get gmail URL  
        /jtp - To get the JavaTpoint.com URL""")  
  
def gmailURL(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "provide the gmail address here (For example, example@gmail.com)"  
        )  
  
def youtubeURL(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "Link for the YouTube => https://www.youtube.com/"  
        )  
  
def linkedInURL(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "URL to the LinkedIn Profile => https://www.linkedin.com/username/"  
        )  
  
def jtpURL(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "URL to the official website => https://www.javatpoint.com/"  
        )  
  
def unknownCommmand(update: Update, context: CallbackContext):  
    sendhelpmsg(update) 
def unknownText(update: Update, context: CallbackContext):  
    update.message.reply_text(  
        "Unfortunately, the system cannot recognize you, you said '%s'" % update.message.text  
        )  
def unzipfile(filename):
  pass
def downloader(update, context):
    #context.bot.get_file(update.message.document).download()

    print("file downloaded",update.message.document.file_name)

    filepath = update.message.document.file_name
    chat_id = update.message.chat_id
    folder = str(chat_id)
    if ( not os.path.exists(folder) ):
      os.makedirs(folder)
    # writing to a custom file
    with open(filepath, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    update.message.reply_text("Processing Please Wait....")
    filenamewoext =  os.path.splitext(filepath)[0]
    ext =  os.path.splitext(filepath)[1]
    print (filepath,ext)
    if (ext == ".zip"):
      update.message.reply_text("Unzipping")
      try:
        cmd = "7z x -y -p'1234' '"+ filepath+"' -o"+folder
        os.system(cmd)
        list_of_files = glob.glob(folder+"/*.csv") 
        # * means all if need specific format then *.csv
        print(list_of_files)
        csvfilepath = max(list_of_files, key=os.path.getctime)
        print(csvfilepath)
        send_document(update,context,csvfilepath)
      except Exception as e:
        update.message.reply_text("Failed to unzip make sure the password is 1234. If issues still exists contact @sudevank")
        print("Error : ",str(e))
        return
    else:
      csvfilepath=filepath
      print("Not zip")
    try:
        update.message.reply_text("Analysing Results...")
        send_document(update,context,"773947703670342050.tgs")
        outputfiles = analyscsv(csvfilepath,chat_id)
        for file in outputfiles:
            send_document(update,context,file)
        update.message.reply_text("Thank you... Please send your feedback  @sudevank")
    except Exception as e:
        update.message.reply_text("An exception occured. Please make sure the file not modified. Still error occures send the file to @sudevank")
        print("Error : ",str(e))
def isNaN(string):
    return string != string

def analyscsv(filepath,chat_id):
  #folder = os.path.dirname(filepath)
  folder = str(chat_id)
  filename=os.path.basename(filepath)
  filenamewoext=  os.path.splitext(filename)[0]
  #print(filenamewoext)
  #print(folder)
  df=pd.read_csv(filepath)
  columnname=df.columns[0].replace('\"','').split(";")
  #print(columnname)
  if(len(columnname) > 1):
     df=pd.read_csv(filepath,names=columnname,skiprows=1)
  df.sort_values('Register No',inplace=True)
  semesters=df["Semester"].unique()
  departments=df["Branch"].unique()
  #creating dataframes for department semester wise
  allresult={}
  #this is for indexing each data frame
  allresultindex={}
  outfiles=[]
  grades=['S','A','B','C','D','E','F']
  for dept in departments:
    resultdfs={}
    resultsemindex={}
    for sem in semesters:
      #resultsemindex[sem]= 1
      coursenames={}
      courses = (df.loc[ (df['Semester'] == sem) & (df['Branch'] == dept ) ])["Course"].unique()
      newcoloumnnames = ["RegNumber","Name","Status"]
      for course in courses:
        code=str(course.split("-")[0])
        coursenames[code] = str(course.split("-")[1])
       
        newcoloumnnames.append(code+"IMark")
        newcoloumnnames.append(code+"Grade")
      for grade in grades:
        newcoloumnnames.append(grade+" Count")
      resultdfs[sem] = pd.DataFrame(columns=newcoloumnnames)
      allresult[dept] = resultdfs
      
      index=1
      for code,name in coursenames.items():
        resultdfs[sem].loc[index,"RegNumber"] = code
        resultdfs[sem].loc[index,"Name"] = name
        #print(code, coursenames[code] )
        index += 1
      #course number is to skip grade count 
      numberOfCourses = index-1
      resultsemindex[sem] =index
      allresultindex[dept] = resultsemindex
      #print(index)
      #print(allresultindex[dept][sem] )
  for ind in df.index:
      regno=df['Register No'][ind]
      semester=df['Semester'][ind]
      department = df['Branch'][ind]
      resindex = allresultindex[department][semester]
      #print(resindex)
      resultdf = allresult[department][semester]
      if(len( resultdf[resultdf["RegNumber"] == regno]) == 0 ):
        allresultindex[department][semester] +=1
        resultdf.loc[resindex,"RegNumber"] = regno
        resultdf.loc[resindex,"Name"] = df['Student Name'][ind]
        coursecode = str(df['Course'][ind].split("-")[0])
        coursenames[coursecode] =  str(df['Course'][ind].split("-")[1])
        resultdf.loc[resindex,coursecode+"IMark"] = df['IMark'][ind]
        resultdf.loc[resindex,coursecode+"Grade"] = df['Grade'][ind]
        index=resultdf[resultdf["RegNumber"] == regno].index
        if ( isNaN(df['Withheld'][ind]) == False):
          resultdf.loc[index,"Status"] = "Withheld"
        #elif ( df['Result'][ind] == "F"):
            #resultdf.loc[index,"Status"] = "F"
        # elif ( df['Result'][ind] == "P"):
        #     resultdf.loc[index,"Status"] = "P"
      else:
        index=resultdf[resultdf["RegNumber"] == regno].index
        coursecode = str(df['Course'][ind].split("-")[0])
        resultdf.loc[index,coursecode+"IMark"] = df['IMark'][ind]
        resultdf.loc[index,coursecode+"Grade"] = df['Grade'][ind]
        if ( isNaN(df['Withheld'][ind]) == False):
          resultdf.loc[index,"Status"] = "Withheld"
        #elif ( df['Result'][ind] == "F"):
            #resultdf.loc[index,"Status"] = "F"
        #elif ( df['Result'][ind] == "P"):
            #resultdf.loc[index,"Status"] = "P"
        #print(resultdf.loc[index,"Status"])
  for dept in departments:
    excelfile=folder+"/Result-"+filenamewoext+"-"+dept+".xlsx"
    #excelfile=filenamewoext+"-"+dept+".xlsx"
    outfiles.append(excelfile)
    #print("Generating "+excelfile)
    if ( os.path.isfile(excelfile) == True ):
        os.remove(excelfile)
    if(1):
      print("Generating "+excelfile)
      writer = pd.ExcelWriter(excelfile)
      for sem in semesters:
        #filename=folder+dept+"-Sem-"+str(sem)+".csv"
        for ind in allresult[dept][sem].index:
          if ( ind <= numberOfCourses):
            #skip course name area 
            continue
          if(allresult[dept][sem].loc[ind,"Status"] == 'Withheld'):
            continue
          studentgrades=allresult[dept][sem].loc[ind].tolist()
          for grade in grades:
            allresult[dept][sem].loc[ind,grade+" Count"] = studentgrades.count(grade)
            #print(grade,studentgrades.count(grade))
        #allresult[dept][sem].to_csv(filename)
          if ( allresult[dept][sem].loc[ind,"F Count"] == 0):
            allresult[dept][sem].loc[ind,"Status"] = 'P'
          else:
              allresult[dept][sem].loc[ind,"Status"] = 'F'
        allresult[dept][sem].to_excel(writer,sheet_name="Sem-"+str(sem))
        writer.save()
        
    else:
      print("Excel File Exists(Delete it):"+excelfile)
  return outfiles
def send_document(update, context,file):
    chat_id = update.message.chat_id
    document = open(file, 'rb')
    context.bot.send_document(chat_id, document)
# adding the handler to handle the messages and commands  
the_updater.dispatcher.add_handler(CommandHandler('start', the_start))  
the_updater.dispatcher.add_handler(CommandHandler('youtube', youtubeURL))  
the_updater.dispatcher.add_handler(CommandHandler('help', the_help))  
the_updater.dispatcher.add_handler(CommandHandler('linkedin', linkedInURL))  
the_updater.dispatcher.add_handler(CommandHandler('gmail', gmailURL))  
the_updater.dispatcher.add_handler(CommandHandler('jtp', jtpURL))  
the_updater.dispatcher.add_handler(MessageHandler(Filters.text, unknownCommmand))  
 # Filtering out unknown commands  
the_updater.dispatcher.add_handler(MessageHandler(Filters.command, unknownCommmand))  
  
# Filtering out unknown messages  
the_updater.dispatcher.add_handler(MessageHandler(Filters.text, unknownText))  

the_updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader)) 
#the_updater.add_error_handler(error)
# running the bot  
the_updater.start_polling() 


