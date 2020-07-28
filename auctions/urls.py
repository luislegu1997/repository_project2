from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.create_listing, name="create_listing"),
    path('item-<str:item>', views.item_page, name="item_page"),
    path('addtoWatchlist-<str:item>', views.WatchlistAdd, name="WatchlistAdd"),
    path('removeFromWatchlist-<str:item>', views.RemoveWatchlist, name="RemoveWatchlist"),
    path('bid-<str:item>', views.Bid_money, name="Bid"),
    path('delete-<str:item>', views.Delete_item, name="delete_item"),
    path('close-<str:item>', views.Close, name="close"),
    path('add_comment-<str:item>', views.Comment_add, name="add_comment"),
    path('Watchlist', views.Watchlist_display, name="watchlist"),
    path('Categories', views.Categories, name ="Categories"),
    path('Category-<str:category>', views.Category_selected, name ="Category")
]
