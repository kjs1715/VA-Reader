from crypt import methods
import os

from flask import Flask, request, send_from_directory


# create and configure the app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    # print(req)

    return {
        "fulfillmentText" : "Testing the webhook"
    }

if __name__ == "__main___":
    app.run()



