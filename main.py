
from time import strftime
from os import name
from flask import Flask,render_template, request,redirect,url_for,session
import sqlite3,smtplib,random,time
from flask import flash

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS login2(username TEXT ,email TEXT,password TEXT ,id TEXT) ')
cur.execute('CREATE TABLE IF NOT EXISTS comment(username TEXT ,comment TEXT,date TEXT,id TEXT) ')
app = Flask(__name__)
app.secret_key = '2141#frq'
@app.route('/su',methods = ['POST', 'GET'])
def signup():
   if request.method=='POST':
      
      username=request.form['username']
      password=request.form['pass']
      email=request.form['email']

      conn = sqlite3.connect('database.db')
      conn.row_factory = sqlite3.Row
   
      cur = conn.cursor()
      #cur.execute('DROP TABLE IF EXISTS login')
      cur.execute("select * from login2")
      username23=[]
      rows = cur.fetchall();

      for row in rows:
         username23.append(row['username'])
      if username and password:
         if username in username23:
            flash('this username is taken')
         else:
            flash('You have created an account!')
            time.sleep(2)
            conn = sqlite3.connect('database.db')
            cur=conn.cursor()
            cur.execute('''INSERT INTO login2 (username,email,password,id) VALUES(?,?,?,?)''',(username,email,str(password),'first'))
            conn.commit()
            return redirect('/')

            


            

      else:
         flash('please fill all fields')
      #conn.execute('UPDATE students SET name ="yara" WHERE name="ahmadalmaaz"')
      ##conn.execute('DELETE FROM students WHERE city = "12"')
      
      conn.commit()
      conn.close()
      
       
      
      return render_template('signuppage.html')
   else:
      
      return render_template('signuppage.html')
@app.route('/verification',methods = ['POST', 'GET'])
def verification(): 
   #if 'email' in session and 'password' in session:
   if False:
      global i
      email=session['email']
      password=session['password']
      username=session['username']
      
      if i==0:
         with smtplib.SMTP("smtp.outlook.com",587) as smtp:
            global key
            key= str(random.randint(1,9))+str(random.randint(1,9)) +str(random.randint(1,9)) + str(random.randint(1,9)) 
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login("ahmd_maaz05@outlook.com","DC8E6A353MMZ")

            subject = 'Email verification'
            msg= f'Subject: {subject} \n\n {key}'
            
            smtp.sendmail("ahmd_maaz05@outlook.com",email,msg)
            i+=1
      if request.method=="POST":
         code=request.form['code']
         if code==key:
            conn = sqlite3.connect('database.db')
            cur=conn.cursor()
            cur.execute('''INSERT INTO login2 (username,email,password,id) VALUES(?,?,?,?)''',(username,email,str(password),'first'))
            conn.commit()
            session.pop('username',None)
            session.pop('password',None)
            session.pop('email',None)
            return redirect('/')
      return render_template('verification.html',email=email)
   else:
      return redirect('/su')
   

@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method=='POST':
      username=request.form['username']
      password=request.form['pass']
      session['username']=username
      conn = sqlite3.connect('database.db')
      conn.row_factory = sqlite3.Row
      cur=conn.cursor()
      cur.execute("select * from login2")
      rows= cur.fetchall();
      namepass=[]
      for row in rows:
        namepass.append(row['username']+row['password'])
      if username and password:
         if username+password in namepass:
            session['enter']=True
            session.pop('_flashes', None)
            return redirect('/home')
            
         else:
            session.pop('_flashes', None)
            flash('Username or password is incorrect')
      else:
         session.pop('_flashes', None)
         flash('please fill all fields')

      return render_template('login.html')
   return render_template('login.html')
   
   
@app.route('/list')
def list():
   if 'databaseaccess' in session:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      
      cur = con.cursor()
      cur.execute("select * from login2")
      
      rows = cur.fetchall();
      cur.execute('select * from comment')
      rows2=cur.fetchall();
      return render_template("list.html",rows = rows,rows2=rows2)
   else: 
      return redirect('/')
@app.route('/home',methods = ['POST', 'GET'])
def homepage():
   if 'enter' in session:
      if request.method=='POST':
         form_name = request.form['form']
         if form_name=='form1':
            code=request.form['code']
            if len(code)==4:
               if code=='4269':
                  session['databaseaccess']='true'
                  return redirect('/list')
         elif form_name=='form2':
            comment=request.form['comment']
            username=session['username']
            con = sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute('''INSERT INTO comment (username,comment,date,id) VALUES(?,?,?,?)''',(username,comment,strftime('%H:%M:%S %p') ,'first'))
            con.commit()
            
      time.sleep(1.5)
      return render_template('home.html')
   else:
      
      return redirect('/')
@app.route('/playxo')
def playxo():
   if 'enter' in session:
      return render_template('xo.html')
   else:
      return redirect('/')
@app.route('/playrps')
def playrps():
   if 'enter' in session:
      return render_template('rockpaperscissors.html')
   else:
      return redirect('/')
if __name__ == '__main__':
   app.run()


