from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index1.html', data=items)


@app.route('/create1', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "Получилась ошибка"
    else:
        return render_template('create1.html')


@app.route('/about1')
def about():
    return render_template('about1.html')


@app.route('/oplat')
def promo():
    return render_template('oplat.html')


@app.route('/dost')
def dost():
    return render_template('dost.html')


@app.route('/uslov')
def uslov():
    return render_template('uslov.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=123456789,
              secret_key='YOUR_KEY')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": item.price
    }
    url = checkout.url(data).get('checkout_url')
    return url


@app.route('/confid')
def config():
    return render_template('confid.html')


if __name__ == "__main__":
    app.run()
