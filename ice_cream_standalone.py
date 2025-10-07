#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج كاشير الآيس كريم - نسخة مستقلة
تعمل مع Python المدمج في Windows
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    import json
    import os
    from datetime import datetime
    
    class SimpleIceCreamCashier:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("🍦 كاشير الآيس كريم")
            self.root.geometry("1000x700")
            self.root.configure(bg='#e8f4fd')
            
            # بيانات المنتجات (محفوظة في الذاكرة) - الأسعار بالريال العماني
            self.products = [
                {'id': 1, 'name': 'آيس كريم فانيليا', 'price': 1.500, 'cost': 0.800},
                {'id': 2, 'name': 'آيس كريم شوكولاتة', 'price': 1.800, 'cost': 1.000},
                {'id': 3, 'name': 'آيس كريم فراولة', 'price': 1.600, 'cost': 0.900},
                {'id': 4, 'name': 'آيس كريم مانجو', 'price': 2.000, 'cost': 1.200},
                {'id': 5, 'name': 'آيس كريم كوكيز', 'price': 2.200, 'cost': 1.300},
                {'id': 6, 'name': 'آيس كريم كراميل', 'price': 1.900, 'cost': 1.100},
            ]
            
            # بيانات السلة والمبيعات
            self.cart = []
            self.total_sales = 0.0
            self.total_expenses = 45.0  # مصروفات افتراضية بالريال العماني
            self.sales_history = []
            
            # تحميل البيانات المحفوظة
            self.load_data()
            
            # إنشاء الواجهة
            self.create_interface()
        
        def load_data(self):
            """تحميل البيانات المحفوظة"""
            try:
                if os.path.exists('cashier_data.json'):
                    with open('cashier_data.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.total_sales = data.get('total_sales', 0.0)
                        self.total_expenses = data.get('total_expenses', 45.0)
                        self.sales_history = data.get('sales_history', [])
            except:
                pass
        
        def save_data(self):
            """حفظ البيانات"""
            try:
                data = {
                    'total_sales': self.total_sales,
                    'total_expenses': self.total_expenses,
                    'sales_history': self.sales_history
                }
                with open('cashier_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except:
                pass
        
        def create_interface(self):
            """إنشاء واجهة المستخدم"""
            # العنوان الرئيسي
            title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
            title_frame.pack(fill='x')
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(title_frame, text="🍦 كاشير الآيس كريم", 
                                  font=('Arial', 20, 'bold'), 
                                  fg='white', bg='#2c3e50')
            title_label.pack(expand=True)
            
            # الإطار الرئيسي
            main_frame = tk.Frame(self.root, bg='#e8f4fd')
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # إطار المنتجات (يسار)
            products_frame = tk.LabelFrame(main_frame, text="المنتجات المتاحة", 
                                         font=('Arial', 14, 'bold'), 
                                         bg='white', fg='#2c3e50')
            products_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
            
            # شبكة المنتجات
            products_grid = tk.Frame(products_frame, bg='white')
            products_grid.pack(fill='both', expand=True, padx=10, pady=10)
            
            # إنشاء أزرار المنتجات
            row = 0
            col = 0
            for product in self.products:
                btn = tk.Button(products_grid, 
                               text=f"{product['name']}\n{product['price']:.3f} ر.ع",
                               font=('Arial', 11, 'bold'),
                               bg='#3498db', fg='white',
                               width=18, height=4,
                               command=lambda p=product: self.add_to_cart(p))
                btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                
                col += 1
                if col >= 2:  # عمودين
                    col = 0
                    row += 1
            
            # جعل الشبكة قابلة للتوسع
            for i in range(2):
                products_grid.columnconfigure(i, weight=1)
            
            # إطار السلة (يمين)
            cart_frame = tk.LabelFrame(main_frame, text="سلة المشتريات", 
                                     font=('Arial', 14, 'bold'), 
                                     bg='white', fg='#2c3e50', width=350)
            cart_frame.pack(side='right', fill='y', padx=(5, 0))
            cart_frame.pack_propagate(False)
            
            # قائمة السلة
            self.cart_listbox = tk.Listbox(cart_frame, font=('Arial', 10), height=12)
            self.cart_listbox.pack(fill='both', expand=True, padx=10, pady=10)
            
            # إطار الإجمالي
            total_frame = tk.Frame(cart_frame, bg='#27ae60', height=50)
            total_frame.pack(fill='x', padx=10, pady=5)
            total_frame.pack_propagate(False)
            
            self.total_label = tk.Label(total_frame, text="الإجمالي: 0.000 ر.ع",
                                       font=('Arial', 14, 'bold'), 
                                       fg='white', bg='#27ae60')
            self.total_label.pack(expand=True)
            
            # أزرار التحكم
            buttons_frame = tk.Frame(cart_frame, bg='white')
            buttons_frame.pack(fill='x', padx=10, pady=10)
            
            tk.Button(buttons_frame, text="إتمام البيع", 
                     font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                     command=self.checkout).pack(fill='x', pady=2)
            
            tk.Button(buttons_frame, text="مسح السلة", 
                     font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                     command=self.clear_cart).pack(fill='x', pady=2)
            
            tk.Button(buttons_frame, text="حذف العنصر المحدد", 
                     font=('Arial', 10), bg='#f39c12', fg='white',
                     command=self.remove_selected).pack(fill='x', pady=2)
            
            tk.Button(buttons_frame, text="عرض التقارير", 
                     font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white',
                     command=self.show_reports).pack(fill='x', pady=2)
        
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
            total = 0
            
            for item in self.cart:
                item_total = item['price'] * item['quantity']
                total += item_total
                
                display_text = f"{item['name']} × {item['quantity']} = {item_total:.3f} ر.ع"
                self.cart_listbox.insert(tk.END, display_text)
            
            self.total_label.config(text=f"الإجمالي: {total:.3f} ر.ع")
        
        def remove_selected(self):
            """حذف العنصر المحدد"""
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
            
            # حساب الإجمالي
            total = sum(item['price'] * item['quantity'] for item in self.cart)
            
            # إضافة للمبيعات
            self.total_sales += total
            sale_record = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'items': self.cart.copy(),
                'total': total
            }
            self.sales_history.append(sale_record)
            
            # حفظ البيانات
            self.save_data()
            
            messagebox.showinfo("نجح", f"تم إتمام البيع بنجاح!\nالإجمالي: {total:.3f} ر.ع")
            self.clear_cart()
        
        def show_reports(self):
            """عرض التقارير"""
            reports_window = tk.Toplevel(self.root)
            reports_window.title("التقارير والإحصائيات")
            reports_window.geometry("600x500")
            reports_window.configure(bg='white')
            reports_window.transient(self.root)
            
            # العنوان
            tk.Label(reports_window, text="📊 التقارير والإحصائيات", 
                    font=('Arial', 18, 'bold'), bg='white').pack(pady=20)
            
            # الإحصائيات
            stats_frame = tk.Frame(reports_window, bg='white')
            stats_frame.pack(fill='x', padx=20, pady=10)
            
            # مبيعات اليوم (محاكاة)
            today_sales = sum(sale['total'] for sale in self.sales_history 
                            if sale['date'].startswith(datetime.now().strftime('%Y-%m-%d')))
            
            profit = self.total_sales - self.total_expenses
            
            stats_data = [
                ("إجمالي المبيعات", f"{self.total_sales:.3f} ر.ع", '#27ae60'),
                ("إجمالي المصروفات", f"{self.total_expenses:.3f} ر.ع", '#e74c3c'),
                ("صافي الربح", f"{profit:.3f} ر.ع", '#27ae60' if profit >= 0 else '#e74c3c'),
                ("عدد الفواتير", f"{len(self.sales_history)}", '#3498db'),
            ]
            
            row = 0
            col = 0
            for title, value, color in stats_data:
                stat_frame = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
                stat_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                tk.Label(stat_frame, text=title, font=('Arial', 11, 'bold'), 
                        fg='white', bg=color).pack(pady=5)
                tk.Label(stat_frame, text=value, font=('Arial', 13, 'bold'), 
                        fg='white', bg=color).pack(pady=5)
                
                col += 1
                if col >= 2:
                    col = 0
                    row += 1
            
            # جعل الأعمدة قابلة للتوسع
            for i in range(2):
                stats_frame.columnconfigure(i, weight=1)
            
            # آخر المبيعات
            tk.Label(reports_window, text="آخر المبيعات:", 
                    font=('Arial', 14, 'bold'), bg='white').pack(pady=(20, 10))
            
            sales_listbox = tk.Listbox(reports_window, font=('Arial', 10), height=8)
            sales_listbox.pack(fill='both', expand=True, padx=20, pady=10)
            
            # عرض آخر 10 مبيعات
            for sale in self.sales_history[-10:]:
                items_text = ", ".join([f"{item['name']} ×{item['quantity']}" 
                                      for item in sale['items']])
                display_text = f"{sale['date']} - {sale['total']:.3f} ر.ع - {items_text}"
                sales_listbox.insert(0, display_text)  # إدراج في البداية
            
            # زر إغلاق
            tk.Button(reports_window, text="إغلاق", font=('Arial', 12, 'bold'),
                     bg='#95a5a6', fg='white', 
                     command=reports_window.destroy).pack(pady=20)
        
        def run(self):
            """تشغيل التطبيق"""
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        
        def on_closing(self):
            """عند إغلاق التطبيق"""
            self.save_data()
            self.root.destroy()
    
    # تشغيل التطبيق
    if __name__ == "__main__":
        try:
            app = SimpleIceCreamCashier()
            app.run()
        except Exception as e:
            print(f"خطأ في تشغيل التطبيق: {e}")
            input("اضغط Enter للخروج...")

except ImportError:
    print("❌ Tkinter غير متاح!")
    print("يرجى تثبيت Python مع Tkinter")
    input("اضغط Enter للخروج...")
except Exception as e:
    print(f"❌ خطأ: {e}")
    input("اضغط Enter للخروج...")
