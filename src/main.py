from google.cloud import dialogflow_v2beta1 as df
from google.api_core.exceptions import InvalidArgument
from BookManager import GoogleBooksManager

import time
import requests
import urllib


# books imports
from libgen_api import LibgenSearch
import json
import PyPDF2 



'''
  Module for Google Dialogflow API

'''

DIALOGFLOW_PROJECT_ID = 'testingdialogflowapi'
DIALOGFLOW_LANGUAGE_CODE = 'English-en'
SESSION_ID = 'me'


class DialogflowManager:

  # session_client: Any
  # session: Any

  def __init__(self):
    self.session_client = df.SessionsClient()
    self.session = self.session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

  # for requesting to recognize users` intent
  def request_text(self, text):
    text_input = df.types.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = df.types.QueryInput(text=text_input)
    try:
      response = self.session_client.detect_intent(session=self.session, query_input=query_input)

      print(response.query_result)

      print("Query text:", response.query_result.query_text)
      print("Detected intent:", response.query_result.intent.display_name)
      print("Detected intent confidence:", response.query_result.intent_detection_confidence)
      print("Fulfillment text:", response.query_result.fulfillment_text)
    except InvalidArgument:
      raise




# module for google downloaded books
class BooksLibrary:
  def __init__(self):
    self.books = None


# single book entry class, requires PyPDF2
class Book:
  def __init__(self):

    self.title = ""
    self.author = ""
    self.pages = []
    self.pageCounts = -1

  def __init__(self, path):

    self.title = ""
    self.author = ""
    self.pages = []
    self.pageCounts = -1

    self.create_book(path)

  def create_book(self, path):
    if path is None:
      print("Book title or contents are empty...")
      return None

    # initialize book entry
    self.pageCounts, self.pages = self.parse_pdf(path)

    print(self.pages)

    # for line in lines
    #   self.pages.append()

  def parse_pdf(self, file_path):
    try:
      pdfFile = open(file_path, 'rb')
      pdfReader = PyPDF2.PdfFileReader(pdfFile)

      book_content = []
      for i in range(pdfReader.numPages):
        lines = self.get_lines(pdfReader, i)
        book_content.append(lines)

      return pdfReader.numPages, book_content
      

    except Exception as e:
      print(e)
      return None, None

  def get_lines(self, reader, index):
    return reader.getPage(index).extractText().split('.')




# test libgen
# s = LibgenSearch()
# results = s.search_title("Pride and Prejudice")
# item_to_download = results[1]
# download_links = s.resolve_download_links(item_to_download)
# print(download_links)
# print(download_links['GET'])

# gbm = GoogleBooksManager()
# gbm.download_file(download_links['GET'])



# test books api
# TODO: 

gbm = GoogleBooksManager()

# gbm.download_file(gbm.get_download_url(gbm.search_by_id("_mUCAAAAYAAJ")))




# test pdf translator
# pdfFileObj = open('book_example.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# print(pdfReader.numPages)
# pageObj = pdfReader.getPage(14)
# print(pageObj.extractText())

# pdfFileObj.close()


# test pdf translator to books
test_book = Book('test.pdf')



# test dialogflow
# dfm = DialogflowManager()
# dfm.request_text("read book")

