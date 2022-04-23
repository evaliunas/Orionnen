import pandas as pd
from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
import upload_file
import dashboard

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'amberlabs.db')
db = SQLAlchemy(app)

class Sales(db.Model):
    __tablename__ = 'Sales'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    sku = db.Column(db.Text)
    buyer = db.Column(db.Text)
    date = db.Column(db.Date)
    revenue = db.Column(db.Float)
    refund = db.Column(db.Float)
    net_revenue = db.Column(db.Float)
    proc_fee = db.Column(db.Float)
    cred_proc_fee = db.Column(db.Float)
    net_proc_fee = db.Column(db.Float)
    trans_trans_fee = db.Column(db.Float)
    cred_trans_trans_fee = db.Column(db.Float)
    ship_trans_fee = db.Column(db.Float)
    cred_ship_trans_fee = db.Column(db.Float)
    ad_fee = db.Column(db.Float)
    cred_ad_fee = db.Column(db.Float)
    net_ad_fee = db.Column(db.Float)
    vat_ad = db.Column(db.Float)
    cred_vat_ad = db.Column(db.Float)
    vat_proc_fee = db.Column(db.Float)
    cred_vat_proc_fee = db.Column(db.Float)
    vat_trans = db.Column(db.Float)
    cred_vat_trans = db.Column(db.Float)
    vat_ship_trans = db.Column(db.Float)
    cred_vat_ship_trans = db.Column(db.Float)
    tax = db.Column(db.Float)
    cred_tax = db.Column(db.Float)
    net_tax = db.Column(db.Float)
    trans_fee = db.Column(db.Float)
    cred_trans_fee = db.Column(db.Float)
    net_trans_fee = db.Column(db.Float)
    vat = db.Column(db.Float)
    cred_vat = db.Column(db.Float)
    net_vat = db.Column(db.Float)
    etsy_costs = db.Column(db.Float)
    prod_costs = db.Column(db.Float)
    ship_costs = db.Column(db.Float)
    undef_costs = db.Column(db.Float)
    other_costs = db.Column(db.Float)
    costs = db.Column(db.Float)
    profit = db.Column(db.Float)
    note = db.Column(db.Text)
    status = db.Column(db.Text)

    def __init__(self,
                 order_id, date, sku='', buyer='', note='', status='Ordered',
                 revenue=0, refund=0, net_revenue=0,
                 proc_fee=0, cred_proc_fee=0, net_proc_fee=0,
                 trans_trans_fee=0, cred_trans_trans_fee=0,
                 ship_trans_fee=0, cred_ship_trans_fee=0,
                 ad_fee=0, cred_ad_fee=0, net_ad_fee=0,
                 vat_ad=0, cred_vat_ad=0,
                 vat_proc_fee=0, cred_vat_proc_fee=0,
                 vat_trans=0, cred_vat_trans=0,
                 vat_ship_trans=0, cred_vat_ship_trans=0,
                 tax=0, cred_tax=0, net_tax=0,
                 trans_fee=0, cred_trans_fee=0, net_trans_fee=0,
                 vat=0, cred_vat=0, undef_costs=0, net_vat=0, other_costs=0,
                 etsy_costs=0, prod_costs=0, ship_costs=0, costs=0, profit=0):
        self.order_id = order_id
        self.date = date
        self.sku = sku
        self.buyer = buyer
        self.note = note
        self.status = status
        self.revenue = revenue
        self.refund = refund
        self.net_revenue = net_revenue
        self.proc_fee = proc_fee
        self.cred_proc_fee = cred_proc_fee
        self.net_proc_fee = net_proc_fee
        self.trans_trans_fee = trans_trans_fee
        self.cred_trans_trans_fee = cred_trans_trans_fee
        self.ship_trans_fee = ship_trans_fee
        self.cred_ship_trans_fee = cred_ship_trans_fee
        self.ad_fee = ad_fee
        self.cred_ad_fee = cred_ad_fee
        self.net_ad_fee = net_ad_fee
        self.vat_ad = vat_ad
        self.cred_vat_ad = cred_vat_ad
        self.vat_proc_fee = vat_proc_fee
        self.cred_vat_proc_fee = cred_vat_proc_fee
        self.vat_trans = vat_trans
        self.cred_vat_trans = cred_vat_trans
        self.vat_ship_trans = vat_ship_trans
        self.cred_vat_ship_trans = cred_vat_ship_trans
        self.tax = tax
        self.cred_tax = cred_tax
        self.net_tax = net_tax
        self.trans_fee = trans_fee
        self.cred_trans_fee = cred_trans_fee
        self.net_trans_fee = net_trans_fee
        self.vat = vat
        self.cred_vat = cred_vat
        self.net_vat = net_vat
        self.etsy_costs = etsy_costs
        self.prod_costs = prod_costs
        self.ship_costs = ship_costs
        self.undef_costs = undef_costs
        self.other_costs = other_costs
        self.costs = costs
        self.profit = profit

db.create_all()

@app.route('/')
def home():
    month = 'all'
    try:
        data = dashboard.calculate(month)
        dataset = dashboard.linechart(month)
        dates = dataset[0]
        profits = dataset[1]
    except:
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dates = []
        profits = []
    return render_template("index.html", data=data, month=month, dates=dates, profits=profits)

@app.route('/dashboard/month=<month>', methods=['GET', 'POST'])
def show_dashboard(month):
    try:
        data = dashboard.calculate(month)
        dataset = dashboard.linechart(month)
        dates = dataset[0]
        profits = dataset[1]
    except:
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dates = []
        profits = []
    return render_template("index.html", data=data, month=month, dates=dates, profits=profits)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    rows = 0
    if request.method == 'POST':
        try:
            df = pd.read_csv(request.files.get('csvfile'))
            rows = df.shape[0]
            upload_file.upload_data(df, rows)
            return render_template("upload.html", rows=rows)
        except:
            return render_template("upload_fail.html")
    else:
        return render_template("upload.html", rows=rows)

@app.route('/orders', methods=['GET', 'POST'])
def show_orders():
    sales = db.session.query(Sales).order_by(Sales.date.desc())
    month = 'all'
    return render_template("orders.html", sales=sales, month=month)

@app.route('/orders/month_<month>', methods=['GET', 'POST'])
def show_filtered_orders(month):
    sales = db.session.query(Sales).filter(Sales.date.between(f'2022-{month}-01', f'2022-{month}-31')).order_by(Sales.date.desc())
    return render_template("orders.html", sales=sales, month=month)

@app.route('/orders/month_<month>/status=<status>', methods=['GET', 'POST'])
def show_orders_status(status, month):
    if month != 'all':
        sales = db.session.query(Sales).filter(Sales.date.between(f'2022-{month}-01', f'2022-{month}-31'), Sales.status == status).order_by(Sales.date.desc())
    else:
        sales = db.session.query(Sales).filter(Sales.status == status).order_by(Sales.date.desc())
    return render_template("orders.html", sales=sales)

@app.route('/orders/id_<order_id>', methods=['GET', 'POST'])
def view_order(order_id):
    sale = Sales.query.filter_by(order_id=order_id).first()
    if request.method == "POST":
        try:
            note = request.form['note']
            if note == "":
                note = "No note"
            sale.note = note
            db.session.commit()
            upload_file.update_data()
            return render_template("edit_order_success.html", sale=sale)
        except:
            db.session.rollback()
            return render_template("edit_order_fail.html", sale=sale)
    if request.method == "GET":
        return render_template("view_order.html", sale=sale)

@app.route('/orders/id_<order_id>/edit', methods=['GET', 'POST'])
def edit_order(order_id):
    sale = Sales.query.filter_by(order_id=order_id).first()
    if request.method == "POST":
        try:
            buyer = request.form['buyer']
            sku = request.form['sku']
            prod_costs = request.form['prod_costs']
            ship_costs = request.form['ship_costs']
            undef_costs = request.form['undef_costs']
            note = request.form['note']
            if buyer != "":
                sale.buyer = buyer
            if sku != "":
                sale.sku = sku
            if prod_costs != "":
                sale.prod_costs = prod_costs
            if ship_costs != "":
                sale.ship_costs = ship_costs
            if undef_costs != "":
                sale.undef_costs = undef_costs
            if note != "":
                sale.note = note
            db.session.commit()
            upload_file.update_data()
            return render_template("edit_order_success.html", sale=sale)
        except:
            db.session.rollback()
            return render_template("edit_order_fail.html", sale=sale)
    if request.method == "GET":
        return render_template("edit_order.html", sale=sale)

@app.route('/orders/id_<order_id>/status=<status>', methods=['GET', 'POST'])
def change_status(order_id, status):
    sale = Sales.query.filter_by(order_id=order_id).first()
    sale.status = status
    db.session.commit()
    upload_file.update_data()
    return render_template("edit_order_success.html", sale=sale)

if __name__ == '__main__':
    app.run(debug=False)