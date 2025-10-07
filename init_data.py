"""
ملف إضافة البيانات التجريبية للبرنامج
"""

from app import app, db
from models import Product, Sale, SaleItem, Expense
from datetime import datetime, timedelta
import random

def init_sample_data():
    """إضافة بيانات تجريبية للبرنامج"""
    
    with app.app_context():
        # إنشاء قاعدة البيانات
        db.create_all()
        
        # التحقق من وجود بيانات مسبقة
        if Product.query.first():
            print("البيانات موجودة بالفعل!")
            return
        
        print("جاري إضافة البيانات التجريبية...")
        
        # إضافة منتجات تجريبية
        products = [
            Product(name="آيس كريم فانيليا", price=15.0, cost=8.0, description="آيس كريم فانيليا كلاسيكي"),
            Product(name="آيس كريم شوكولاتة", price=18.0, cost=10.0, description="آيس كريم شوكولاتة غني"),
            Product(name="آيس كريم فراولة", price=16.0, cost=9.0, description="آيس كريم فراولة طبيعي"),
            Product(name="آيس كريم مانجو", price=20.0, cost=12.0, description="آيس كريم مانجو استوائي"),
            Product(name="آيس كريم كوكيز", price=22.0, cost=13.0, description="آيس كريم بقطع الكوكيز"),
            Product(name="آيس كريم كراميل", price=19.0, cost=11.0, description="آيس كريم كراميل حلو"),
            Product(name="آيس كريم نعناع", price=17.0, cost=9.5, description="آيس كريم نعناع منعش"),
            Product(name="آيس كريم موز", price=16.0, cost=8.5, description="آيس كريم موز طبيعي"),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print(f"تم إضافة {len(products)} منتج")
        
        # إضافة مبيعات تجريبية للأيام الماضية
        for i in range(30):  # آخر 30 يوم
            date = datetime.now() - timedelta(days=i)
            
            # عدد عشوائي من المبيعات يومياً (1-8 مبيعات)
            daily_sales = random.randint(1, 8)
            
            for j in range(daily_sales):
                sale = Sale(total_amount=0, date=date - timedelta(hours=random.randint(0, 23), 
                                                                minutes=random.randint(0, 59)))
                db.session.add(sale)
                db.session.flush()
                
                # إضافة عناصر عشوائية للفاتورة
                num_items = random.randint(1, 4)
                total = 0
                
                selected_products = random.sample(products, num_items)
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        product_id=product.id,
                        quantity=quantity,
                        price=product.price
                    )
                    db.session.add(sale_item)
                    total += quantity * product.price
                
                sale.total_amount = total
        
        db.session.commit()
        print("تم إضافة المبيعات التجريبية")
        
        # إضافة مصروفات تجريبية
        expense_categories = [
            ("فاتورة كهرباء", "كهرباء", 450.0),
            ("راتب موظف", "رواتب", 3000.0),
            ("مواد خام - حليب", "مواد خام", 800.0),
            ("مواد خام - سكر", "مواد خام", 200.0),
            ("صيانة الثلاجة", "صيانة", 150.0),
            ("مواد تنظيف", "تنظيف", 80.0),
            ("إيجار المحل", "إيجار", 2500.0),
            ("فاتورة مياه", "مياه", 120.0),
            ("مواد خام - فواكه", "مواد خام", 300.0),
            ("أكواب وملاعق", "أدوات", 100.0),
        ]
        
        for i, (desc, category, amount) in enumerate(expense_categories):
            # توزيع المصروفات على الشهر الماضي
            date = datetime.now() - timedelta(days=random.randint(1, 30))
            expense = Expense(
                description=desc,
                amount=amount,
                category=category,
                date=date
            )
            db.session.add(expense)
        
        db.session.commit()
        print(f"تم إضافة {len(expense_categories)} مصروف")
        
        print("تم إنشاء البيانات التجريبية بنجاح! 🎉")
        print("\nيمكنك الآن:")
        print("1. تشغيل البرنامج: python app.py")
        print("2. فتح المتصفح على: http://127.0.0.1:5000")

if __name__ == "__main__":
    init_sample_data()
