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
    def __init__(self,TAFile,template,data):
        #read date from the TA File
        print(data)
        packet = io.BytesIO()
        self.can = canvas.Canvas(packet, pagesize=landscape(A4))

        self.updateNewCanvas()


        self.data = data

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
    def printString(self,x,y,data,isBold=False):
        x = (x+1.1)*cm
        y = (20.35 - y)*cm
        if isBold:
            self.can.setFont("Helvetica-Bold", 10)
        else:
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

        travelling_start_date = self.data.get('before_date')
        travelling_end_date = self.data.get('after_date')


        self.printString(18.50,2.40,self.data.get('from_date'))
        self.printString(23.50,2.40,self.data.get('to_date'))

        self.printString(18.00,3.50,str(self.data.get('basic_pay')))

        self.printString(2.75,7.55,travelling_start_date)
        self.printString(2.75,8.20,travelling_start_date)
        self.printString(2.75,8.80,travelling_start_date)

        self.printString(9.60,7.55,travelling_start_date)
        self.printString(9.60,8.20,travelling_start_date)
        self.printString(9.60,8.80,travelling_start_date)


        self.printString(2.75,9.95,travelling_end_date)
        self.printString(2.75,10.55,travelling_end_date)
        self.printString(2.75,11.20,travelling_end_date)


        self.printString(9.60,9.95,travelling_end_date)
        self.printString(9.60,10.55,travelling_end_date)
        self.printString(9.60,11.20,travelling_end_date)


        self.printString(12.50,13.40,str(travelling_start_date))
        self.printString(20.80,13.40,str(travelling_end_date))



        





        self.printString(3.40,9.35,str(self.data.get('days')))
        self.printString(7.20,9.35,str(self.data.get('da_pay')))

        da_halt = int(self.data.get('da_pay') * self.data.get('days'))

        



        self.printString(20.00,8.10,str(int(self.data.get('da_pay')/2)))
        
        self.printString(24.00,8.10,str(int(self.data.get('da_pay')+460)))

        self.printString(21.60,9.35,str(da_halt))
        self.printString(24.00,9.35,str(da_halt))




        self.printString(20.00,10.60,str(int(self.data.get('da_pay')/2)))
        self.printString(24.00,10.60,str(int(self.data.get('da_pay')+460)))

        total = int(1380 + da_halt + self.data.get('da_pay'))

        self.printString(23.90,11.80,str(total),isBold=True)








        
        self.printString(4.70,3.00,name.group(1))
        self.printString(4.70,3.60,camp_desg.group(1))
        self.printString(4.70,4.10,designation.group(1))
        self.printString(4.70,4.60,bank_name.group(1))


        self.printString(18.,4.10,ifs_code.group(1))
        self.printString(18.,4.60,account_no.group(1))


        self.printString(7.30,14.00,account_no.group(1)+" "+ifs_code.group(1)+" with " + bank_name.group(1))

        self.printString(24.10,15.20,name.group(1))

        self.printString(22.00,1.40,mobile_no.group(1))

        barcode = code128.Code128(mobile_no.group(1),barHeight=.3*inch,barWidth = 1.6)
        print(barcode)

        x = (20.59+1.1)*cm
        y = (20.35 - 0.65)*cm
        barcode.drawOn(self.can, x, y)

