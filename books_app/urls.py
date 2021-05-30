from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage),
    path('/add_book',views.add_book),
    path('/add_fav/<int:book_id>',views.add_fav),
    path("/<int:book_id>",views.view_book),
    path("/delete_book/<int:book_id>",views.delete_book),
    path("/update_book/<int:book_id>",views.update_book),
    path("/unfavorite_book/<int:book_id>",views.remove_book),
    path("/add_fav_view/<int:book_id>",views.add_fav_views)
]