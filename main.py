import requests

request = requests.get(
    'https://query1.finance.yahoo.com/v7/finance/download/XISC.JK?period1=1587215758&period2=1618751758&interval=1d&events=history&includeAdjustedClose=true')
with open("XISC.JK.csv", "wb") as code:
    code.write(request.content)
