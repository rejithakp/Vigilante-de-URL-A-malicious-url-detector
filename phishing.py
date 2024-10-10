import os

from flask import Flask, render_template, request, session, redirect
from DBConnection import *
from werkzeug.utils import secure_filename
import phishing_detection
import nice

app = Flask(__name__)
app.secret_key="Remya"

UPLOAD_FOLDER= '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def login():
    return render_template("index.html")


@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login` WHERE `User_name`='"+username+"' AND `Password`='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['Login_id']
        if res['User_type']=='admin':
            return redirect('/ahome')
        elif res['User_type']=='user':
            return redirect('/uhome')
        else:
            return '''<script>alert("invalid user");window.location='/'</script>'''
    else:
        return '''<script>alert("invalid user");window.location='/'</script>'''

@app.route('/logout')
def logout():
    session['lid']=''
    return redirect('/login')

@app.route('/ahome')
def ahome():
    if session['lid']!='':
        return render_template("admin/index.html")
    else:
        return redirect('/login')

@app.route('/change_password')
def change_password():
    if session['lid'] != '':
        return render_template("admin/Change_password.html")
    else:
        return redirect('/login')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    currentpassword=request.form['textfield']
    newpassword=request.form['textfield2']
    confirmpassword=request.form['textfield3']
    db=Db()
    qry="SELECT * FROM `login` WHERE `Password`='"+currentpassword+"' AND `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if newpassword==confirmpassword:
            db=Db()
            qry1="update `login` set `Password`='"+confirmpassword+"' where `Login_id`='"+str(session['lid'])+"'"
            res1=db.update(qry1)

            return '''<script>alert("Password successfully changed");window.location='/'</script>'''
        else:
            return '''<script>alert("Password does not match");window.location='/change_password'</script>'''
    else:
      return  '''<script>alert("invalid user");window.location='/change_password'</script>'''



@app.route('/send_reply/<id>')
def send_reply(id):
    if session['lid'] != '':
        return render_template("admin/send_reply.html",id=id)
    else:
        return redirect('/login')


@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    id=request.form['cid']
    reply=request.form['textarea']
    db=Db()
    qry="UPDATE `complaint` SET `Reply`='"+reply+"',`Status`='Replied' WHERE `Complaint_id`='"+id+"'"
    res=db.update(qry)
    return '''<script>alert("Successfully Replied");window.location='/view_complaints'</script>'''


@app.route('/tips')
def tips():
    if session['lid'] != '':
        return render_template("admin/Tips.html")
    else:
        return redirect('/login')

@app.route('/tips_post',methods=['post'])
def tips_post():

    tips=request.form['textarea']
    db=Db()
    qry="INSERT INTO `tips`(`Tips`,`Date`)VALUES('"+tips+"',CURDATE())"
    res=db.insert(qry)
    return '''<script>alert("Successfully added");window.location='/ahome'</script>'''


@app.route('/view_complaints')
def view_complaints():
    if session['lid'] != '':

        db=Db()
        qry="SELECT * FROM Complaint JOIN `user` ON `complaint`.`User_id`=`user`.`Login_id`"
        res=db.select(qry)
        return render_template("admin/View_complaint.html",data=res)
    else:
        return redirect('/login')
@app.route('/view_complaint_post',methods=['post'])
def view_complaints_post():
    from_date=request.form['textfield']
    to_date=request.form['textfield2']
    db = Db()
    qry = "SELECT * FROM Complaint JOIN `user` ON `complaint`.`User_id`=`user`.`Login_id` WHERE `date` BETWEEN '"+from_date+"' AND '"+to_date+"'"
    res = db.select(qry)
    return render_template("admin/View_complaint.html", data=res)

@app.route('/view_feedback')
def view_feedback():
    if session['lid'] != '':

        db=Db()
        qry="SELECT * FROM feedback JOIN `user` ON `feedback`.`User_id`=`user`.`Login_id`"
        res=db.select(qry)
        return render_template("admin/View_feedback.html",data=res)
    else:
        return redirect('/login')


@app.route('/view_tips')
def view_tips():
    if session['lid'] != '':
        db=Db()
        qry="select * from tips"
        res=db.select(qry)
        return render_template("admin/view_tips.html",data=res)
    else:
        return redirect('/login')
@app.route('/delete_tips/<id>')
def delete_tips(id):
    if session['lid'] != '':
        db=Db()
        qry="DELETE FROM `tips` WHERE `Tip_id`='"+id+"'"
        res=db.delete(qry)
        return '''<script>alert("Deleted");window.location='/view_tips'</script>'''
    else:
        return redirect('/login')

#########################user




@app.route('/uhome')
def uhome():
    return render_template("user/u_index.html")


@app.route('/view_profile')
def view_profile():
    db=Db()
    qry="SELECT * FROM `user` WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("user/view_profile.html",data=res)



@app.route('/user_change_password')
def user_change_password():
    return render_template("user/changepassword.html")

@app.route('/user_change_password_post',methods=['post'])
def user_change_password_post():
    db=Db()
    current_password=request.form['textfield']
    new_password=request.form['textfield2']
    confirm_password=request.form['textfield3']
    qry = "SELECT * FROM `login` WHERE `Password`='" + current_password + "' AND `Login_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if new_password == confirm_password:
            db = Db()
            qry ="update `login` set `Password`='" + confirm_password + "' Where `Login_id`='" + str(session['lid']) + "'"
            res = db.update(qry)
            return '''<script>alert("Password successfully changed");window.location='/'</script>'''
        else:
            return '''<script>alert("Password does not match");window.location='/user_change_password'</script>'''
    else:
        return '''<script>alert("invalid user");window.location='/user_change_password'</script>'''

@app.route('/edit_profile')
def edit_profile():
    db=Db()
    qry="SELECT * FROM `user` WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)

    return render_template("user/edit_profile.html",data=res)

@app.route('/user_edit_profile',methods=['post'])
def user_edit_profile():
    db=Db()
    Name=request.form['textfield']
    Place=request.form['textfield2']
    Post=request.form['textfield3']
    Pin=request.form['textfield4']
    District=request.form['textfield5']
    Phone_no=request.form['textfield6']
    Gender=request.form['RadioGroup1']
    Email=request.form['textfield7']
    qry="UPDATE `user` SET `Name`='"+Name+"',`place`='"+Place+"',`post`='"+Post+"',`Pin`='"+Pin+"',`District`='"+District+"',`Phone_no`='"+Phone_no+"',`Gender`='"+Gender+"',`Email`='"+Email+"' WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.update(qry)


    return '''<script>alert("successfully updated");window.location='/view_profile'</script>'''

@app.route('/signup')
def signup():
    return render_template("user/registerindex.html")

@app.route('/signup_post',methods=['post'])
def signup_post():

    db=Db()
    Name=request.form['textfield']
    Place=request.form['textfield2']
    Post=request.form['textfield3']
    Pin=request.form['textfield4']
    District=request.form['textfield5']
    Phone_no=request.form['textfield6']
    Gender=request.form['RadioGroup1']
    Email=request.form['textfield7']
    Password=request.form['textfield8']
    Confirm_password=request.form['textfield9']
    if Password==Confirm_password:
        qry="INSERT INTO `login`(`User_name`,`Password`,`User_type`)VALUES('"+Email+"','"+Confirm_password+"','user')"
        res=db.insert(qry)
        qry2="INSERT INTO `user`(`Login_id`,`Name`,`place`,`post`,`Pin`,`District`,`Phone_no`,`Gender`,`Email`)VALUES('"+str(res)+"','"+Name+"','"+Place+"','"+Post+"','"+Pin+"','"+District+"','"+Phone_no+"','"+Gender+"','"+Email+"')"
        res2=db.insert(qry2)
        return '''<script>alert("success");window.location='/'</script>'''
    else:
        return '''<script>alert("incorrect password");window.location='/'</script>'''


@app.route('/user_view_feedback')
def user_view_feedback():
    db=Db()
    qry="SELECT * FROM `feedback` JOIN `user` ON `feedback`.`User_id`=`user`.`Login_id`"
    res=db.select(qry)
    return render_template("user/Feedback.html",data=res)


@app.route('/Send_complaint')
def Send_complaint():
    return render_template("user/Sendcomplaint.html")

@app.route('/Send_complaint_post',methods=['post'])
def Send_complaint_post():
    db=Db()
    complaint=request.form['textarea']
    qry="INSERT INTO `complaint`(`User_id`,`Complaint`,`Date`,`Time`,`Status`,`Reply`)VALUES('"+str(session['lid'])+"','"+complaint+"',CURDATE(),CURTIME(),'pending','pending')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/uhome'</script>'''

@app.route('/Send_feedback')
def Send_feedback():
    return render_template("user/Sendfeedback.html")

@app.route('/Send_feedback_post',methods=['post'])
def Send_feedback_post():
    feedback=request.form['textarea']
    db=Db()
    qry="INSERT INTO `feedback`(`User_id`,`Date`,`Time`,`Feedback`)VALUES('"+str(session['lid'])+"',CURDATE(),CURTIME(),'"+feedback+"')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/uhome'</script>'''


@app.route('/View_reply')
def View_reply():
    db=Db()
    qry="SELECT * FROM `complaint`WHERE `User_id`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("user/view_reply.html",data=res)

@app.route('/View_reply_post',methods=['post'])
def View_reply_post():
    return "ok"

@app.route('/user_view_tips')
def user_view_tips():
    db = Db()
    qry ="SELECT * FROM `tips`"
    res = db.select(qry)
    return render_template("user/view_tips.html",data=res)



@app.route('/user_detect')
def user_detect():
    print('hi')
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            contents = file.read()
            with open("files/URL.txt", "wb") as f:
                f.write(contents)
            file.save = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("index2.html")

    return render_template("user/index2.html")


@app.route('/predict',methods=["GET", "POST"])
def result():
    if request.method == "POST":
        url = request.form["url"]
        method=request.form["modelname"]
        print(method)
        data   = nice.getResult2(url,method)
        print(data)
        return render_template('user/result.html',data=data)
  #  url  = request.args['url']
  #  modelname  = request.args['modelname']
        # print(url,"haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        # if method=="logisticregression" or method=="RandomForest":
        #     data   = phishing_detection.getResult(url,method)
        #     print(data)
        #     return render_template('user/index2.html',data=data)
        # else:
        #     phishing_detection.getResult2(url,method)





if __name__ == '__main__':
    app.run(debug=True)
