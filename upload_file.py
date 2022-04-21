import datetime
from app import db, Sales
from decimal import Decimal as D

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
            date = datetime.datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
            if bool(Sales.query.filter_by(order_id=order_id).first()) == True:
                sale = Sales.query.filter_by(order_id=order_id).first()
                if data < 0:
                    sale.vat_ship_trans = abs(data)
                else:
                    sale.cred_vat_ship_trans = data
                db.session.commit()
            else:
                sale = Sales(order_id, date)
                db.session.add(sale)
                db.session.commit()
                if data < 0:
                    sale.vat_ship_trans = abs(data)
                else:
                    sale.cred_vat_ship_trans = data
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
            date = datetime.datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
            if bool(Sales.query.filter_by(order_id=order_id).first()) == True:
                sale = Sales.query.filter_by(order_id=order_id).first()
                if data < 0:
                    sale.vat_trans = abs(data)
                else:
                    sale.cred_vat_trans = data
                db.session.commit()
            else:
                sale = Sales(order_id, date)
                db.session.add(sale)
                db.session.commit()
                if data < 0:
                    sale.vat_trans = abs(data)
                else:
                    sale.cred_vat_trans = data
                db.session.commit()
        if 'Sale' in str(df.loc[row, 'Type']) or 'Refund' in str(df.loc[row, 'Type']):
            order_id = int(''.join(filter(str.isdigit, df.loc[row, 'Title'])))
            data_num = df.loc[row, 'Net'].replace('€', '')
            data = float(data_num)
            date = datetime.datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
            if bool(Sales.query.filter_by(order_id=order_id).first()) == True:
                sale = Sales.query.filter_by(order_id=order_id).first()
                if 'Sale' in str(df.loc[row, 'Type']):
                    sale.revenue = data
                else:
                    sale.refund = abs(data)
                db.session.commit()
            else:
                sale = Sales(order_id, date)
                db.session.add(sale)
                db.session.commit()
                if 'Sale' in str(df.loc[row, 'Type']):
                    sale.revenue = data
                else:
                    sale.refund = abs(data)
                db.session.commit()
        if 'rder' in str(df.loc[row, 'Info']):
            order_id = int(''.join(filter(str.isdigit, df.loc[row, 'Info'])))
            if bool(Sales.query.filter_by(order_id=order_id).first()) == True:
                sale = Sales.query.filter_by(order_id=order_id).first()
                data_num = df.loc[row, 'Net'].replace('€', '')
                data = float(data_num)
                if 'rocessing' in str(df.loc[row, 'Title']):
                    if 'VAT' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.vat_proc_fee = abs(data)
                        else:
                            sale.cred_vat_proc_fee = data
                    elif data < 0:
                        sale.proc_fee = abs(data)
                    else:
                        sale.cred_proc_fee = data
                if 'ransaction' in str(df.loc[row, 'Title']):
                    if 'hipping' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.ship_trans_fee = abs(data)
                        else:
                            sale.cred_ship_trans_fee = data
                    else:
                        if data < 0:
                            sale.trans_trans_fee = abs(data)
                        else:
                            sale.cred_trans_trans_fee = data
                if 'Offsite Ads' in str(df.loc[row, 'Title']):
                    if 'VAT' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.vat_ad = abs(data)
                        else:
                            sale.cred_vat_ad = data
                    elif data < 0:
                        sale.ad_fee = abs(data)
                    else:
                        sale.cred_ad_fee = data
                if 'tax' in str(df.loc[row, 'Title']):
                    if data < 0:
                        sale.tax = abs(data)
                    else:
                        sale.cred_tax = data
                db.session.commit()
            else:
                date = datetime.datetime.strptime(str(df.loc[row, 'Date']), '%B %d, %Y')
                sale = Sales(order_id, date)
                db.session.add(sale)
                db.session.commit()
                data = float(df.loc[row, 'Net'].replace('€', ''))
                if 'rocessing' in str(df.loc[row, 'Title']):
                    if 'VAT' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.vat_proc_fee = abs(data)
                        else:
                            sale.cred_vat_proc_fee = data
                    elif data < 0:
                        sale.proc_fee = abs(data)
                    else:
                        sale.cred_proc_fee = data
                if 'ransaction fee' in str(df.loc[row, 'Title']):
                    if 'hipping' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.ship_trans_fee = abs(data)
                        else:
                            sale.cred_ship_trans_fee = data
                    else:
                        if data < 0:
                            sale.trans_trans_fee = abs(data)
                        else:
                            sale.cred_trans_trans_fee = data
                if 'Offsite Ads' in str(df.loc[row, 'Title']):
                    if 'VAT' in str(df.loc[row, 'Title']):
                        if data < 0:
                            sale.vat_ad = abs(data)
                        else:
                            sale.cred_vat_ad = data
                    elif data < 0:
                        sale.ad_fee = abs(data)
                    else:
                        sale.cred_ad_fee = data
                if 'tax' in str(df.loc[row, 'Title']):
                    if data < 0:
                        sale.tax = abs(data)
                    else:
                        sale.cred_tax = data
                db.session.commit()
        row += 1
    update_data()

def update_data():
    sales = Sales.query.all()
    for sale in sales:
        sale.net_revenue = D(str(sale.revenue)) - D(str(sale.refund))
        sale.trans_fee = D(str(sale.trans_trans_fee)) + D(str(sale.ship_trans_fee))
        sale.cred_trans_fee = D(str(sale.cred_trans_trans_fee)) + D(str(sale.cred_ship_trans_fee))
        sale.net_trans_fee = D(str(sale.trans_fee)) - D(str(sale.cred_trans_fee))
        sale.vat = D(str(sale.vat_ad)) + D(str(sale.vat_proc_fee)) \
                    + D(str(sale.vat_trans)) + D(str(sale.vat_ship_trans))
        sale.cred_vat = D(str(sale.cred_vat_ad)) + D(str(sale.cred_vat_proc_fee)) \
                        + D(str(sale.cred_vat_trans)) + D(str(sale.cred_vat_ship_trans))
        sale.net_vat = D(str(sale.vat)) - D(str(sale.cred_vat))
        sale.net_proc_fee = D(str(sale.proc_fee)) - D(str(sale.cred_proc_fee))
        sale.net_ad_fee = D(str(sale.ad_fee)) - D(str(sale.cred_ad_fee))
        sale.net_tax = D(str(sale.tax)) - D(str(sale.cred_tax))
        sale.etsy_costs = D(str(sale.net_proc_fee)) + D(str(sale.net_ad_fee)) \
                        + D(str(sale.net_tax)) + D(str(sale.net_vat)) \
                        + D(str(sale.net_trans_fee))
        sale.other_costs = D(str(sale.prod_costs)) + D(str(sale.ship_costs)) + D(str(sale.undef_costs))
        sale.costs = D(str(sale.etsy_costs)) + D(str(sale.other_costs))
        sale.profit = D(str(sale.net_revenue)) - D(str(sale.costs))
        db.session.commit()