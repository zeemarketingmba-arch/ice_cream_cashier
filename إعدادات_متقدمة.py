#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعدادات متقدمة لبرنامج كاشير الآيس كريم
تخصيص المنتجات والأسعار والإعدادات
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class AdvancedSettings:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚙️ الإعدادات المتقدمة - كاشير الآيس كريم")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f8ff')
        
        self.settings_file = 'settings.json'
        self.products_file = 'products.json'
        
        # الإعدادات الافتراضية
        self.default_settings = {
            'currency': 'ر.ع',
            'currency_name': 'الريال العماني',
            'decimal_places': 3,
            'tax_rate': 0.0,
            'shop_name': 'محل الآيس كريم',
            'receipt_footer': 'شكراً لزيارتكم! 🍦',
            'auto_backup': True,
            'theme': 'light'
        }
        
        # المنتجات الافتراضية
        self.default_products = [
            {'id': 1, 'name': 'آيس كريم فانيليا', 'price': 1.500, 'cost': 0.800, 'category': 'كلاسيكي'},
            {'id': 2, 'name': 'آيس كريم شوكولاتة', 'price': 1.800, 'cost': 1.000, 'category': 'كلاسيكي'},
            {'id': 3, 'name': 'آيس كريم فراولة', 'price': 1.600, 'cost': 0.900, 'category': 'فواكه'},
            {'id': 4, 'name': 'آيس كريم مانجو', 'price': 2.000, 'cost': 1.200, 'category': 'فواكه'},
            {'id': 5, 'name': 'آيس كريم كوكيز', 'price': 2.200, 'cost': 1.300, 'category': 'مميز'},
            {'id': 6, 'name': 'آيس كريم كراميل', 'price': 1.900, 'cost': 1.100, 'category': 'مميز'},
            {'id': 7, 'name': 'آيس كريم فستق', 'price': 2.500, 'cost': 1.500, 'category': 'مكسرات'},
            {'id': 8, 'name': 'آيس كريم لوز', 'price': 2.300, 'cost': 1.400, 'category': 'مكسرات'},
        ]
        
        self.load_settings()
        self.load_products()
        self.create_interface()
    
    def load_settings(self):
        """تحميل الإعدادات"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.default_settings.copy()
        except:
            self.settings = self.default_settings.copy()
    
    def load_products(self):
        """تحميل المنتجات"""
        try:
            if os.path.exists(self.products_file):
                with open(self.products_file, 'r', encoding='utf-8') as f:
                    self.products = json.load(f)
            else:
                self.products = self.default_products.copy()
        except:
            self.products = self.default_products.copy()
    
    def save_settings(self):
        """حفظ الإعدادات"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الإعدادات:\n{str(e)}")
    
    def save_products(self):
        """حفظ المنتجات"""
        try:
            with open(self.products_file, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ المنتجات:\n{str(e)}")
    
    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        # العنوان
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="⚙️ الإعدادات المتقدمة", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # دفتر التبويبات
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # تبويب الإعدادات العامة
        general_frame = tk.Frame(notebook, bg='white')
        notebook.add(general_frame, text="🏪 إعدادات عامة")
        self.create_general_settings(general_frame)
        
        # تبويب المنتجات
        products_frame = tk.Frame(notebook, bg='white')
        notebook.add(products_frame, text="🍦 إدارة المنتجات")
        self.create_products_management(products_frame)
        
        # تبويب العملة والأسعار
        currency_frame = tk.Frame(notebook, bg='white')
        notebook.add(currency_frame, text="💰 العملة والأسعار")
        self.create_currency_settings(currency_frame)
        
        # تبويب النسخ الاحتياطية
        backup_frame = tk.Frame(notebook, bg='white')
        notebook.add(backup_frame, text="💾 النسخ الاحتياطية")
        self.create_backup_settings(backup_frame)
        
        # أزرار الحفظ والإلغاء
        buttons_frame = tk.Frame(self.root, bg='#f0f8ff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(buttons_frame, text="💾 حفظ جميع الإعدادات", 
                 font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                 command=self.save_all_settings).pack(side='left', padx=10)
        
        tk.Button(buttons_frame, text="🔄 استعادة الافتراضية", 
                 font=('Arial', 12), bg='#f39c12', fg='white',
                 command=self.reset_to_defaults).pack(side='left', padx=10)
        
        tk.Button(buttons_frame, text="❌ إغلاق", 
                 font=('Arial', 12), bg='#95a5a6', fg='white',
                 command=self.root.destroy).pack(side='right', padx=10)
    
    def create_general_settings(self, parent):
        """إنشاء إعدادات عامة"""
        # اسم المحل
        tk.Label(parent, text="🏪 اسم المحل:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.shop_name_var = tk.StringVar(value=self.settings.get('shop_name', ''))
        tk.Entry(parent, textvariable=self.shop_name_var, font=('Arial', 12), width=40).pack(anchor='w', padx=20, pady=5)
        
        # نص الفاتورة
        tk.Label(parent, text="🧾 نص نهاية الفاتورة:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.receipt_footer_var = tk.StringVar(value=self.settings.get('receipt_footer', ''))
        tk.Entry(parent, textvariable=self.receipt_footer_var, font=('Arial', 12), width=40).pack(anchor='w', padx=20, pady=5)
        
        # معدل الضريبة
        tk.Label(parent, text="📊 معدل الضريبة (%):", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.tax_rate_var = tk.DoubleVar(value=self.settings.get('tax_rate', 0.0) * 100)
        tk.Scale(parent, from_=0, to=25, orient='horizontal', variable=self.tax_rate_var, 
                resolution=0.1, length=300).pack(anchor='w', padx=20, pady=5)
        
        # النسخ الاحتياطية التلقائية
        self.auto_backup_var = tk.BooleanVar(value=self.settings.get('auto_backup', True))
        tk.Checkbutton(parent, text="💾 تفعيل النسخ الاحتياطية التلقائية", 
                      variable=self.auto_backup_var, font=('Arial', 12), bg='white').pack(anchor='w', padx=20, pady=10)
    
    def create_products_management(self, parent):
        """إدارة المنتجات"""
        # إطار الأزرار
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(buttons_frame, text="➕ إضافة منتج", 
                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                 command=self.add_product).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="✏️ تعديل منتج", 
                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                 command=self.edit_product).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="🗑️ حذف منتج", 
                 font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                 command=self.delete_product).pack(side='left', padx=5)
        
        # جدول المنتجات
        columns = ('ID', 'الاسم', 'السعر', 'التكلفة', 'الفئة', 'الربح')
        self.products_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # تعريف الأعمدة
        self.products_tree.heading('ID', text='الرقم')
        self.products_tree.heading('الاسم', text='اسم المنتج')
        self.products_tree.heading('السعر', text='السعر (ر.ع)')
        self.products_tree.heading('التكلفة', text='التكلفة (ر.ع)')
        self.products_tree.heading('الفئة', text='الفئة')
        self.products_tree.heading('الربح', text='الربح (ر.ع)')
        
        # تحديد عرض الأعمدة
        self.products_tree.column('ID', width=50)
        self.products_tree.column('الاسم', width=200)
        self.products_tree.column('السعر', width=100)
        self.products_tree.column('التكلفة', width=100)
        self.products_tree.column('الفئة', width=100)
        self.products_tree.column('الربح', width=100)
        
        self.products_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # تحديث جدول المنتجات
        self.update_products_tree()
    
    def create_currency_settings(self, parent):
        """إعدادات العملة"""
        # العملة
        tk.Label(parent, text="💰 رمز العملة:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.currency_var = tk.StringVar(value=self.settings.get('currency', 'ر.ع'))
        tk.Entry(parent, textvariable=self.currency_var, font=('Arial', 12), width=20).pack(anchor='w', padx=20, pady=5)
        
        # اسم العملة
        tk.Label(parent, text="🏷️ اسم العملة:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.currency_name_var = tk.StringVar(value=self.settings.get('currency_name', 'الريال العماني'))
        tk.Entry(parent, textvariable=self.currency_name_var, font=('Arial', 12), width=30).pack(anchor='w', padx=20, pady=5)
        
        # عدد الخانات العشرية
        tk.Label(parent, text="🔢 عدد الخانات العشرية:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=5)
        self.decimal_places_var = tk.IntVar(value=self.settings.get('decimal_places', 3))
        tk.Scale(parent, from_=0, to=5, orient='horizontal', variable=self.decimal_places_var, 
                length=200).pack(anchor='w', padx=20, pady=5)
        
        # عملات شائعة
        tk.Label(parent, text="💱 عملات شائعة:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=20, pady=10)
        
        currencies_frame = tk.Frame(parent, bg='white')
        currencies_frame.pack(anchor='w', padx=20, pady=5)
        
        common_currencies = [
            ('الريال العماني', 'ر.ع'),
            ('الدرهم الإماراتي', 'د.إ'),
            ('الريال السعودي', 'ر.س'),
            ('الدينار الكويتي', 'د.ك'),
            ('الدولار الأمريكي', '$'),
            ('اليورو', '€')
        ]
        
        for name, symbol in common_currencies:
            tk.Button(currencies_frame, text=f"{name} ({symbol})", 
                     font=('Arial', 10), bg='#ecf0f1', 
                     command=lambda n=name, s=symbol: self.set_currency(n, s)).pack(side='left', padx=5, pady=2)
    
    def create_backup_settings(self, parent):
        """إعدادات النسخ الاحتياطية"""
        tk.Label(parent, text="💾 إدارة النسخ الاحتياطية", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        # أزرار النسخ الاحتياطية
        backup_buttons_frame = tk.Frame(parent, bg='white')
        backup_buttons_frame.pack(pady=20)
        
        tk.Button(backup_buttons_frame, text="📁 إنشاء نسخة احتياطية الآن", 
                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                 command=self.create_backup).pack(pady=5, fill='x')
        
        tk.Button(backup_buttons_frame, text="🔄 استعادة من نسخة احتياطية", 
                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                 command=self.restore_backup).pack(pady=5, fill='x')
        
        tk.Button(backup_buttons_frame, text="🗂️ فتح مجلد النسخ الاحتياطية", 
                 font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white',
                 command=self.open_backup_folder).pack(pady=5, fill='x')
        
        # معلومات النسخ الاحتياطية
        info_frame = tk.LabelFrame(parent, text="ℹ️ معلومات", font=('Arial', 12, 'bold'), bg='white')
        info_frame.pack(fill='x', padx=20, pady=20)
        
        info_text = """💡 نصائح للنسخ الاحتياطية:

✅ قم بإنشاء نسخة احتياطية يومياً
✅ احتفظ بنسخ في مكان آمن
✅ تحقق من النسخ بانتظام
✅ استخدم أسماء واضحة للملفات

📁 مكان النسخ الافتراضي: مجلد backups"""
        
        tk.Label(info_frame, text=info_text, font=('Arial', 10), 
                bg='white', justify='left').pack(padx=10, pady=10)
    
    def update_products_tree(self):
        """تحديث جدول المنتجات"""
        # مسح البيانات الحالية
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # إضافة المنتجات
        for product in self.products:
            profit = product['price'] - product['cost']
            self.products_tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                f"{product['price']:.3f}",
                f"{product['cost']:.3f}",
                product.get('category', 'عام'),
                f"{profit:.3f}"
            ))
    
    def add_product(self):
        """إضافة منتج جديد"""
        self.product_dialog()
    
    def edit_product(self):
        """تعديل منتج"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للتعديل")
            return
        
        item = self.products_tree.item(selection[0])
        product_id = int(item['values'][0])
        
        # البحث عن المنتج
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            self.product_dialog(product)
    
    def delete_product(self):
        """حذف منتج"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج للحذف")
            return
        
        item = self.products_tree.item(selection[0])
        product_id = int(item['values'][0])
        product_name = item['values'][1]
        
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف المنتج:\n{product_name}"):
            self.products = [p for p in self.products if p['id'] != product_id]
            self.update_products_tree()
    
    def product_dialog(self, product=None):
        """نافذة إضافة/تعديل منتج"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إضافة منتج" if product is None else "تعديل منتج")
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # الحقول
        tk.Label(dialog, text="اسم المنتج:", font=('Arial', 12), bg='white').pack(pady=5)
        name_var = tk.StringVar(value=product['name'] if product else '')
        tk.Entry(dialog, textvariable=name_var, font=('Arial', 12), width=30).pack(pady=5)
        
        tk.Label(dialog, text="سعر البيع (ر.ع):", font=('Arial', 12), bg='white').pack(pady=5)
        price_var = tk.DoubleVar(value=product['price'] if product else 0.0)
        tk.Entry(dialog, textvariable=price_var, font=('Arial', 12), width=30).pack(pady=5)
        
        tk.Label(dialog, text="سعر التكلفة (ر.ع):", font=('Arial', 12), bg='white').pack(pady=5)
        cost_var = tk.DoubleVar(value=product['cost'] if product else 0.0)
        tk.Entry(dialog, textvariable=cost_var, font=('Arial', 12), width=30).pack(pady=5)
        
        tk.Label(dialog, text="الفئة:", font=('Arial', 12), bg='white').pack(pady=5)
        category_var = tk.StringVar(value=product.get('category', 'عام') if product else 'عام')
        category_combo = ttk.Combobox(dialog, textvariable=category_var, 
                                     values=['كلاسيكي', 'فواكه', 'مميز', 'مكسرات', 'عام'])
        category_combo.pack(pady=5)
        
        def save_product():
            name = name_var.get().strip()
            try:
                price = price_var.get()
                cost = cost_var.get()
            except:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للأسعار")
                return
            
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم المنتج")
                return
            
            if price <= 0 or cost < 0:
                messagebox.showerror("خطأ", "يرجى إدخال أسعار صحيحة")
                return
            
            if product:  # تعديل
                product['name'] = name
                product['price'] = price
                product['cost'] = cost
                product['category'] = category_var.get()
            else:  # إضافة جديد
                new_id = max([p['id'] for p in self.products]) + 1 if self.products else 1
                new_product = {
                    'id': new_id,
                    'name': name,
                    'price': price,
                    'cost': cost,
                    'category': category_var.get()
                }
                self.products.append(new_product)
            
            self.update_products_tree()
            dialog.destroy()
        
        # أزرار
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="💾 حفظ", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', command=save_product).pack(side='left', padx=10)
        
        tk.Button(buttons_frame, text="❌ إلغاء", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', command=dialog.destroy).pack(side='left', padx=10)
    
    def set_currency(self, name, symbol):
        """تعيين العملة"""
        self.currency_name_var.set(name)
        self.currency_var.set(symbol)
    
    def save_all_settings(self):
        """حفظ جميع الإعدادات"""
        try:
            # تحديث الإعدادات
            self.settings['shop_name'] = self.shop_name_var.get()
            self.settings['receipt_footer'] = self.receipt_footer_var.get()
            self.settings['tax_rate'] = self.tax_rate_var.get() / 100
            self.settings['auto_backup'] = self.auto_backup_var.get()
            self.settings['currency'] = self.currency_var.get()
            self.settings['currency_name'] = self.currency_name_var.get()
            self.settings['decimal_places'] = self.decimal_places_var.get()
            
            # حفظ الملفات
            self.save_settings()
            self.save_products()
            
            messagebox.showinfo("نجح", "تم حفظ جميع الإعدادات بنجاح!")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الإعدادات:\n{str(e)}")
    
    def reset_to_defaults(self):
        """استعادة الإعدادات الافتراضية"""
        if messagebox.askyesno("تأكيد", "هل تريد استعادة جميع الإعدادات الافتراضية؟"):
            self.settings = self.default_settings.copy()
            self.products = self.default_products.copy()
            
            # تحديث الواجهة
            self.shop_name_var.set(self.settings['shop_name'])
            self.receipt_footer_var.set(self.settings['receipt_footer'])
            self.tax_rate_var.set(self.settings['tax_rate'] * 100)
            self.auto_backup_var.set(self.settings['auto_backup'])
            self.currency_var.set(self.settings['currency'])
            self.currency_name_var.set(self.settings['currency_name'])
            self.decimal_places_var.set(self.settings['decimal_places'])
            
            self.update_products_tree()
            
            messagebox.showinfo("تم", "تم استعادة الإعدادات الافتراضية")
    
    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        try:
            # استيراد أداة النسخ الاحتياطية
            import subprocess
            subprocess.run([sys.executable, 'نسخة_احتياطية.py'])
        except:
            messagebox.showinfo("معلومات", "يرجى تشغيل ملف 'نسخة_احتياطية.py' منفصلاً")
    
    def restore_backup(self):
        """استعادة نسخة احتياطية"""
        try:
            import subprocess
            subprocess.run([sys.executable, 'نسخة_احتياطية.py'])
        except:
            messagebox.showinfo("معلومات", "يرجى تشغيل ملف 'نسخة_احتياطية.py' منفصلاً")
    
    def open_backup_folder(self):
        """فتح مجلد النسخ الاحتياطية"""
        try:
            import subprocess
            backup_folder = 'backups'
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            subprocess.run(['explorer', backup_folder])
        except:
            messagebox.showinfo("معلومات", "مجلد النسخ الاحتياطية: backups")
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedSettings()
    app.run()
