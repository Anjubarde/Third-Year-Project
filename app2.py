from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'


db = SQLAlchemy(app)


class Cake(db.Model):
    product = db.Column(db.String(20), primary_key=True)
    rate = db.Column(db.Integer(), unique=False, nullable=False)
    per = db.Column(db.String(5), unique=False, nullable=False)


@app.route("/")
def home():
    cakes = Cake.query.all()
    return render_template('home.html', cakes=cakes)


@app.route("/add", methods=['POST', 'GET'])
def addInfo():
    try:

        if request.method == 'POST':
            'add entry to DB'

            product = request.form.get('product')
            rate = request.form.get('rate')
            per = request.form.get('per')

            entry = Cake(product=product, rate=rate, per=per)
            db.create_all()
            db.session.add(entry)
            db.session.commit()

        return render_template('add.html')

    except Exception as e:
        return redirect(url_for('home'))


@app.route('/home/delete/<string:product>', methods=['POST', 'GET'])
def delete(product):
    entry = Cake.query.get(product)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update/<string:product>', methods=['GET', 'POST'])
def update(product):
    try:
        cake = Cake.query.get(product)

        if request.method == 'POST':
            rate = request.form.get('rate')
            per = request.form.get('per')

            if rate:
                cake.rate = rate
            if per:
                cake.per = per

            db.session.commit()

            # return redirect(url_for('update', product=product))

        return render_template('update.html', cake=cake)

    except Exception as e:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
