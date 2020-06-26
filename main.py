# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import flask
from flask import Flask, request
import json
import random

app = Flask(__name__)

# Firefox session
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

@app.route('/')
def home():
    return "Welcome to the Quotes Microservice"

@app.route('/quotes', methods = ['GET'])
def get_quotes():
    error = None

    # get query value
    keyword = request.args.get('query')

    quotes = get_quotes_list(keyword)

    if not quotes:
        error = "No quotes found"
        return error

    # prepare response
    resp =  flask.Response(json.dumps(quotes))
    resp.headers["Content-Type"] = "application/json"
    return resp

@app.route('/quote', methods = ['GET'])
def get_quote():
    error = None

    # get query value
    keyword = request.args.get('query')
    quotes = get_quotes_list(keyword)

    if not quotes:
        error = "No quotes found"
        return error

    # pick random quote
    rand_index = random.randrange(0,len(quotes))
    quote = quotes[rand_index]

    # prepare response
    resp =  flask.Response(quote)
    resp.headers["Content-Type"] = "text/html"
    return resp

def get_quotes_list(search_kw):
    # urls
    entry_url = f"https://www.azquotes.com/quotes/topics/{search_kw}.html"

    driver.get(entry_url)
    driver.implicitly_wait(100)

    # for elem in driver.find_elements_by_class_name("title"):
    bs_instance = BeautifulSoup(driver.page_source, 'html.parser')
    a_elements = bs_instance.find_all('a', attrs={'class': 'title'})

    quotes = list(map(lambda elem: elem.get_text().replace("\n", ""), a_elements))

    return quotes
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)