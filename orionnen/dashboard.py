import run
from decimal import Decimal as D
import datetime

def calculate(month):
    if month == 'all':
        order = run.db.session.query(app.Order).all()
        ord_count = app.db.session.query(run.Order).count()
        rf_count = app.db.session.query(app.Order).filter(run.Order.net_revenue == 0).count()
    else:
        order = app.db.session.query(run.Order).filter(app.Order.date.between(f'2022-{month}-01', f'2022-{month}-31'))
        ord_count = app.db.session.query(app.Order).filter(run.Order.date.between(f'2022-{month}-01', f'2022-{month}-31')).count()
        rf_count = run.db.session.query(app.Order).filter(
            app.Order.date.between(f'2022-{month}-01', f'2022-{month}-31'), app.Order.net_revenue==0).count()
    net_revenue = costs = etsy_costs = prod_costs = ship_costs = undef_costs = profit = 0
    for order in order:
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
        order = app.Order.query.order_by(run.Order.date.asc())
    else:
        order = app.db.session.query(run.Order).filter(app.Order.date.between(f'2022-{month}-01', f'2022-{month}-31')).order_by(app.Order.date.asc())
    start_date = order[0].date
    end_date = order[-1].date
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        dates.append(f"{start_date.month}/{start_date.day}")
        profit = 0
        order_day = app.db.session.query(app.Order).filter(run.Order.date == start_date)
        for order in order_day:
            profit += order.profit
        profits.append(profit)
        start_date += delta
    return [dates, profits]