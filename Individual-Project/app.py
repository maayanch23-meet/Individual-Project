from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
	"apiKey" : "AIzaSyBP6AkN_CdrLJbevi9srOPtrdwXgwfGNps",
	"authDomain" : "cs-project-af5ad.firebaseapp.com",
	"projectId" : "cs-project-af5ad",
	"storageBucket" : "cs-project-af5ad.appspot.com",
	"messagingSenderId" : "213710981406",
	"appId" : "1:213710981406:web:33141b3eaff556b721210f",
	"measurementId" : "G-R8HYBM3MEG", "databaseURL" : "https://cs-project-af5ad-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		user = {'username' : request.form['username'], 'fullname' : request.form['fullname']}
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/home', methods = ['GET', 'POST'])
def home():
	if request.method == 'POST':
		try:
			task = {request.form['task'] : "val"}
			db.child("Users").child(login_session['user']['localId']).child('Tasks').update(task)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("home.html")

@app.route('/to_do_list')
def to_do_list():
	task = db.child("Users").child(login_session['user']['localId']).child("Tasks").get().val()
	if task == None:
		task = []
	return render_template("todolist.html", user_task = task)

@app.route('/delete/<string:user_task>', methods = ['GET','POST'])
def delete(user_task):
	try:
		db.child("Users").child(login_session['user']['localId']).child("Tasks").child(user_task).remove()
		return redirect(url_for('to_do_list'))
	except:
		error = "Couldn’t remove object"
	return redirect(url_for('to_do_list'))



#Code goes above here

if __name__ == '__main__':
	app.run(debug=True)