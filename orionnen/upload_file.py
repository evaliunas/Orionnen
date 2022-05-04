from datetime import datetime
from orionnen import db
from orionnen.models import Order
from decimal import Decimal as D
from flask_login import current_user

def upload_data(df, rows):
    row = 0
    while row < rows:
        if 'shipping transaction' in str(df.loc[row, 'Title']):
            i = 1
            while True:
                if 'order' in str(df.loc[row + i, 'Info']):
                    order_id = int(''.join(filter(str.isdigit, df.loc[row + i, 'Info'])))
                    break
                else:
                    i += 1
            data_num = df.loc[row, 'Net'].replace('€', '')
            data = float(data_num)
            order = Order.query.filter_by(order_id=order_id).first()
            if not order:
                date = datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
                order = Order(author=current_user, order_id=order_id, date=date)
                db.session.add(order)
                db.session.commit()
            if data < 0:
                order.vat_ship_trans = abs(data)
            else:
                order.cred_vat_ship_trans = data
            db.session.commit()

        if 'transaction' in str(df.loc[row, 'Info']):
            i = 1
            while True:
                if 'order' in str(df.loc[row + i, 'Info']):
                    order_id = int(''.join(filter(str.isdigit, df.loc[row + i, 'Info'])))
                    break
                else:
                    i += 1
            data_num = df.loc[row, 'Net'].replace('€', '')
            data = float(data_num)
            order = Order.query.filter_by(order_id=order_id).first()
            if not order:
                date = datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
                order = Order(author=current_user, order_id=order_id, date=date)
                db.session.add(order)
                db.session.commit()
            if data < 0:
                order.vat_trans = abs(data)
            else:
                order.cred_vat_trans = data
            db.session.commit()

        if 'Sale' in str(df.loc[row, 'Type']) or 'Refund' in str(df.loc[row, 'Type']):
            order_id = int(''.join(filter(str.isdigit, df.loc[row, 'Title'])))
            data_num = df.loc[row, 'Net'].replace('€', '')
            data = float(data_num)
            order = Order.query.filter_by(order_id=order_id).first()
            if not order:
                date = datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
                order = Order(author=current_user, order_id=order_id, date=date)
                db.session.add(order)
                db.session.commit()
            if 'Sale' in str(df.loc[row, 'Type']):
                order.revenue = data
            else:
                order.refund = abs(data)
            db.session.commit()

        if 'rder' in str(df.loc[row, 'Info']):
            order_id = int(''.join(filter(str.isdigit, df.loc[row, 'Info'])))
            data_num = df.loc[row, 'Net'].replace('€', '')
            data = float(data_num)
            order = Order.query.filter_by(order_id=order_id).first()
            if not order:
                date = datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
                order = Order(author=current_user, order_id=order_id, date=date)
                db.session.add(order)
                db.session.commit()
            if 'rocessing' in str(df.loc[row, 'Title']):
                if 'VAT' in str(df.loc[row, 'Title']):
                    if data < 0:
                        order.vat_proc_fee = abs(data)
                    else:
                        order.cred_vat_proc_fee = data
                elif data < 0:
                    order.proc_fee = abs(data)
                else:
                    order.cred_proc_fee = data
            if 'ransaction' in str(df.loc[row, 'Title']):
                if 'hipping' in str(df.loc[row, 'Title']):
                    if data < 0:
                        order.ship_trans_fee = abs(data)
                    else:
                        order.cred_ship_trans_fee = data
                elif data < 0:
                    order.trans_trans_fee = abs(data)
                else:
                    order.cred_trans_trans_fee = data
            if 'Offsite Ads' in str(df.loc[row, 'Title']):
                if 'VAT' in str(df.loc[row, 'Title']):
                    if data < 0:
                        order.vat_ad = abs(data)
                    else:
                        order.cred_vat_ad = data
                elif data < 0:
                    order.ad_fee = abs(data)
                else:
                    order.cred_ad_fee = data
            if 'tax' in str(df.loc[row, 'Title']):
                if data < 0:
                    order.tax = abs(data)
                else:
                    order.cred_tax = data
            db.session.commit()

        row += 1
    update_data()

def update_data():
    orders = Order.query.all()
    for order in orders:
        order.net_revenue = D(str(order.revenue)) - D(str(order.refund))
        order.trans_fee = D(str(order.trans_trans_fee)) + D(str(order.ship_trans_fee))
        order.cred_trans_fee = D(str(order.cred_trans_trans_fee)) + D(str(order.cred_ship_trans_fee))
        order.net_trans_fee = D(str(order.trans_fee)) - D(str(order.cred_trans_fee))
        order.vat = D(str(order.vat_ad)) + D(str(order.vat_proc_fee)) \
                    + D(str(order.vat_trans)) + D(str(order.vat_ship_trans))
        order.cred_vat = D(str(order.cred_vat_ad)) + D(str(order.cred_vat_proc_fee)) \
                        + D(str(order.cred_vat_trans)) + D(str(order.cred_vat_ship_trans))
        order.net_vat = D(str(order.vat)) - D(str(order.cred_vat))
        order.net_proc_fee = D(str(order.proc_fee)) - D(str(order.cred_proc_fee))
        order.net_ad_fee = D(str(order.ad_fee)) - D(str(order.cred_ad_fee))
        order.net_tax = D(str(order.tax)) - D(str(order.cred_tax))
        order.etsy_costs = D(str(order.net_proc_fee)) + D(str(order.net_ad_fee)) \
                        + D(str(order.net_tax)) + D(str(order.net_vat)) \
                        + D(str(order.net_trans_fee))
        order.other_costs = D(str(order.prod_costs)) + D(str(order.ship_costs)) + D(str(order.undef_costs))
        order.costs = D(str(order.etsy_costs)) + D(str(order.other_costs))
        order.profit = D(str(order.net_revenue)) - D(str(order.costs))
        db.session.commit()