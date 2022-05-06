from datetime import datetime
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from orionnen.upload_file import upload_data, update_data
from orionnen import app, db, bcrypt, mail
from orionnen.dashboard import calculate, linechart
from orionnen.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, EditOrderForm, NewOrderForm, InputCostsForm
from orionnen.models import Order, User, Costs
from flask_mail import Message

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account successfully created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@orionnen.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not request this email then simply ignore this email and changes will be made"""
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_token(token)
    if user in None:
        flash('Reset password request is invalid or expired. Please try again.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password successfully updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Acount')

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    month = 'all'
    try:
        data = calculate(month)
        dataset = linechart(month)
        dates = dataset[0]
        profits = dataset[1]
    except:
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dates = []
        profits = []
    return render_template("dashboard.html", data=data, month=month, dates=dates, profits=profits)

@app.route('/dashboard/month=<month>', methods=['GET', 'POST'])
@login_required
def filter_dashboard(month):
    try:
        data = calculate(month)
        dataset = linechart(month)
        dates = dataset[0]
        profits = dataset[1]
    except:
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dates = []
        profits = []
    return render_template("dashboard.html", data=data, month=month, dates=dates, profits=profits)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('csvfile'))
        rows = df.shape[0]
        try:
            upload_data(df, rows)
            flash('Data Uploaded!', 'success')
            return redirect(url_for('upload'))
        except ValueError:
            flash('Wrong data provided!', 'warning')
            return redirect(url_for('upload'))
    return render_template("upload.html")

@app.route('/new_order', methods=['GET', 'POST'])
@login_required
def new_order():
    form = NewOrderForm()
    if form.validate_on_submit():
        order = Order(author=current_user, order_id=form.order_id.data, date=form.date.data)
        db.session.add(order)
        db.session.commit()
        if form.buyer.data:
            order.buyer = form.buyer.data
        if form.sku.data:
            order.sku = form.sku.data
        if form.revenue.data:
            order.revenue = form.revenue.data
        if form.note.data:
            order.note = form.note.data
        db.session.commit()
        flash('Order added!', 'success')
    return render_template("new_order.html", title='New Order', form=form)

@app.route('/orders', methods=['GET', 'POST'])
@login_required
def show_orders():
    orders = db.session.query(Order).filter_by(author=current_user).order_by(Order.date.desc())
    return render_template("orders.html", orders=orders, month='All', status='All')

@app.route('/orders/<month>/<status>', methods=['GET', 'POST'])
@login_required
def show_orders_filtered(status, month):
    if month == 'All':
        if status == 'Not delivered':
            orders = db.session.query(Order).filter(Order.status != 'Delivered', Order.status != 'Waiting for return',
                                                    Order.status != 'Canceled').filter_by(author=current_user).order_by(
                                                    Order.date.desc())
        elif status != 'All':
            orders = db.session.query(Order).filter(Order.status == status).filter_by(author=current_user).order_by(
                                                    Order.date.desc())
        else:
            orders = db.session.query(Order).filter_by(author=current_user).order_by(Order.date.desc())
    else:
        if status == 'Not delivered':
            orders = db.session.query(Order).filter(Order.date.between(f'2022-{month}-01', f'2022-{month}-31'),
                                                    Order.status != 'Delivered', Order.status != 'Waiting for return',
                                                    Order.status != 'Canceled').filter_by(author=current_user).order_by(
                                                    Order.date.desc())
        elif status != 'All':
            orders = db.session.query(Order).filter(Order.date.between(f'2022-{month}-01', f'2022-{month}-31'),
                                                    Order.status == status).filter_by(author=current_user).order_by(
                                                    Order.date.desc())
        else:
            orders = db.session.query(Order).filter(Order.date.between(f'2022-{month}-01', f'2022-{month}-31')).filter_by(
                                                    author=current_user).order_by(Order.date.desc())
    return render_template("orders.html", orders=orders, month=month, status=status)

@app.route('/orders/id_<order_id>', methods=['GET', 'POST'])
@login_required
def view_order(order_id):
    order = Order.query.filter_by(order_id=order_id).filter_by(author=current_user).first()
    if request.method == "POST":
        note = request.form['note']
        order.note = note
        db.session.commit()
        flash('Order updated!', 'success')
        return redirect(url_for('view_order', order_id=order.order_id))
    return render_template("view_order.html", order=order)

@app.route('/orders/id_<order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.filter_by(order_id=order_id).filter_by(author=current_user).first()
    form = EditOrderForm()
    if form.validate_on_submit():
        if form.buyer.data:
            order.buyer = form.buyer.data
        if form.sku.data:
            order.sku = form.sku.data
        if form.prod_costs.data != None:
            order.prod_costs = form.prod_costs.data
        if form.ship_costs.data != None:
            order.ship_costs = form.ship_costs.data
        if form.undef_costs.data != None:
            order.undef_costs = form.undef_costs.data
        if form.note.data:
            order.note = form.note.data
        db.session.commit()
        update_data()
        flash('Order updated!', 'success')
        return redirect(url_for('view_order', order_id=order.order_id))
    return render_template("edit_order.html", order=order, form=form)

@app.route('/orders/id_<order_id>/delete')
@login_required
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).filter_by(author=current_user).first()
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted!', 'success')
    return redirect(url_for("show_orders"))

@app.route('/orders/id_<order_id>/status=<status>', methods=['GET', 'POST'])
@login_required
def change_status(order_id, status):
    order = Order.query.filter_by(order_id=order_id).filter_by(author=current_user).first()
    order.status = status
    db.session.commit()
    flash('Order updated!', 'success')
    return redirect(url_for('view_order', order_id=order_id))

@app.route('/new_costs', methods=['GET', 'POST'])
@login_required
def new_costs():
    form = InputCostsForm()
    if form.validate_on_submit():
        costs = Costs(author=current_user, order_id=form.order_id.data, date=form.date.data, value=form.value.data)
        db.session.add(costs)
        db.session.commit()
        if form.order_id.data:
            costs.order_id = form.order_id.data
            order = Order.query.filter_by(order_id=form.order_id.data).filter_by(author=current_user).first()
            if not order:
                flash('No order with provided order ID', 'danger')
                db.session.delete(costs)
                db.session.commit()
                return redirect(url_for('new_costs', title='New Costs', form=form))
            else:
                if form.costs_name.data:
                    costs.costs_name = form.costs_name.data
                if form.note.data:
                    costs.note = form.note.data
                if form.type.data == 'Production costs':
                    costs.prod_costs = True
                else:
                    costs.prod_costs = False
                if form.type.data == 'Shipping costs':
                    costs.ship_costs = True
                else:
                    costs.ship_costs = False
                if form.type.data == 'Other costs':
                    costs.undef_costs = True
                else:
                    costs.undef_costs = False
                db.session.commit()
                update_data()
                flash('Costs added!', 'success')
    return render_template("new_costs.html", title='New Costs', form=form)

@app.route('/costs/id_<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_costs(id):
    costs = Costs.query.filter_by(id=id).filter_by(author=current_user).first()
    form = EditCostsForm()
    if form.validate_on_submit():
        if form.date.data:
            costs.date = form.date.data
        if form.value.data:
            costs.value = form.value.data
        if form.costs_name.data:
            costs.costs_name = form.costs_name.data
        if form.note.data:
            costs.note = form.note.data
        if form.type.data == 'Production costs':
            costs.prod_costs = True
        else:
            costs.prod_costs = False
        if form.type.data == 'Shipping costs':
            costs.ship_costs = True
        else:
            costs.ship_costs = False
        if form.type.data == 'Other costs':
            costs.undef_costs = True
        else:
            costs.undef_costs = False
        db.session.commit()
        update_data()
        flash('Costs updated!', 'success')
        return redirect(url_for('view_costs', id=id))
    return render_template("edit_costs.html", costs=costs, form=form)

@app.route('/costs/<id>/delete')
@login_required
def delete_costs(id):
    costs = Costs.query.filter_by(id=id).filter_by(author=current_user).first()
    db.session.delete(costs)
    db.session.commit()
    flash('Costs deleted!', 'success')
    return redirect(url_for("orders"))