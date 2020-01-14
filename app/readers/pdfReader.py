# PDFMiner
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

import io
import requests


def reader(url):
    r = requests.get(url)
    data = io.BytesIO(r.content)

    # Create parser object to parse the pdf content
    parser = PDFParser(data)

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser)

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources
    # such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted
    # information into desired format
    # Device to connect to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared
    # resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Initialize the text
    extracted_text = ""

    # Ok now that we have everything to process a pdf document,
    # lets process it page by page
    for page in PDFPage.create_pages(document):
        # As the interpreter processes the page stored in PDFDocument
        # object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested
        # in LTTextBox and LTTextLine
        for lt_obj in layout:
            if (isinstance(lt_obj, LTTextBox) or
                    isinstance(lt_obj, LTTextLine)):
                extracted_text += lt_obj.get_text()

    return extracted_text
