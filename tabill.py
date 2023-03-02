from PyPDF2 import PdfWriter, PdfReader
import io
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 ,landscape
from reportlab.lib.units import inch, cm
from reportlab.graphics.barcode import code128

class TABill:
    def __init__(self):
        self.state = "initial"
    def __init__(self,TAFile,template):

        #read date from the TA File

 

        packet = io.BytesIO()
        self.can = canvas.Canvas(packet, pagesize=landscape(A4))

        self.updateNewCanvas()

        reader = PdfReader(TAFile)
 

        page = reader.pages[0]
        
        # extracting text from page
        self.text = page.extract_text()

        self.extractText()
        self.can.save()
        packet.seek(0)

        #read the canvas into a pdf reader
        self.newpdf =  PdfReader(packet)
        

       

        #read the TA bill
        self.existing_pdf = PdfReader(open(template, "rb"))
        page = self.existing_pdf.pages[0]
        #merge with the gnerated file
        page.merge_page(self.newpdf.pages[0])

        #put it into a new pdf
        self.output = PdfWriter()
        self.output.add_page(page)
        

    def saveBill(self,outputfile):
        print("saving file",outputfile)
        output_stream = open(outputfile, "wb")
        self.output.write(output_stream)
        output_stream.close()
    def printString(self,x,y,data):
        x = (x+1.1)*cm
        y = (20.35 - y)*cm
        self.can.setFont("Helvetica", 9)
        self.can.drawString(x,y,data)
    def updateNewCanvas(self):
        # basicPay = "56000"
        # self.printString(17.6,3.86,basicPay)
        # self.printString(.1,7.75,"GPC Palakkad")
        # self.printString(3.1,7.75,"27/2/2023")
        pass

    def extractText(self):
        text = self.text
        
        # Regex patterns for extracting data from pdf
        officer_pattern = r"Name of Officer\s*:\s*(.*?)\s*Institution"
        mobile_no_pattern = r'Mobile No (\d{10})'
        bank_name_pattern =r"Bank\s*:\s*(.*?)\s*Bank"
        valuation_camp_regex = r"Institution\s+(.+)"
        camp_designation_regex = r"Camp Designation\s*:\s*(.*?)\s*Basic Pay"
        designation_regex = r"Designation\s*:\s*(.*?)\s*IFS Code"
        ifs_code_regex = r"IFS\s+Code\s+(\w+)"
        account_no_regex = r"Bank\s+Account\s+Number\s+(\w+)"


        name = re.search(officer_pattern,text)
        mobile_no = re.search(mobile_no_pattern,text)
        bank_name = re.search(bank_name_pattern,text)
        valuation_camp = re.search(valuation_camp_regex,text)
        camp_desg = re.search(camp_designation_regex,text)
        designation = re.search(designation_regex,text)
        ifs_code = re.search(ifs_code_regex,text)
        account_no = re.search(account_no_regex,text)
        
        print(name.group(1))
        print(mobile_no.group(1))
        print(bank_name.group(1))
        print(valuation_camp.group(1))
        print(camp_desg.group(1))
        print(ifs_code.group(1))
        print(account_no.group(1))

        # self.personal_datas['name'] = name.group(1)
        # self.personal_datas['mobile_no'] = mobile_no.group(1)
        # self.personal_datas['bank_name'] = bank_name.group(1)
        # self.personal_datas['valuation_camp'] = valuation_camp.group(1)
        # self.personal_datas['camp_desg'] = camp_desg.group(1)
        # self.personal_datas['ifs_code'] = ifs_code.group(1)
        # self.personal_datas['account_no'] = account_no.group(1)
        # self.personal_datas['designation'] = designation.group(1)

        # self.updateNewCanvas()
        self.printString(4.60,3.00,name.group(1))
        self.printString(4.60,3.60,camp_desg.group(1))
        self.printString(4.60,4.10,designation.group(1))
        self.printString(4.60,4.60,bank_name.group(1))


        self.printString(18.,4.10,ifs_code.group(1))
        self.printString(18.,4.60,account_no.group(1))


        self.printString(8.13,14.20,account_no.group(1)+" "+ifs_code.group(1)+" with " + bank_name.group(1))

        self.printString(24.40,15.35,name.group(1))

        self.printString(22.00,1.40,mobile_no.group(1))

        # qr = qrcode.QRCode(version=1, box_size=10, border=4)

        # qr.add_data(mobile_no.group(1))

        # qr.make(fit=True)

        # img = qr.make_image(fill_color="black", back_color="white")



        barcode = code128.Code128(mobile_no.group(1),barHeight=.3*inch,barWidth = 1.4)


        print(barcode)

        x = (20.59+1.1)*cm
        y = (20.35 - 0.65)*cm



        barcode.drawOn(self.can, x, y)







        








        # return self.personal_datas
