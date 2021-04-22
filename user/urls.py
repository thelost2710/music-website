from django.contrib import admin
from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login', views.login),
    path('CheckLogin', views.CheckLogin),
    path('', views.index),
    path('logout', views.logout_view),
    path('ViewAlbum', views.ViewAlbum),
    path('YourAlbum', views.YourAlbum),
    path('ViewHotAlbum', views.ViewHotAlbum),
    path('NewAlbum', views.NewAlbum),
    path('ViewCart', views.ViewCart),
    path('ViewMusic', views.ViewMusic),
    path('MusicChart', views.MusicChart),
    path('viewMusicInAlbum/<int:id>/', views.viewMusicInAlbum),
    path('LikeMusic/<int:id>/', views.LikeMusic),
    path('LikeAlbum/<int:id>/', views.LikeAlbum),
    path('addCart/<int:id>/', views.addCart),
    path('deleteCart/<int:id>/', views.deleteCart),
    path('createAlbumInterface', views.createAlbumInterface),
    path('createAlbum', views.createAlbum),
    path('deleteYourAlbum/<int:id>/', views.deleteYourAlbum),
    path('addMusic/<int:idMusic>/<int:idAlbum>/', views.addMusic),
    path('deleteMusic/<int:idMusic>/<int:idAlbum>/', views.deleteMusic),
    path('bill/<int:totalPrice>/', views.bill),
    path('saveBill', views.saveBill),
    path('Contact', views.Contact),
    path('MusicPurchaseHistory', views.MusicPurchaseHistory),
    path('signUpInterface', views.signUpInterface),
    path('signUp', views.signUp),
    path('ChangePasswordInterface', views.ChangePasswordInterface),
    path('ChangePassword', views.ChangePassword),
    path('ViewProfile', views.ViewProfile),
    path('saveInformation', views.saveInformation),
    path('search', views.search),
    path('signUpPage', views.signUpPage),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)