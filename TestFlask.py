from flask import Flask

app = Flask(__name__)


@app.route('/')
def Hello():
  return ''


@app.route('/webhook')
def webhook():
  return {
    'fulfillmentText' : 'Helloooo'
  }

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)