from google.cloud import dialogflow_v2beta1 as df
from google.api_core.exceptions import InvalidArgument

import time
import requests
import urllib


# books imports
from libgen_api import LibgenSearch
import json
import PyPDF2 



# for simulating chrome
from selenium import webdriver


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

  def 



class GoogleBooksManager:
  '''
    Module for Google books API
  '''

  def __init__(self):

    self.BOOKS_API_KEY = 'AIzaSyBp8-9rxUGOkZBxcqUf8-tsmPEAcCJrzVE'
    self.KEY_QUERY = '&key=' + self.BOOKS_API_KEY
    self.BOOK_TITLE_QUERY = 'little+prince'
    self.BOOK_ID = '_mUCAAAAYAAJ'

    self.DEFAULT_API = 'https://www.googleapis.com/books/v1/volumes'
    self.BOOKS_SEARCH_API = 'https://www.googleapis.com/books/v1/volumes/'
    self.BOOKS_ID_SEARCH_API = 'https://www.googleapis.com/books/v1/volumes/'

  # return the list of query searching results
  def search_query(self, query):

    try:
      params = dict(
        key=self.BOOKS_API_KEY,
        filter=['full', 'free-ebooks'],
        maxResults=1,
        q=query
      )
      req = requests.get(url=self.DEFAULT_API, params=params)
      data = req.json()
      # print(data)

      return data['items']
    except BaseException: 
        raise

  def search_by_id(self, id):
    try:
      params = dict(
        key=self.BOOKS_API_KEY
      )
      res = requests.get(url=self.DEFAULT_API + '/' + id, params=params)
      data = res.json()
      # print(data)

      return data
    except BaseException: 
        raise


  def get_download_url(self, book):
    if book['accessInfo'] is None:
      print('No accessInfo for ' + book['id'] + ' volume...')
      return None

    pdf_info = book['accessInfo']['pdf']
    isAvailable = pdf_info['isAvailable']
    # TODO: try pdf and epub version, compare
    if isAvailable is False:
      print("pdf ver download url does not exist for book_id " + book['id'])
      return None

    download_url = pdf_info['downloadLink']
    print(download_url)
    return download_url
    
  def download_file(self, url):
    if url is None:
      print("downlaod url is None")
      return None
    
    try:
      head_req = requests.get("https://books.google.com/books/download/")
      header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.00',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close', 
        'referer':'https://www.google.com/',
        # 'Cookie': "NID=" + str(head_req.cookies['NID']),
      }
      time.sleep(3)

      # TODO: sth wrong with requests
      # res = requests.get(url=url, headers=header)
      # data = res.content;

      # pdf = open("test"+".pdf", 'wb')
      # pdf.write(res.content)
      # pdf.close()

      res = urllib.request.urlopen(url)
      local_file = open('test.pdf', 'wb')
      local_file.write(res.read())
      local_file.close()


    except Exception as e:
      # if 'captcha'.encode() in res.content:
      #   print('Banned from google')
      # else:
        print(e)



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

# test books api
# TODO: 

# gbm = GoogleBooksManager()
# gbm.download_file(gbm.get_download_url(gbm.search_by_id("_mUCAAAAYAAJ")))


# test pdf translator
# pdfFileObj = open('book_example.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# print(pdfReader.numPages)
# pageObj = pdfReader.getPage(14)
# print(pageObj.extractText())

# pdfFileObj.close()


# test pdf translator to books
# test_book = Book('book_example.pdf')



# test dialogflow
# dfm = DialogflowManager()
# dfm.request_text("read book")


# test libgen
s = LibgenSearch()
results = s.search_title("Pride and Prejudice")
item_to_download = results[1]
download_links = s.resolve_download_links(item_to_download)
print(download_links)
print(download_links['GET'])

gbm = GoogleBooksManager()
gbm.download_file(download_links['GET'])