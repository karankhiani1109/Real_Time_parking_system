import pymongo
from flask import Flask, redirect, url_for, request, render_template , send_file

myclient= pymongo.MongoClient("mongodb://utkarsh1:utkarsh123@ds129233.mlab.com:29233/parking_system")
db=myclient.get_default_database()
registration=db['registration']
parkd=db['parkd']
# def data_input(url):

# mycursor = mydb.cursor()
app = Flask(__name__)

@app.route('/registered')
def registered():
    return render_template('login.html')


@app.route('/data' ,methods=['POST','GET'])
def data():
    if request.method == 'POST':
        name=request.form['name']
        carid=request.form['carid']
        time=request.form['time']
        duration=request.form['dur']
        slot=request.form['Slot']

        # password=request.form['passwordr']
        # email=request.form['emailr']
        # parkd.ensure_index("date")
        parkd.insert({'name':name,'carno':carid,'time':time,'duration':duration,'slot':slot})
        # sql = "INSERT INTO registration VALUES(%s, %s, %s)"
        # val = (username,password,email)
        print (carid)
        # mycursor.execute(sql,val)
        # mydb.commit()
    else:
        print ("notfound")
    return "inserted"    

@app.route('/booklist/<string:id>')
def booklist(id):
    dict=[]
    t=parkd.find()
    
    for i in t:
        if(i['name']==id):
            dict={"name":id,"duration":i['duration'],"carno":i['carno'],"time":i['time'],"slot":i['slot']}
            return render_template('booklist.html',result=dict)
            break
    return "no record "        

@app.route('/url' ,methods=['POST','GET'])
def url():
    if request.method == 'POST':
        username=request.form['usernamer']
        password=request.form['passwordr']
        email=request.form['emailr']
        registration.insert({'username':username,'password':password,'email':email})
        # sql = "INSERT INTO registration VALUES(%s, %s, %s)"
        # val = (username,password,email)
        print (username)
        # mycursor.execute(sql,val)
        # mydb.commit()
    else:
        print ("notfound")
    return "registered"    
@app.route('/login' ,methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username=request.form['usernamel']
        password=request.form['passwordl']
        t=registration.find()
        
        dict=[]
        slt=[]
        for row in t:
            if row['username']==username and row['password']==password:
                sl=1
                while sl<9:
                    c=0
                    t1=parkd.find()
                    for j in t1:
                        print(j)
                        # print(str(sl))
                        # print(j['slot'])
                        if(str(sl)==(j['slot'])):
                            c=1
                            print(sl)
                    if c==0:
                        slt.append(sl)
                    sl=sl+1         
                dict={'name':username,'slotlist':slt}            
                return render_template('parknow.html',result=dict)


    return "Sorry. Try again." 
if __name__ == '__main__':
    app.debug=True
    app.run()
