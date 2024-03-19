from encrypt_k7s2 import encrypter, decrypter
from flask import Flask, request, jsonify
import requests
# from VertexClient import dbORM
import __trash

from_ = "http://127.0.0.1:2781"
# from_ = "https://vertexdb.pythonanywhere.com"

dbview = Flask(__name__)

def getDBRaw():
	def request_then_text(url):
		req = requests.get(url)
		return req.text
	
	return request_then_text(url=f'{from_}/handler/get-db-raw/{__trash.retTr()}')

@dbview.route("/query-ask-table")
def showDBPage():
	
	return """
<title>SJView</title>
<p>What Table?</p>
<form action="/show-result" method="POST">
	<input type="text" name="table_name">
	<button>Submit</button>
</form>
	"""

@dbview.route("/show-result", methods=['GET', 'POST'])
def showResult():
	if request.method == 'POST':
		try:
			return jsonify(eval(requests.get(f'{from_}/handler/get-all/{__trash.retTr()}/{encrypter(request.form["table_name"])}').text))
		except SyntaxError:
			return f"""<title>SJView</title><p>[ERROR]: TABLE '{request.form['table_name']}' DOESN'T EXIST</p>"""

	return decrypter(getDBRaw())

dbview.run(debug=True, host="127.0.0.1", port="2024")