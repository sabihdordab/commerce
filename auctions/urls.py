from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create_listing , name = "create"),
    path("<int:id>",views.listing_page , name = "listing_page"),
    path('comment/<int:id>',views.add_comment , name = "add_comment"),
    path('add_watch_list/<int:id>',views.add_watch_list,name='add_watch_list'),
    path('remove_watch_list/<int:id>',views.remove_watch_list,name='remove_watch_list'),
    path('watch_list',views.watch_list,name='watch_list'),
    path('categories',views.categories,name = 'categories'),
    path('category/<str:category_name>',views.category , name = 'category'),
    path('add_bid/<int:id>',views.add_bid , name = 'add_bid'),
    path('close_listing/<int:id>',views.close_listing,name = 'close_listing')
]