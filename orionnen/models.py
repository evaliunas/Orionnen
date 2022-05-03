from orionnen import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, unique=True, nullable=False)
    sku = db.Column(db.String(20), default='')
    buyer = db.Column(db.String(20), default='')
    date = db.Column(db.Date, nullable=False)
    note = db.Column(db.String(20), default='')
    status = db.Column(db.String(20), default='Ordered')
    revenue = db.Column(db.Float, default=0)
    refund = db.Column(db.Float, default=0)
    net_revenue = db.Column(db.Float, default=0)
    proc_fee = db.Column(db.Float, default=0)
    cred_proc_fee = db.Column(db.Float, default=0)
    net_proc_fee = db.Column(db.Float, default=0)
    trans_trans_fee = db.Column(db.Float, default=0)
    cred_trans_trans_fee = db.Column(db.Float, default=0)
    ship_trans_fee = db.Column(db.Float, default=0)
    cred_ship_trans_fee = db.Column(db.Float, default=0)
    ad_fee = db.Column(db.Float, default=0)
    cred_ad_fee = db.Column(db.Float, default=0)
    net_ad_fee = db.Column(db.Float, default=0)
    vat_ad = db.Column(db.Float, default=0)
    cred_vat_ad = db.Column(db.Float, default=0)
    vat_proc_fee = db.Column(db.Float, default=0)
    cred_vat_proc_fee = db.Column(db.Float, default=0)
    vat_trans = db.Column(db.Float, default=0)
    cred_vat_trans = db.Column(db.Float, default=0)
    vat_ship_trans = db.Column(db.Float, default=0)
    cred_vat_ship_trans = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    cred_tax = db.Column(db.Float, default=0)
    net_tax = db.Column(db.Float, default=0)
    trans_fee = db.Column(db.Float, default=0)
    cred_trans_fee = db.Column(db.Float, default=0)
    net_trans_fee = db.Column(db.Float, default=0)
    vat = db.Column(db.Float, default=0)
    cred_vat = db.Column(db.Float, default=0)
    net_vat = db.Column(db.Float, default=0)
    etsy_costs = db.Column(db.Float, default=0)
    prod_costs = db.Column(db.Float, default=0)
    ship_costs = db.Column(db.Float, default=0)
    undef_costs = db.Column(db.Float, default=0)
    other_costs = db.Column(db.Float, default=0)
    costs = db.Column(db.Float, default=0)
    profit = db.Column(db.Float, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

db.create_all()