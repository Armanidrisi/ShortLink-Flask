from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random 

app = Flask(__name__)
BASE_URL="http://localhost:5000" #need to change in production 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(350))
  linkid = db.Column(db.String(50))
  
  def __repr__(self):
    return '<linkid %r>' % self.linkid


def getid():
  return "".join(random.sample("abcdefghijklmnopqrstuvwxlmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXLMNOPQRSTUVWXYZ",6))

@app.route("/",methods=["GET","POST"])
def homepage():
  
  if request.method == "POST":
    
    url = request.form.get("url")
    
    if url == "":
      return render_template("index.html",message="Please Provide URL")
    old = Url.query.filter_by(url=url).first()
    
    if old is None:
      linkid = getid()
      u = Url(url=url,linkid=linkid)
      db.session.add(u)
      db.session.commit()
      return render_template("index.html",message=f"Generated Url: {BASE_URL}/short/{linkid}")
    else:
      linkid = old.linkid
      return render_template("index.html",message=f"Generated Url: {BASE_URL}/short/{linkid}")
  
  return render_template("index.html")
  
  
@app.route("/short/<linkid>")
def redirect_url(linkid):
    url = Url.query.filter_by(linkid=linkid).first()
    if url:
        return redirect(url.url)
    else:
        return "Oops! This Url Not Found"
  
  
@app.route("/about")
def send_about():
  return render_template("about.html")


if __name__ == "__main__":
  app.run(debug=True)