from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app =  Flask('__name__')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/restaurant"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Menu(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   item = db.Column(db.String(80), unique=True, nullable=False)
   price = db.Column(db.String(120), nullable=False)
   qty = db.Column(db.Integer, nullable=False)

   def __repr__(self):
      return "My name is {}, price {} with quantity in {}gms".format(self.item, self.price, self.qty)

class Order(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   item = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
   date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

   def __repr__(self):
      return "My order is {}, date {}".format(self.item, self.date)

@app.route('/menu', methods=['POST', 'GET'])
def Add_Menu_Item():
   if request.method == 'POST':
      menuItem = Menu(
         item=request.form.get('item'),
         price=request.form.get('price'),
         qty=request.form.get('qty')
      )
      db.session.add(menuItem)
      db.session.commit()
      return redirect(url_for('res_taken'))
   
   return render_template('addMenu.html')

@app.route('/')
def res_taken():
   items = Menu.query.all()
   return render_template('index.html', items = items)

@app.route('/save')
def save_form():
   print(request.form)
   return 'done'

@app.route('/order/<int:id>')
@app.route('/order/')
def take_order(id = None):
   if id is not None:
      db.session.add(Order(item=id))
      db.session.commit()

   return render_template('orders.html', orders = Order.query.all())

@app.route('/delete/<int:id>')
def delete_order(id):
   orderItem = Order.query.filter_by(id = id).first()
   db.session.delete(orderItem)
   db.session.commit()
   return redirect(url_for('take_order'))

if __name__ == '__main__':
    app.run(debug=True)
