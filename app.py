from flask import Flask ,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mytask.db"
db = SQLAlchemy(app)

class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,  nullable=False)
    email = db.Column(db.String)


with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        obj=Mytask(username= request.form["user"],email=request.form["email"])
        db.session.add(obj)
        db.session.commit()
    obj= Mytask.query.all()
       

    return render_template("index.html", obj=obj)

@app.route('/delete/<int:id>')
def delete(id):

    obj=Mytask.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
       

    return redirect("/")


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        username= request.form["user"]
        email=request.form["email"]
        obj1=Mytask.query.filter_by(id=id).first()
        obj1.username=username
        obj1.email=email
        db.session.add(obj1)
        db.session.commit()
        return redirect("/")
    obj1=Mytask.query.filter_by(id=id).first()
    return render_template("edit.html", obj1=obj1)


if __name__ == "__main__":
        app.run(debug=True,port=9000)

    