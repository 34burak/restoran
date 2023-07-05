import tkinter as tk
import sqlite3

# Veritabanı bağlantısı oluşturma
conn = sqlite3.connect('C:\\Users\\burak\\eticaret\\db.sqlite3')
cursor = conn.cursor()

# Masaüstü uygulaması penceresi
window = tk.Tk()
window.title("Sipariş Takip")
window.geometry("800x450")  # Pencere boyutu

# Metin stilini tanımlama
text_style = ("Arial", 20, "bold")

# Metin alanı
text_box = tk.Text(window, height=60, width=80, font=text_style)  # Metin alanı stilini ayarlama
text_box.pack()

def update_orders_text():
    # Veritabanından son eklenen siparişleri çekme
    cursor.execute("SELECT urun, telefon, adres, notlar, toplam_tutar FROM yemekler_siparis ORDER BY ROWID DESC LIMIT 10")
    siparisler = cursor.fetchall()

    # Metin alanını güncelleme
    text_box.delete(1.0, tk.END)
    text_box.tag_configure("bold", font=text_style)  # Kalın metin stilini ayarlama
     # Kalın metin stilini kullanarak başlık ekleme
    for siparis in siparisler:
        urun = siparis[0]
        telefon = siparis[1]
        adres = siparis[2]
        notlar = siparis[3]
        toplam_tutar = siparis[4]
        text_box.insert(tk.END, "Ürün:  ", "bold") 
        text_box.insert(tk.END, f"{urun}\n")
        text_box.insert(tk.END, "Toplam Tutar: ", "bold")
        text_box.insert(tk.END, f"{toplam_tutar}\n")
        text_box.insert(tk.END, "Telefon:  ", "bold")
        text_box.insert(tk.END, f"{telefon}\n")
        text_box.insert(tk.END, "Adres:  ", "bold")
        text_box.insert(tk.END, f"{adres}\n")
        text_box.insert(tk.END, "Notlar:  ", "bold")
        text_box.insert(tk.END, f"{notlar}\n") 
        text_box.insert(tk.END, "---------------------------------------------------------------------\n")

# Otomatik güncelleme işlevi
def auto_update():
    update_orders_text()
    window.after(5000, auto_update)  # Her 5 saniyede bir güncelleme

# İlk güncelleme
update_orders_text()

# Otomatik güncelleme işlemini başlatma
auto_update()

# Pencereyi çalıştırma
window.mainloop()
