from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    """نموذج المنتجات - أنواع الآيس كريم"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # سعر البيع
    cost = db.Column(db.Float, nullable=False)   # سعر التكلفة
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع عناصر المبيعات
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def profit_margin(self):
        """حساب هامش الربح"""
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0

class Sale(db.Model):
    """نموذج المبيعات - الفواتير"""
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع عناصر الفاتورة
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sale {self.id} - {self.total_amount}>'
    
    @property
    def total_cost(self):
        """حساب إجمالي التكلفة للفاتورة"""
        total = 0
        for item in self.items:
            total += item.quantity * item.product.cost
        return total
    
    @property
    def profit(self):
        """حساب الربح من الفاتورة"""
        return self.total_amount - self.total_cost

class SaleItem(db.Model):
    """نموذج عناصر الفاتورة"""
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # السعر وقت البيع
    
    def __repr__(self):
        return f'<SaleItem {self.product.name} x{self.quantity}>'
    
    @property
    def total_price(self):
        """إجمالي سعر العنصر"""
        return self.quantity * self.price
    
    @property
    def total_cost(self):
        """إجمالي تكلفة العنصر"""
        return self.quantity * self.product.cost
    
    @property
    def profit(self):
        """ربح العنصر"""
        return self.total_price - self.total_cost

class Expense(db.Model):
    """نموذج المصروفات"""
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.description} - {self.amount}>'
