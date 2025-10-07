"""
برنامج كاشير الآيس كريم - تطبيق سطح مكتب
باستخدام Tkinter و SQLite
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime, date
import json
from pathlib import Path

class IceCreamCashier:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("كاشير الآيس كريم 🍦")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # إعداد قاعدة البيانات
        self.init_database()

        # متغيرات السلة
        self.cart = []
        self.total = 0.0

        # إنشاء الواجهة
        self.create_widgets()
        self.load_products()

    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        self.conn = sqlite3.connect('ice_cream_desktop.db')
        cursor = self.conn.cursor()

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
                ('آيس كريم كوكيز', 22.0, 13.0, 'آيس كريم بقطع الكوكيز'),
                ('آيس كريم كراميل', 19.0, 11.0, 'آيس كريم كراميل حلو'),
            ]

            cursor.executemany(
                'INSERT INTO products (name, price, cost, description) VALUES (?, ?, ?, ?)',
                sample_products
            )

            # إضافة مصروفات تجريبية
            sample_expenses = [
                ('فاتورة كهرباء', 450.0, 'كهرباء'),
                ('مواد خام - حليب', 800.0, 'مواد خام'),
                ('راتب موظف', 3000.0, 'رواتب'),
                ('صيانة الثلاجة', 150.0, 'صيانة'),
            ]

            cursor.executemany(
                'INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)',
                sample_expenses
            )

        self.conn.commit()

    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # إطار العنوان
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="🍦 كاشير الآيس كريم",
                              font=('Arial', 24, 'bold'),
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)

        # إطار الأزرار الرئيسية
        nav_frame = tk.Frame(self.root, bg='#34495e', height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)

        # أزرار التنقل
        btn_style = {'font': ('Arial', 12, 'bold'), 'fg': 'white', 'bg': '#3498db',
                    'relief': 'flat', 'padx': 20, 'pady': 10}

        tk.Button(nav_frame, text="🛒 الكاشير", command=self.show_cashier, **btn_style).pack(side='left', padx=5, pady=10)
        tk.Button(nav_frame, text="🍦 المنتجات", command=self.show_products, **btn_style).pack(side='left', padx=5, pady=10)
        tk.Button(nav_frame, text="💸 المصروفات", command=self.show_expenses, **btn_style).pack(side='left', padx=5, pady=10)
        tk.Button(nav_frame, text="📊 التقارير", command=self.show_reports, **btn_style).pack(side='left', padx=5, pady=10)

        # الإطار الرئيسي
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # عرض الكاشير افتراضياً
        self.show_cashier()

    def clear_main_frame(self):
        """مسح الإطار الرئيسي"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_cashier(self):
        """عرض واجهة الكاشير"""
        self.clear_main_frame()

        # إطار المنتجات (يسار)
        products_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=2)
        products_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        tk.Label(products_frame, text="المنتجات المتاحة", font=('Arial', 16, 'bold'),
                bg='white').pack(pady=10)

        # إطار شبكة المنتجات
        self.products_grid_frame = tk.Frame(products_frame, bg='white')
        self.products_grid_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # إطار السلة (يمين)
        cart_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=2, width=400)
        cart_frame.pack(side='right', fill='y', padx=(5, 0))
        cart_frame.pack_propagate(False)

        tk.Label(cart_frame, text="سلة المشتريات", font=('Arial', 16, 'bold'),
                bg='white').pack(pady=10)

        # قائمة السلة
        self.cart_listbox = tk.Listbox(cart_frame, font=('Arial', 11), height=15)
        self.cart_listbox.pack(fill='both', expand=True, padx=10, pady=10)

        # إطار الإجمالي
        total_frame = tk.Frame(cart_frame, bg='#27ae60')
        total_frame.pack(fill='x', padx=10, pady=5)

        self.total_label = tk.Label(total_frame, text="الإجمالي: 0.00 ج.م",
                                   font=('Arial', 14, 'bold'),
                                   fg='white', bg='#27ae60')
        self.total_label.pack(pady=10)

        # أزرار السلة
        buttons_frame = tk.Frame(cart_frame, bg='white')
        buttons_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(buttons_frame, text="إتمام البيع", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', command=self.checkout).pack(fill='x', pady=2)

        tk.Button(buttons_frame, text="مسح السلة", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=self.clear_cart).pack(fill='x', pady=2)

        tk.Button(buttons_frame, text="حذف العنصر المحدد", font=('Arial', 10),
                 bg='#f39c12', fg='white', command=self.remove_selected_item).pack(fill='x', pady=2)

        # تحميل المنتجات
        self.load_products_grid()

    def load_products(self):
        """تحميل المنتجات من قاعدة البيانات"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, price, cost, description FROM products WHERE is_active = 1')
        self.products = []
        for row in cursor.fetchall():
            self.products.append({
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'cost': row[3],
                'description': row[4]
            })

    def load_products_grid(self):
        """تحميل شبكة المنتجات"""
        # مسح المنتجات الحالية
        for widget in self.products_grid_frame.winfo_children():
            widget.destroy()

        # إنشاء أزرار المنتجات
        row = 0
        col = 0
        for product in self.products:
            product_btn = tk.Button(
                self.products_grid_frame,
                text=f"{product['name']}\n{product['price']:.2f} ج.م",
                font=('Arial', 11, 'bold'),
                bg='#3498db',
                fg='white',
                width=15,
                height=4,
                command=lambda p=product: self.add_to_cart(p)
            )
            product_btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            col += 1
            if col >= 3:  # 3 منتجات في كل صف
                col = 0
                row += 1

        # جعل الأعمدة قابلة للتوسع
        for i in range(3):
            self.products_grid_frame.columnconfigure(i, weight=1)

    def add_to_cart(self, product):
        """إضافة منتج للسلة"""
        # البحث عن المنتج في السلة
        for item in self.cart:
            if item['id'] == product['id']:
                item['quantity'] += 1
                break
        else:
            # إضافة منتج جديد
            self.cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })

        self.update_cart_display()

    def update_cart_display(self):
        """تحديث عرض السلة"""
        self.cart_listbox.delete(0, tk.END)
        self.total = 0

        for item in self.cart:
            item_total = item['price'] * item['quantity']
            self.total += item_total

            display_text = f"{item['name']} × {item['quantity']} = {item_total:.2f} ج.م"
            self.cart_listbox.insert(tk.END, display_text)

        self.total_label.config(text=f"الإجمالي: {self.total:.2f} ج.م")

    def remove_selected_item(self):
        """حذف العنصر المحدد من السلة"""
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            del self.cart[index]
            self.update_cart_display()

    def clear_cart(self):
        """مسح السلة"""
        self.cart = []
        self.update_cart_display()

    def checkout(self):
        """إتمام البيع"""
        if not self.cart:
            messagebox.showwarning("تحذير", "السلة فارغة!")
            return

        try:
            cursor = self.conn.cursor()

            # إضافة الفاتورة
            cursor.execute('INSERT INTO sales (total_amount) VALUES (?)', (self.total,))
            sale_id = cursor.lastrowid

            # إضافة عناصر الفاتورة
            for item in self.cart:
                cursor.execute(
                    'INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                    (sale_id, item['id'], item['quantity'], item['price'])
                )

            self.conn.commit()

            messagebox.showinfo("نجح", f"تم إتمام البيع بنجاح!\nرقم الفاتورة: {sale_id}\nالإجمالي: {self.total:.2f} ج.م")
            self.clear_cart()

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ البيع: {str(e)}")

    def show_products(self):
        """عرض إدارة المنتجات"""
        self.clear_main_frame()

        # إطار العنوان والأزرار
        header_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="إدارة المنتجات", font=('Arial', 18, 'bold'),
                bg='#f0f0f0').pack(side='left')

        tk.Button(header_frame, text="إضافة منتج جديد", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', command=self.add_product_dialog).pack(side='right')

        # جدول المنتجات
        columns = ('ID', 'الاسم', 'سعر البيع', 'سعر التكلفة', 'هامش الربح', 'الوصف')
        self.products_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings', height=20)

        # تعيين عناوين الأعمدة
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120)

        # شريط التمرير
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # أزرار التحكم
        control_frame = tk.Frame(self.main_frame, bg='#f0f0f0', width=200)
        control_frame.pack(side='right', fill='y', padx=(10, 0))
        control_frame.pack_propagate(False)

        tk.Button(control_frame, text="تعديل المنتج", font=('Arial', 12),
                 bg='#f39c12', fg='white', command=self.edit_product_dialog).pack(fill='x', pady=5)

        tk.Button(control_frame, text="حذف المنتج", font=('Arial', 12),
                 bg='#e74c3c', fg='white', command=self.delete_product).pack(fill='x', pady=5)

        tk.Button(control_frame, text="تحديث القائمة", font=('Arial', 12),
                 bg='#3498db', fg='white', command=self.refresh_products_list).pack(fill='x', pady=5)

        # تحميل المنتجات
        self.refresh_products_list()

    def refresh_products_list(self):
        """تحديث قائمة المنتجات"""
        # مسح البيانات الحالية
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # تحميل البيانات الجديدة
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, price, cost, description, is_active FROM products')

        for row in cursor.fetchall():
            product_id, name, price, cost, description, is_active = row

            # حساب هامش الربح
            if cost > 0:
                margin = ((price - cost) / cost) * 100
            else:
                margin = 0

            # إضافة للجدول
            status = "نشط" if is_active else "غير نشط"
            self.products_tree.insert('', 'end', values=(
                product_id, name, f"{price:.2f}", f"{cost:.2f}",
                f"{margin:.1f}%", description or "لا يوجد"
            ))

        # تحديث قائمة المنتجات للكاشير
        self.load_products()

    def add_product_dialog(self):
        """حوار إضافة منتج جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة منتج جديد")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()

        # حقول الإدخال
        tk.Label(dialog, text="اسم المنتج:", font=('Arial', 12), bg='white').pack(pady=5)
        name_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="سعر البيع (ج.م):", font=('Arial', 12), bg='white').pack(pady=5)
        price_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        price_entry.pack(pady=5)

        tk.Label(dialog, text="سعر التكلفة (ج.م):", font=('Arial', 12), bg='white').pack(pady=5)
        cost_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        cost_entry.pack(pady=5)

        tk.Label(dialog, text="الوصف:", font=('Arial', 12), bg='white').pack(pady=5)
        desc_entry = tk.Text(dialog, font=('Arial', 12), width=30, height=3)
        desc_entry.pack(pady=5)

        def save_product():
            name = name_entry.get().strip()
            try:
                price = float(price_entry.get())
                cost = float(cost_entry.get())
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للأسعار")
                return

            description = desc_entry.get(1.0, tk.END).strip()

            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم المنتج")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    'INSERT INTO products (name, price, cost, description) VALUES (?, ?, ?, ?)',
                    (name, price, cost, description)
                )
                self.conn.commit()
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح!")
                dialog.destroy()
                self.refresh_products_list()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ المنتج: {str(e)}")

        # أزرار الحفظ والإلغاء
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="حفظ", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', command=save_product).pack(side='left', padx=10)

        tk.Button(buttons_frame, text="إلغاء", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=dialog.destroy).pack(side='left', padx=10)

    def edit_product_dialog(self):
        """حوار تعديل منتج"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]

        # جلب بيانات المنتج
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, price, cost, description FROM products WHERE id = ?', (product_id,))
        product_data = cursor.fetchone()

        if not product_data:
            messagebox.showerror("خطأ", "لم يتم العثور على المنتج")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("تعديل المنتج")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()

        # حقول الإدخال مع البيانات الحالية
        tk.Label(dialog, text="اسم المنتج:", font=('Arial', 12), bg='white').pack(pady=5)
        name_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        name_entry.pack(pady=5)
        name_entry.insert(0, product_data[0])

        tk.Label(dialog, text="سعر البيع (ج.م):", font=('Arial', 12), bg='white').pack(pady=5)
        price_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        price_entry.pack(pady=5)
        price_entry.insert(0, str(product_data[1]))

        tk.Label(dialog, text="سعر التكلفة (ج.م):", font=('Arial', 12), bg='white').pack(pady=5)
        cost_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        cost_entry.pack(pady=5)
        cost_entry.insert(0, str(product_data[2]))

        tk.Label(dialog, text="الوصف:", font=('Arial', 12), bg='white').pack(pady=5)
        desc_entry = tk.Text(dialog, font=('Arial', 12), width=30, height=3)
        desc_entry.pack(pady=5)
        desc_entry.insert(1.0, product_data[3] or "")

        def update_product():
            name = name_entry.get().strip()
            try:
                price = float(price_entry.get())
                cost = float(cost_entry.get())
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للأسعار")
                return

            description = desc_entry.get(1.0, tk.END).strip()

            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم المنتج")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    'UPDATE products SET name=?, price=?, cost=?, description=? WHERE id=?',
                    (name, price, cost, description, product_id)
                )
                self.conn.commit()
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح!")
                dialog.destroy()
                self.refresh_products_list()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء تحديث المنتج: {str(e)}")

        # أزرار الحفظ والإلغاء
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="حفظ التعديلات", font=('Arial', 12, 'bold'),
                 bg='#f39c12', fg='white', command=update_product).pack(side='left', padx=10)

        tk.Button(buttons_frame, text="إلغاء", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=dialog.destroy).pack(side='left', padx=10)

    def delete_product(self):
        """حذف منتج"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]

        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف المنتج '{product_name}'؟"):
            try:
                cursor = self.conn.cursor()
                cursor.execute('UPDATE products SET is_active = 0 WHERE id = ?', (product_id,))
                self.conn.commit()
                messagebox.showinfo("نجح", "تم حذف المنتج بنجاح!")
                self.refresh_products_list()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حذف المنتج: {str(e)}")

    def show_expenses(self):
        """عرض إدارة المصروفات"""
        self.clear_main_frame()

        # إطار العنوان والأزرار
        header_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="إدارة المصروفات", font=('Arial', 18, 'bold'),
                bg='#f0f0f0').pack(side='left')

        tk.Button(header_frame, text="إضافة مصروف جديد", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=self.add_expense_dialog).pack(side='right')

        # جدول المصروفات
        columns = ('ID', 'الوصف', 'المبلغ', 'الفئة', 'التاريخ')
        self.expenses_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings', height=20)

        # تعيين عناوين الأعمدة
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=150)

        # شريط التمرير
        scrollbar2 = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=scrollbar2.set)

        self.expenses_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')

        # تحميل المصروفات
        self.refresh_expenses_list()

    def refresh_expenses_list(self):
        """تحديث قائمة المصروفات"""
        # مسح البيانات الحالية
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)

        # تحميل البيانات الجديدة
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, description, amount, category, date FROM expenses ORDER BY date DESC')

        for row in cursor.fetchall():
            expense_id, description, amount, category, date_str = row

            # تنسيق التاريخ
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = date_str

            self.expenses_tree.insert('', 'end', values=(
                expense_id, description, f"{amount:.2f} ج.م", category, formatted_date
            ))

    def add_expense_dialog(self):
        """حوار إضافة مصروف جديد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة مصروف جديد")
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()

        # حقول الإدخال
        tk.Label(dialog, text="وصف المصروف:", font=('Arial', 12), bg='white').pack(pady=5)
        desc_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        desc_entry.pack(pady=5)

        tk.Label(dialog, text="المبلغ (ج.م):", font=('Arial', 12), bg='white').pack(pady=5)
        amount_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        amount_entry.pack(pady=5)

        tk.Label(dialog, text="الفئة:", font=('Arial', 12), bg='white').pack(pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, font=('Arial', 12), width=28)
        category_combo['values'] = ('مواد خام', 'رواتب', 'إيجار', 'كهرباء', 'مياه', 'غاز',
                                   'صيانة', 'تنظيف', 'مواصلات', 'تسويق', 'أدوات', 'ضرائب', 'أخرى')
        category_combo.pack(pady=5)

        def save_expense():
            description = desc_entry.get().strip()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال رقم صحيح للمبلغ")
                return

            category = category_var.get().strip()

            if not description:
                messagebox.showerror("خطأ", "يرجى إدخال وصف المصروف")
                return

            if not category:
                messagebox.showerror("خطأ", "يرجى اختيار فئة المصروف")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    'INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)',
                    (description, amount, category)
                )
                self.conn.commit()
                messagebox.showinfo("نجح", "تم إضافة المصروف بنجاح!")
                dialog.destroy()
                self.refresh_expenses_list()
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ المصروف: {str(e)}")

        # أزرار الحفظ والإلغاء
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="حفظ", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=save_expense).pack(side='left', padx=10)

        tk.Button(buttons_frame, text="إلغاء", font=('Arial', 12, 'bold'),
                 bg='#95a5a6', fg='white', command=dialog.destroy).pack(side='left', padx=10)

    def show_reports(self):
        """عرض التقارير"""
        self.clear_main_frame()

        tk.Label(self.main_frame, text="التقارير والإحصائيات", font=('Arial', 18, 'bold'),
                bg='#f0f0f0').pack(pady=20)

        # إطار الإحصائيات
        stats_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        stats_frame.pack(fill='x', padx=20, pady=10)

        # حساب الإحصائيات
        cursor = self.conn.cursor()

        # مبيعات اليوم
        today = date.today().strftime('%Y-%m-%d')
        cursor.execute('SELECT SUM(total_amount) FROM sales WHERE DATE(date) = ?', (today,))
        today_sales = cursor.fetchone()[0] or 0

        # مصروفات اليوم
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE DATE(date) = ?', (today,))
        today_expenses = cursor.fetchone()[0] or 0

        # صافي الربح اليوم
        today_profit = today_sales - today_expenses

        # مبيعات الشهر
        current_month = date.today().strftime('%Y-%m')
        cursor.execute('SELECT SUM(total_amount) FROM sales WHERE strftime("%Y-%m", date) = ?', (current_month,))
        month_sales = cursor.fetchone()[0] or 0

        # مصروفات الشهر
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE strftime("%Y-%m", date) = ?', (current_month,))
        month_expenses = cursor.fetchone()[0] or 0

        # صافي الربح الشهر
        month_profit = month_sales - month_expenses

        # عرض الإحصائيات
        stats_data = [
            ("مبيعات اليوم", f"{today_sales:.2f} ج.م", '#27ae60'),
            ("مصروفات اليوم", f"{today_expenses:.2f} ج.م", '#e74c3c'),
            ("ربح اليوم", f"{today_profit:.2f} ج.م", '#27ae60' if today_profit >= 0 else '#e74c3c'),
            ("مبيعات الشهر", f"{month_sales:.2f} ج.م", '#3498db'),
            ("مصروفات الشهر", f"{month_expenses:.2f} ج.م", '#e67e22'),
            ("ربح الشهر", f"{month_profit:.2f} ج.م", '#27ae60' if month_profit >= 0 else '#e74c3c'),
        ]

        # إنشاء بطاقات الإحصائيات
        row = 0
        col = 0
        for title, value, color in stats_data:
            stat_frame = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            stat_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            tk.Label(stat_frame, text=title, font=('Arial', 12, 'bold'),
                    fg='white', bg=color).pack(pady=5)
            tk.Label(stat_frame, text=value, font=('Arial', 14, 'bold'),
                    fg='white', bg=color).pack(pady=5)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # جعل الأعمدة قابلة للتوسع
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)

        # إطار التوصيات
        recommendations_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=2)
        recommendations_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(recommendations_frame, text="💡 توصيات لتحسين الأداء",
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        recommendations = [
            "• راجع أسعار المنتجات بانتظام لضمان الربحية",
            "• تابع المنتجات الأكثر مبيعاً وركز عليها",
            "• قلل من المصروفات غير الضرورية",
            "• قدم عروض ترويجية في أوقات الذروة",
            "• احتفظ بسجل دقيق لجميع المعاملات",
            "• حلل تقارير المبيعات لفهم اتجاهات العملاء"
        ]

        for recommendation in recommendations:
            tk.Label(recommendations_frame, text=recommendation, font=('Arial', 12),
                    bg='white', anchor='w').pack(fill='x', padx=20, pady=2)

        # زر طباعة التقرير
        tk.Button(recommendations_frame, text="طباعة التقرير", font=('Arial', 12, 'bold'),
                 bg='#9b59b6', fg='white', command=self.print_report).pack(pady=20)

    def print_report(self):
        """طباعة التقرير (محاكاة)"""
        messagebox.showinfo("طباعة", "سيتم تطوير وظيفة الطباعة قريباً!")

    def run(self):
        """تشغيل التطبيق"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """عند إغلاق التطبيق"""
        if messagebox.askokcancel("إغلاق", "هل تريد إغلاق البرنامج؟"):
            self.conn.close()
            self.root.destroy()

# تشغيل التطبيق
if __name__ == "__main__":
    app = IceCreamCashier()
    app.run()