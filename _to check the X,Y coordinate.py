import os
import glob
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from cStringIO import StringIO


directory = os.path.abspath('')
#Enter the files name here or the path.
filename='.pdf'
pdfFiles = glob.glob(os.path.join(directory, filename))

resourceManager = PDFResourceManager()
returnString = StringIO()
codec = 'utf-8'
laParams = LAParams()
device = PDFPageAggregator(resourceManager, laparams=laParams)
interpreter = PDFPageInterpreter(resourceManager, device)


maxPages = 0
caching = True
pageNums=set()

for one_pdf in pdfFiles:
    print("Processing file: " + str(one_pdf))
    fp = file(one_pdf, 'rb')
    name = "one_pdf"

    lst =[]
    def parse_obj(lt_objs):
        for one_pdf in enumerate(pdfFiles):
            for obj in lt_objs:
                if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                    print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_'))
                    
                    lst.append([one_pdf,[[obj.bbox[0],obj.bbox[1]], obj.get_text()]])

                elif isinstance(obj, pdfminer.layout.LTFigure):
                    parse_obj(obj._objs)

    for page in PDFPage.get_pages(fp, pageNums, maxpages=maxPages,caching=caching, check_extractable=True):

            interpreter.process_page(page)
            layout = device.get_result()

            parse_obj(layout._objs)

device.close()
returnString.close()
