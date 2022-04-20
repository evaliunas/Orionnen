import app
from decimal import Decimal as D
import datetime

def calculate(month):
    if month == 'all':
        sales = app.db.session.query(app.Sales).all()
        ord_count = app.db.session.query(app.Sales).count()
        rf_count = app.db.session.query(app.Sales).filter(app.Sales.net_revenue==0).count()
    else:
        sales = app.db.session.query(app.Sales).filter(app.Sales.date.between(f'2022-{month}-01', f'2022-{month}-31'))
        ord_count = app.db.session.query(app.Sales).filter(app.Sales.date.between(f'2022-{month}-01', f'2022-{month}-31')).count()
        rf_count = app.db.session.query(app.Sales).filter(
            app.Sales.date.between(f'2022-{month}-01', f'2022-{month}-31'), app.Sales.net_revenue==0).count()
    net_revenue = costs = etsy_costs = prod_costs = ship_costs = undef_costs = profit = 0
    for sale in sales:
        net_revenue += D(str(sale.net_revenue))
        costs += D(str(sale.costs))
        prod_costs += D(str(sale.prod_costs))
        etsy_costs += D(str(sale.etsy_costs))
        ship_costs += D(str(sale.ship_costs))
        undef_costs += D(str(sale.undef_costs))
        profit += D(str(sale.profit))
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
        sales = app.Sales.query.order_by(app.Sales.date.asc())
    else:
        sales = app.db.session.query(app.Sales).filter(app.Sales.date.between(f'2022-{month}-01', f'2022-{month}-31')).order_by(app.Sales.date.asc())
    start_date = sales[0].date
    end_date = sales[-1].date
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        dates.append(f"{start_date.month}/{start_date.day}")
        profit = 0
        sales_day = app.db.session.query(app.Sales).filter(app.Sales.date == start_date)
        for sale in sales_day:
            profit += sale.profit
        profits.append(profit)
        start_date += delta
    return [dates, profits]