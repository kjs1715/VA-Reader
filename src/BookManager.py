class BaseBookManager:
  def __init__(self) -> None:
    pass

  

class GoogleBooksManager(BaseBookManager):
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
      time.sleep(3)
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


class LibgenManager(BaseBookManager):
  def __init__(self) -> None:
    super().__init__()
