from flask_login import current_user
from orionnen import db
from orionnen.models import Order
from decimal import Decimal as D
import datetime

def calculate(month):
    if month == 'all':
        orders = db.session.query(Order).filter_by(author=current_user)
        ord_count = db.session.query(Order).filter_by(author=current_user).count()
        rf_count = db.session.query(Order).filter_by(author=current_user).filter(Order.net_revenue <= 0).count()
    else:
        orders = db.session.query(Order).filter(Order.date.between(
            f'2022-{month}-01', f'2022-{month}-31')).filter_by(author=current_user)
        ord_count = db.session.query(Order).filter(Order.date.between(
            f'2022-{month}-01', f'2022-{month}-31')).filter_by(author=current_user).count()
        rf_count = db.session.query(Order).filter(
            Order.date.between(f'2022-{month}-01', f'2022-{month}-31'), Order.net_revenue==0).filter_by(
            author=current_user).count()
    net_revenue = costs = etsy_costs = prod_costs = ship_costs = undef_costs = profit = 0
    for order in orders:
        net_revenue += D(str(order.net_revenue))
        costs += D(str(order.costs))
        prod_costs += D(str(order.prod_costs))
        etsy_costs += D(str(order.etsy_costs))
        ship_costs += D(str(order.ship_costs))
        undef_costs += D(str(order.undef_costs))
        profit += D(str(order.profit))
    net_ord = ord_count - rf_count
    if net_ord != 0:
        avg_net_revenue = round(net_revenue/net_ord,2)
        avg_costs = round(costs/net_ord,2)
        avg_prod_costs = round(prod_costs/net_ord,2)
        avg_etsy_costs = round(etsy_costs/net_ord,2)
        avg_ship_costs = round(ship_costs/net_ord,2)
        avg_undef_costs = round(undef_costs/net_ord,2)
        avg_profit = round(profit/net_ord,2)
    else:
        avg_net_revenue = avg_costs = avg_prod_costs = avg_etsy_costs = avg_ship_costs = avg_undef_costs = avg_profit = 0
    return [ord_count, rf_count, net_revenue, avg_net_revenue, costs, avg_costs, etsy_costs, avg_etsy_costs,
            prod_costs, avg_prod_costs, ship_costs, avg_ship_costs, undef_costs, avg_undef_costs, profit, avg_profit]

def linechart(month):
    dates = []
    profits = []
    if month == 'all':
        orders = db.session.query(Order).filter_by(author=current_user).order_by(Order.date.asc())
    else:
        orders = db.session.query(Order).filter(Order.date.between(
            f'2022-{month}-01', f'2022-{month}-31')).filter_by(author=current_user).order_by(Order.date.asc())
    start_date = orders[0].date
    end_date = orders[-1].date
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        dates.append(f"{start_date.month}/{start_date.day}")
        profit = 0
        day_orders = db.session.query(Order).filter(Order.date == start_date)
        for order in day_orders:
            profit += order.profit
        profits.append(profit)
        start_date += delta
    return [dates, profits]