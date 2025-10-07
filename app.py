import sys
sys.path.append("C:/Lib/site-packages")

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_cream_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# استيراد النماذج وقاعدة البيانات
from models import db, Product, Sale, SaleItem, Expense

# ربط قاعدة البيانات بالتطبيق
db.init_app(app)

# إنشاء قاعدة البيانات
with app.app_context():
    db.create_all()

# الصفحة الرئيسية - واجهة الكاشير
@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).all()
    return render_template('index.html', products=products)

# إضافة منتج جديد
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        cost = float(request.form['cost'])
        description = request.form.get('description', '')
        
        product = Product(name=name, price=price, cost=cost, description=description)
        db.session.add(product)
        db.session.commit()
        flash('تم إضافة المنتج بنجاح!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

# عرض جميع المنتجات
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# تعديل منتج
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.cost = float(request.form['cost'])
        product.description = request.form.get('description', '')
        product.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash('تم تحديث المنتج بنجاح!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

# حذف منتج
@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.is_active = False
    db.session.commit()
    flash('تم حذف المنتج بنجاح!', 'success')
    return redirect(url_for('products'))

# إضافة مبيعة جديدة
@app.route('/add_sale', methods=['POST'])
def add_sale():
    try:
        items = request.json.get('items', [])
        total = float(request.json.get('total', 0))
        
        if not items:
            return jsonify({'success': False, 'message': 'لا توجد عناصر في الفاتورة'})
        
        # إنشاء فاتورة جديدة
        sale = Sale(total_amount=total)
        db.session.add(sale)
        db.session.flush()  # للحصول على ID الفاتورة
        
        # إضافة عناصر الفاتورة
        for item in items:
            product_id = item['product_id']
            quantity = int(item['quantity'])
            price = float(item['price'])
            
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product_id,
                quantity=quantity,
                price=price
            )
            db.session.add(sale_item)
        
        db.session.commit()
        return jsonify({'success': True, 'sale_id': sale.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# عرض المصروفات
@app.route('/expenses')
def expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('expenses.html', expenses=expenses)

# إضافة مصروف جديد
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        
        expense = Expense(description=description, amount=amount, category=category)
        db.session.add(expense)
        db.session.commit()
        flash('تم إضافة المصروف بنجاح!', 'success')
        return redirect(url_for('expenses'))
    
    return render_template('add_expense.html')

# التقارير
@app.route('/reports')
def reports():
    today = date.today()
    
    # مبيعات اليوم
    today_sales = db.session.query(db.func.sum(Sale.total_amount)).filter(
        db.func.date(Sale.date) == today
    ).scalar() or 0
    
    # مصروفات اليوم
    today_expenses = db.session.query(db.func.sum(Expense.amount)).filter(
        db.func.date(Expense.date) == today
    ).scalar() or 0
    
    # صافي الربح اليوم
    today_profit = today_sales - today_expenses
    
    # إجمالي المبيعات هذا الشهر
    month_sales = db.session.query(db.func.sum(Sale.total_amount)).filter(
        db.func.strftime('%Y-%m', Sale.date) == today.strftime('%Y-%m')
    ).scalar() or 0
    
    # إجمالي المصروفات هذا الشهر
    month_expenses = db.session.query(db.func.sum(Expense.amount)).filter(
        db.func.strftime('%Y-%m', Expense.date) == today.strftime('%Y-%m')
    ).scalar() or 0
    
    # صافي الربح هذا الشهر
    month_profit = month_sales - month_expenses
    
    return render_template('reports.html', 
                         today_sales=today_sales,
                         today_expenses=today_expenses,
                         today_profit=today_profit,
                         month_sales=month_sales,
                         month_expenses=month_expenses,
                         month_profit=month_profit)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
import os
import time
import threading
import webbrowser

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    time.sleep(1)
    app.run(debug=False)



