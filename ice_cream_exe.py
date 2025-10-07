#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج كاشير الآيس كريم - نسخة الملف التنفيذي
محسن للتوزيع كملف exe مستقل
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class IceCreamCashierEXE:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍦 كاشير الآيس كريم - الريال العماني")
        self.root.geometry("1100x750")
        self.root.configure(bg='#e8f4fd')
        
        # تحديد مجلد البيانات
        if getattr(sys, 'frozen', False):
            # إذا كان ملف تنفيذي
            self.app_dir = os.path.dirname(sys.executable)
        else:
            # إذا كان ملف Python عادي
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.data_file = os.path.join(self.app_dir, 'cashier_data.json')
        
        # بيانات المنتجات - الأسعار بالريال العماني
        self.products = [
            {'id': 1, 'name': 'آيس كريم فانيليا', 'price': 1.500, 'cost': 0.800},
            {'id': 2, 'name': 'آيس كريم شوكولاتة', 'price': 1.800, 'cost': 1.000},
            {'id': 3, 'name': 'آيس كريم فراولة', 'price': 1.600, 'cost': 0.900},
            {'id': 4, 'name': 'آيس كريم مانجو', 'price': 2.000, 'cost': 1.200},
            {'id': 5, 'name': 'آيس كريم كوكيز', 'price': 2.200, 'cost': 1.300},
            {'id': 6, 'name': 'آيس كريم كراميل', 'price': 1.900, 'cost': 1.100},
            {'id': 7, 'name': 'آيس كريم فستق', 'price': 2.500, 'cost': 1.500},
            {'id': 8, 'name': 'آيس كريم لوز', 'price': 2.300, 'cost': 1.400},
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
        
        # رسالة ترحيب
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """عرض رسالة ترحيب"""
        welcome_msg = """🍦 مرحباً بك في برنامج كاشير الآيس كريم!

✅ العملة: الريال العماني (ر.ع)
✅ حفظ البيانات تلقائياً
✅ تقارير مفصلة
✅ واجهة سهلة الاستخدام

💡 نصائح سريعة:
• انقر على المنتجات لإضافتها للسلة
• استخدم أزرار + و - لتعديل الكمية
• راجع التقارير لمتابعة الأرباح

🚀 ابدأ البيع الآن!"""
        
        messagebox.showinfo("مرحباً! 🍦", welcome_msg)
    
    def load_data(self):
        """تحميل البيانات المحفوظة"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.total_sales = data.get('total_sales', 0.0)
                    self.total_expenses = data.get('total_expenses', 45.0)
                    self.sales_history = data.get('sales_history', [])
        except Exception as e:
            print(f"خطأ في تحميل البيانات: {e}")
    
    def save_data(self):
        """حفظ البيانات"""
        try:
            data = {
                'total_sales': self.total_sales,
                'total_expenses': self.total_expenses,
                'sales_history': self.sales_history,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")
    
    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🍦 كاشير الآيس كريم - الريال العماني", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # شريط المعلومات
        info_frame = tk.Frame(self.root, bg='#34495e', height=40)
        info_frame.pack(fill='x')
        info_frame.pack_propagate(False)
        
        info_label = tk.Label(info_frame, 
                             text=f"💰 إجمالي المبيعات: {self.total_sales:.3f} ر.ع | 📊 عدد الفواتير: {len(self.sales_history)}", 
                             font=('Arial', 12), 
                             fg='white', bg='#34495e')
        info_label.pack(expand=True)
        
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
                           font=('Arial', 10, 'bold'),
                           bg='#3498db', fg='white',
                           width=16, height=4,
                           command=lambda p=product: self.add_to_cart(p))
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            
            col += 1
            if col >= 3:  # 3 أعمدة
                col = 0
                row += 1
        
        # جعل الشبكة قابلة للتوسع
        for i in range(3):
            products_grid.columnconfigure(i, weight=1)
        
        # إطار السلة (يمين)
        cart_frame = tk.LabelFrame(main_frame, text="سلة المشتريات", 
                                 font=('Arial', 14, 'bold'), 
                                 bg='white', fg='#2c3e50', width=380)
        cart_frame.pack(side='right', fill='y', padx=(5, 0))
        cart_frame.pack_propagate(False)
        
        # قائمة السلة
        self.cart_listbox = tk.Listbox(cart_frame, font=('Arial', 10), height=14)
        self.cart_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # إطار الإجمالي
        total_frame = tk.Frame(cart_frame, bg='#27ae60', height=60)
        total_frame.pack(fill='x', padx=10, pady=5)
        total_frame.pack_propagate(False)
        
        self.total_label = tk.Label(total_frame, text="الإجمالي: 0.000 ر.ع", 
                                   font=('Arial', 16, 'bold'), 
                                   fg='white', bg='#27ae60')
        self.total_label.pack(expand=True)
        
        # أزرار التحكم
        buttons_frame = tk.Frame(cart_frame, bg='white')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(buttons_frame, text="💳 إتمام البيع", 
                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                 command=self.checkout).pack(fill='x', pady=2)
        
        tk.Button(buttons_frame, text="🗑️ مسح السلة", 
                 font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                 command=self.clear_cart).pack(fill='x', pady=2)
        
        tk.Button(buttons_frame, text="❌ حذف المحدد", 
                 font=('Arial', 10), bg='#f39c12', fg='white',
                 command=self.remove_selected).pack(fill='x', pady=2)
        
        tk.Button(buttons_frame, text="📊 التقارير", 
                 font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white',
                 command=self.show_reports).pack(fill='x', pady=2)
        
        tk.Button(buttons_frame, text="ℹ️ حول البرنامج", 
                 font=('Arial', 10), bg='#95a5a6', fg='white',
                 command=self.show_about).pack(fill='x', pady=2)
    
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
        else:
            messagebox.showwarning("تحذير", "يرجى اختيار عنصر لحذفه")
    
    def clear_cart(self):
        """مسح السلة"""
        if self.cart:
            if messagebox.askyesno("تأكيد", "هل تريد مسح جميع العناصر من السلة؟"):
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
        
        # رسالة النجاح
        success_msg = f"""✅ تم إتمام البيع بنجاح!

🧾 رقم الفاتورة: {len(self.sales_history)}
💰 الإجمالي: {total:.3f} ر.ع
📅 التاريخ: {sale_record['date']}

شكراً لك! 🍦"""
        
        messagebox.showinfo("نجح البيع! 🎉", success_msg)
        self.clear_cart()
        
        # تحديث شريط المعلومات
        self.update_info_bar()
    
    def update_info_bar(self):
        """تحديث شريط المعلومات"""
        # البحث عن شريط المعلومات وتحديثه
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#34495e':
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(text=f"💰 إجمالي المبيعات: {self.total_sales:.3f} ر.ع | 📊 عدد الفواتير: {len(self.sales_history)}")
                        break
                break

    def show_reports(self):
        """عرض التقارير"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("📊 التقارير والإحصائيات")
        reports_window.geometry("700x600")
        reports_window.configure(bg='white')
        reports_window.transient(self.root)
        reports_window.grab_set()

        # العنوان
        tk.Label(reports_window, text="📊 التقارير والإحصائيات",
                font=('Arial', 18, 'bold'), bg='white').pack(pady=20)

        # الإحصائيات
        stats_frame = tk.Frame(reports_window, bg='white')
        stats_frame.pack(fill='x', padx=20, pady=10)

        # مبيعات اليوم
        today_sales = sum(sale['total'] for sale in self.sales_history
                        if sale['date'].startswith(datetime.now().strftime('%Y-%m-%d')))

        profit = self.total_sales - self.total_expenses

        stats_data = [
            ("إجمالي المبيعات", f"{self.total_sales:.3f} ر.ع", '#27ae60'),
            ("إجمالي المصروفات", f"{self.total_expenses:.3f} ر.ع", '#e74c3c'),
            ("صافي الربح", f"{profit:.3f} ر.ع", '#27ae60' if profit >= 0 else '#e74c3c'),
            ("عدد الفواتير", f"{len(self.sales_history)}", '#3498db'),
            ("مبيعات اليوم", f"{today_sales:.3f} ر.ع", '#f39c12'),
            ("متوسط الفاتورة", f"{(self.total_sales/len(self.sales_history) if self.sales_history else 0):.3f} ر.ع", '#9b59b6'),
        ]

        row = 0
        col = 0
        for title, value, color in stats_data:
            stat_frame = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            stat_frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')

            tk.Label(stat_frame, text=title, font=('Arial', 10, 'bold'),
                    fg='white', bg=color).pack(pady=3)
            tk.Label(stat_frame, text=value, font=('Arial', 12, 'bold'),
                    fg='white', bg=color).pack(pady=3)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        # جعل الأعمدة قابلة للتوسع
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)

        # آخر المبيعات
        tk.Label(reports_window, text="🧾 آخر المبيعات:",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(20, 10))

        # إطار قائمة المبيعات مع شريط تمرير
        sales_frame = tk.Frame(reports_window, bg='white')
        sales_frame.pack(fill='both', expand=True, padx=20, pady=10)

        sales_listbox = tk.Listbox(sales_frame, font=('Arial', 10), height=10)
        scrollbar = tk.Scrollbar(sales_frame, orient='vertical', command=sales_listbox.yview)
        sales_listbox.configure(yscrollcommand=scrollbar.set)

        sales_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # عرض آخر 20 مبيعة
        for sale in self.sales_history[-20:]:
            items_text = ", ".join([f"{item['name']} ×{item['quantity']}"
                                  for item in sale['items']])
            display_text = f"{sale['date']} - {sale['total']:.3f} ر.ع - {items_text}"
            sales_listbox.insert(0, display_text)  # إدراج في البداية

        # أزرار
        buttons_frame = tk.Frame(reports_window, bg='white')
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="🖨️ طباعة التقرير", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white', command=self.print_report).pack(side='left', padx=10)

        tk.Button(buttons_frame, text="❌ إغلاق", font=('Arial', 12, 'bold'),
                 bg='#95a5a6', fg='white',
                 command=reports_window.destroy).pack(side='left', padx=10)

    def print_report(self):
        """طباعة التقرير (محاكاة)"""
        report_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🍦 كاشير الآيس كريم 🍦                    ║
║                      تقرير المبيعات                         ║
╚══════════════════════════════════════════════════════════════╝

📅 تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}
💰 العملة: الريال العماني (ر.ع)

📊 الإحصائيات العامة:
═══════════════════════════════════════════════════════════════
• إجمالي المبيعات: {self.total_sales:.3f} ر.ع
• إجمالي المصروفات: {self.total_expenses:.3f} ر.ع
• صافي الربح: {(self.total_sales - self.total_expenses):.3f} ر.ع
• عدد الفواتير: {len(self.sales_history)}
• متوسط الفاتورة: {(self.total_sales/len(self.sales_history) if self.sales_history else 0):.3f} ر.ع

🧾 آخر 10 مبيعات:
═══════════════════════════════════════════════════════════════
"""

        for sale in self.sales_history[-10:]:
            items_text = ", ".join([f"{item['name']} ×{item['quantity']}" for item in sale['items']])
            report_text += f"• {sale['date']} - {sale['total']:.3f} ر.ع - {items_text}\n"

        report_text += "\n═══════════════════════════════════════════════════════════════\nشكراً لاستخدام برنامج كاشير الآيس كريم! 🍦"

        # حفظ التقرير في ملف
        try:
            report_file = os.path.join(self.app_dir, f"تقرير_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_text)

            messagebox.showinfo("تم الحفظ", f"تم حفظ التقرير في:\n{report_file}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ التقرير:\n{str(e)}")

    def show_about(self):
        """عرض معلومات البرنامج"""
        about_text = """🍦 برنامج كاشير الآيس كريم

📋 الإصدار: 1.0
💰 العملة: الريال العماني (ر.ع)
👨‍💻 المطور: Augment Agent
📅 تاريخ الإنشاء: 2024

✨ المميزات:
• واجهة سهلة الاستخدام
• حفظ البيانات تلقائياً
• تقارير مفصلة
• حسابات دقيقة للأرباح والخسائر
• دعم كامل للغة العربية

🎯 الهدف:
مساعدة أصحاب محلات الآيس كريم في إدارة مبيعاتهم
بطريقة سهلة ومنظمة مع متابعة الأرباح والخسائر.

💡 نصائح:
• أضف منتجاتك الحقيقية
• سجل المصروفات بانتظام
• راجع التقارير يومياً
• احتفظ بنسخة احتياطية من البيانات

شكراً لاستخدام البرنامج! 🙏"""

        messagebox.showinfo("حول البرنامج", about_text)

    def run(self):
        """تشغيل التطبيق"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # وضع النافذة في المنتصف
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

        self.root.mainloop()

    def on_closing(self):
        """عند إغلاق التطبيق"""
        if messagebox.askokcancel("إغلاق البرنامج", "هل تريد إغلاق برنامج كاشير الآيس كريم؟"):
            self.save_data()
            self.root.destroy()

# تشغيل التطبيق
if __name__ == "__main__":
    try:
        app = IceCreamCashierEXE()
        app.run()
    except Exception as e:
        import traceback
        error_msg = f"حدث خطأ في تشغيل البرنامج:\n\n{str(e)}\n\nتفاصيل الخطأ:\n{traceback.format_exc()}"

        try:
            import tkinter.messagebox as mb
            mb.showerror("خطأ في البرنامج", error_msg)
        except:
            print(error_msg)
            input("اضغط Enter للخروج...")
