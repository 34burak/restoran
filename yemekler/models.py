from django.db import models




class Yemek(models.Model):
    KATEGORI_CHOICES = (
        ('corba', 'Çorbalar'),
        ('ana_yemek', 'Ana Yemekler'),
        ('tatli', 'Tatlılar'),
    )
    isim = models.CharField(max_length=255)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    icerik = models.TextField()
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)


    def __str__(self):
        return self.isim




class Sepet(models.Model):
    yemek = models.ForeignKey(Yemek, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField()
    tutar = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.yemek.isim} - Adet: {self.adet} - Tutar:{self.tutar}"
   
class Siparis(models.Model):
    telefon = models.CharField(max_length=15)
    adres = models.CharField(max_length=255)
    notlar = models.TextField()
    urun = models.TextField()  # Güncellenen alan
    toplam_tutar = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Sipariş - Telefon: {self.telefon}, Adres: {self.adres}"






class SiparisUrun(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE)
    yemek = models.ForeignKey(Yemek, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField()


    def __str__(self):
        return f"Sipariş ID: {self.siparis_id} - Yemek: {self.yemek.isim}, Adet: {self.adet}"