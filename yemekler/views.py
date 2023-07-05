import json
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Yemek, Sepet, Siparis, SiparisUrun

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def anasayfa(request):
    yemekler = Yemek.objects.all()

    # Yemekleri kategorilere göre gruplandırma
    yemekler_gruplu = {}
    for kategori in Yemek.KATEGORI_CHOICES:
        yemekler_gruplu[kategori[0]] = []

    for yemek in yemekler:
        yemekler_gruplu[yemek.kategori].append(yemek)

    context = {
        'yemekler_gruplu': yemekler_gruplu,
    }

    return render(request, 'anasayfa.html', context)

def sepete_ekle(request, yemek_id):
    if request.method == 'POST':
        yemek = Yemek.objects.get(id=yemek_id)
        adet = int(request.POST.get('adet'))
        fiyat = yemek.fiyat
        tutar = adet * fiyat

        # Sepeti session üzerinde kontrol etme
        sepet = request.session.get('sepet', [])
        urun = {
            'yemek_id': yemek.id,
            'adet': adet,
            'fiyat': float(fiyat),
            'tutar': float(tutar),
        }
        sepet.append(urun)
        request.session['sepet'] = sepet

    return redirect('anasayfa')

def sepeti_goster(request):
    sepet = request.session.get('sepet', [])
    sepet_urunler = []
    toplam_tutar = 0

    # Sepet ürünlerini ve toplam tutarı hesaplama
    for urun in sepet:
        yemek = Yemek.objects.get(id=urun['yemek_id'])
        urun['isim'] = yemek.isim
        urun['toplam_tutar'] = urun['adet'] * urun['fiyat']
        sepet_urunler.append(urun)
        toplam_tutar += urun['toplam_tutar']

    context = {
        'sepet_urunler': sepet_urunler,
        'toplam_tutar': toplam_tutar,
    }

    return render(request, 'sepet.html', context)

def urun_sil(request, urun_id):
    sepet = request.session.get('sepet', [])

    for index, urun in enumerate(sepet):
        if urun['yemek_id'] == int(urun_id):
            sepet.pop(index)
            break

    request.session['sepet'] = sepet
    return redirect('sepeti_goster')

def siparis_ver(request):
    if request.method == 'POST':
        telefon = request.POST.get('telefon')
        adres = request.POST.get('adres')
        notlar = request.POST.get('notlar')

        # Sepetteki ürünleri string dizisi olarak al
        sepet_urunler = request.session.get('sepet', [])
        sepet_urunler_string = []

        for urun in sepet_urunler:
            yemek = Yemek.objects.get(id=urun['yemek_id'])
            urun_str = f"\n- {yemek.isim} - Adet:{urun['adet']} - Tutar:{urun['tutar']}"
            sepet_urunler_string.append(urun_str)

        # Toplam tutarı hesapla
        toplam_tutar = sum(urun['tutar'] for urun in sepet_urunler)

        # Siparişi oluşturma ve kaydetme
        siparis = Siparis(telefon=telefon, adres=adres, notlar=notlar, urun=', '.join(sepet_urunler_string), toplam_tutar=toplam_tutar)
        siparis.save()

        # Sepeti temizleme işlemi
        request.session['sepet'] = []

        return redirect('anasayfa')

    return HttpResponse(status=405)
