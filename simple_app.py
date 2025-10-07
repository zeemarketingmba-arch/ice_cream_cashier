"""
نسخة مبسطة من برنامج كاشير الآيس كريم
تستخدم المكتبات المدمجة في Python فقط
"""

import http.server
import socketserver
import json
import sqlite3
import os
import webbrowser
from datetime import datetime
from urllib.parse import parse_qs, urlparse
import threading
import time

# إنشاء قاعدة البيانات
def init_database():
    conn = sqlite3.connect('ice_cream_simple.db')
    cursor = conn.cursor()
    
    # جدول المنتجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المبيعات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول عناصر المبيعات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # جدول المصروفات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إضافة بيانات تجريبية إذا لم تكن موجودة
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('آيس كريم فانيليا', 15.0, 8.0, 'آيس كريم فانيليا كلاسيكي'),
            ('آيس كريم شوكولاتة', 18.0, 10.0, 'آيس كريم شوكولاتة غني'),
            ('آيس كريم فراولة', 16.0, 9.0, 'آيس كريم فراولة طبيعي'),
            ('آيس كريم مانجو', 20.0, 12.0, 'آيس كريم مانجو استوائي'),
        ]
        
        cursor.executemany(
            'INSERT INTO products (name, price, cost, description) VALUES (?, ?, ?, ?)',
            sample_products
        )
        
        print("تم إضافة المنتجات التجريبية")
    
    conn.commit()
    conn.close()

# HTML للصفحة الرئيسية
def get_main_page():
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>كاشير الآيس كريم</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
        .products-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .product-card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); cursor: pointer; text-align: center; }
        .product-card:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .cart { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .cart-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-warning { background: #ffc107; color: black; }
        .total { background: #28a745; color: white; padding: 15px; border-radius: 10px; text-align: center; margin: 15px 0; }
        .nav { background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .nav a { margin: 0 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍦 كاشير الآيس كريم</h1>
        </div>
        
        <div class="nav">
            <a href="/">الكاشير</a>
            <a href="/products">المنتجات</a>
            <a href="/expenses">المصروفات</a>
            <a href="/reports">التقارير</a>
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
            <div>
                <h3>المنتجات المتاحة</h3>
                <div class="products-grid" id="products-grid">
                    <!-- سيتم تحميل المنتجات هنا -->
                </div>
            </div>
            
            <div>
                <div class="cart">
                    <h3>سلة المشتريات</h3>
                    <div id="cart-items">
                        <p style="text-align: center; color: #666;">السلة فارغة</p>
                    </div>
                    <div id="cart-total" style="display: none;">
                        <div class="total">
                            <h4>الإجمالي: <span id="total-amount">0.00</span> ج.م</h4>
                        </div>
                        <button class="btn btn-success" style="width: 100%;" onclick="checkout()">إتمام البيع</button>
                        <button class="btn btn-warning" style="width: 100%;" onclick="clearCart()">مسح السلة</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let cart = [];
        let products = [];

        // تحميل المنتجات
        async function loadProducts() {
            try {
                const response = await fetch('/api/products');
                products = await response.json();
                displayProducts();
            } catch (error) {
                console.error('خطأ في تحميل المنتجات:', error);
            }
        }

        function displayProducts() {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = products.map(product => `
                <div class="product-card" onclick="addToCart(${product.id}, '${product.name}', ${product.price})">
                    <h4>${product.name}</h4>
                    <p><strong>${product.price.toFixed(2)} ج.م</strong></p>
                    <p style="color: #666; font-size: 0.9em;">${product.description || ''}</p>
                </div>
            `).join('');
        }

        function addToCart(productId, productName, productPrice) {
            const existingItem = cart.find(item => item.product_id === productId);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({
                    product_id: productId,
                    name: productName,
                    price: productPrice,
                    quantity: 1
                });
            }
            
            updateCartDisplay();
        }

        function updateQuantity(productId, newQuantity) {
            if (newQuantity <= 0) {
                cart = cart.filter(item => item.product_id !== productId);
            } else {
                const item = cart.find(item => item.product_id === productId);
                if (item) item.quantity = newQuantity;
            }
            updateCartDisplay();
        }

        function updateCartDisplay() {
            const cartItemsDiv = document.getElementById('cart-items');
            const cartTotalDiv = document.getElementById('cart-total');
            const totalAmountSpan = document.getElementById('total-amount');
            
            if (cart.length === 0) {
                cartItemsDiv.innerHTML = '<p style="text-align: center; color: #666;">السلة فارغة</p>';
                cartTotalDiv.style.display = 'none';
                return;
            }
            
            let total = 0;
            cartItemsDiv.innerHTML = cart.map(item => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                return `
                    <div class="cart-item">
                        <div>
                            <strong>${item.name}</strong><br>
                            <small>${item.price.toFixed(2)} ج.م × ${item.quantity}</small>
                        </div>
                        <div>
                            <button class="btn" onclick="updateQuantity(${item.product_id}, ${item.quantity - 1})">-</button>
                            <span>${item.quantity}</span>
                            <button class="btn" onclick="updateQuantity(${item.product_id}, ${item.quantity + 1})">+</button>
                            <div><strong>${itemTotal.toFixed(2)} ج.م</strong></div>
                        </div>
                    </div>
                `;
            }).join('');
            
            totalAmountSpan.textContent = total.toFixed(2);
            cartTotalDiv.style.display = 'block';
        }

        function clearCart() {
            cart = [];
            updateCartDisplay();
        }

        async function checkout() {
            if (cart.length === 0) {
                alert('السلة فارغة!');
                return;
            }
            
            try {
                const response = await fetch('/api/sale', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ items: cart })
                });
                
                const result = await response.json();
                if (result.success) {
                    alert('تم إتمام البيع بنجاح!\\nرقم الفاتورة: ' + result.sale_id);
                    clearCart();
                } else {
                    alert('حدث خطأ: ' + result.message);
                }
            } catch (error) {
                alert('حدث خطأ في الاتصال');
            }
        }

        // تحميل المنتجات عند تحميل الصفحة
        loadProducts();
    </script>
</body>
</html>
    '''

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_main_page().encode('utf-8'))
        elif self.path == '/api/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            conn = sqlite3.connect('ice_cream_simple.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, price, cost, description FROM products WHERE is_active = 1')
            products = []
            for row in cursor.fetchall():
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'price': row[2],
                    'cost': row[3],
                    'description': row[4]
                })
            conn.close()
            
            self.wfile.write(json.dumps(products, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/sale':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            try:
                conn = sqlite3.connect('ice_cream_simple.db')
                cursor = conn.cursor()
                
                # حساب الإجمالي
                total = sum(item['price'] * item['quantity'] for item in data['items'])
                
                # إضافة الفاتورة
                cursor.execute('INSERT INTO sales (total_amount) VALUES (?)', (total,))
                sale_id = cursor.lastrowid
                
                # إضافة عناصر الفاتورة
                for item in data['items']:
                    cursor.execute(
                        'INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                        (sale_id, item['product_id'], item['quantity'], item['price'])
                    )
                
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'sale_id': sale_id}, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': str(e)}, ensure_ascii=False).encode('utf-8'))

def start_server():
    init_database()
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"🍦 برنامج كاشير الآيس كريم يعمل على:")
        print(f"   http://localhost:{PORT}")
        print(f"   http://127.0.0.1:{PORT}")
        print("\nلإيقاف البرنامج اضغط Ctrl+C")
        
        # فتح المتصفح تلقائياً
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nتم إيقاف البرنامج. شكراً لاستخدام كاشير الآيس كريم! 🍦")

if __name__ == "__main__":
    start_server()
