from bottle import *
from glob import glob

@route('/hello')
def hello():
    return '<h1>' + "Hello World!" + '</h1>'

@route("/<path>")
def getthefile():
	print(path)
	return static_file(path, root=".")

@route ("/list")
def listt():
	#use glob: glob.glob("*.mp3") returns a list
	#for f in glob.glob()
		#do stuff
	for file in glob("*.mp3"):
		answer = ""
		print("Filename= " + file + "<br>")
		answer = answer + '<a href="' + file + '">' + file + '</a><BR>'
	return answer

@route ("/upload")
def upload():
	"""Upload file"""
	return '''
	<form action="" method="post" enctype="multipart/form-data">
	Select file: <input name = "file" type = "file">
	<input name = "Submit" type = "submit">
	</form>
	'''

if __name__ == '__main__':
	run(host='euclid.nmu.edu', port=9000, debug=True)
