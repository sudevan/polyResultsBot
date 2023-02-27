from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 ,landscape
from reportlab.lib.units import inch, cm
class TABill:
    def __init__(self,TAFile):
        packet = io.BytesIO()
        self.can = canvas.Canvas(packet, pagesize=landscape(A4))
        
        self.updateNewCanvas()
        self.can.save()
        packet.seek(0)

        #read the canvas into a pdf reader
        self.newpdf =  PdfReader(packet)
        

        #read the TA bill
        self.existing_pdf = PdfReader(open(TAFile, "rb"))
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
        self.can.drawString(x,y,data)
    def updateNewCanvas(self):
        basicPay = "56000"
        self.printString(17.6,3.86,basicPay)
        self.printString(.1,7.75,"GPC Palakkad")
        self.printString(3.1,7.75,"27/2/2023")
        