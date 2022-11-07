from django.urls import path
from . import views

urlpatterns = [
    #URL syntax: ('pattern to watch for', file.methodName, name="shortcut name")
    path('admin', views.admin_console, name="admin"),
    path('', views.GH_index, name='GameHoard'),
    path('<str:pk>/UpdateGame/', views.update, name='UpdateGame'),
    path('bs/', views.beautifulsoup, name='BeautifulSoup'),
    path('api/', views.api_template, name='API'),
    path('WishList', views.create_wishlist, name='WishList'),
    path('DeleteWish', views.delete_wishlist, name='DeleteWish'),
]