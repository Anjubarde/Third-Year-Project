from flask import Flask, render_template, request, redirect,url_for, session
from flask_sqlalchemy import SQLAlchemy
import jinja2

app = Flask(_name_, template_folder='path/to/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)

class Studata(db.Model):
    Aadhar_Card_No = db.Column(db.Integer(), primary_key=True)
    Student_Name = db.Column(db.String(20), unique=False, nullable=False)
    Class = db.Column(db.String(20), unique=False, nullable=False)

@app.route("/")
def home():
    db.create_all()
    try:
            return render_template("home.html")
    except jinja2.exceptions.TemplateNotFound as e:

       return f"Template not found: {e}"
    # return render_template("home.html")


@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        Student_Name = request.form.get('Student_Name')
        Aadhar_Card_No = request.form.get('Aadhar_Card_No')
        Class = request.form.get('Class')

        entry = Studata(Student_Name=Student_Name, Aadhar_Card_No=Aadhar_Card_No, Class=Class)

        db.session.add(entry)
        db.session.commit()
    return render_template('index.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # Get the primary key value from the form or URL
        Aadhar_Card_No = request.form.get('Aadhar_Card_No')
        entry = Studata.query.get(Aadhar_Card_No)
        if entry:
            entry.Student_Name = request.form.get('Student_Name')
            entry.Class = request.form.get('Class')
            db.session.commit()
    return render_template('update.html')

@app.route('/delete/<Aadhar_Card_No>')
def delete(Aadhar_Card_No):
    entry = Studata.query.get(Aadhar_Card_No)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('home'))


if _name_ == "_main_":
    app.run(debug=True)