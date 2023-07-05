from django.urls import path
from yemekler.views import anasayfa, sepete_ekle, sepeti_goster,siparis_ver,urun_sil
from django.contrib import admin

urlpatterns = [
    path('', anasayfa, name='anasayfa'),
    path('sepete-ekle/<int:yemek_id>/', sepete_ekle, name='sepete_ekle'),
    path('sepeti-goster/', sepeti_goster, name='sepeti_goster'),
    path('admin/', admin.site.urls),
    path('siparis-ver/', siparis_ver, name='siparis_ver'),
    path('sil/<int:urun_id>/', urun_sil, name='sil'),
]
