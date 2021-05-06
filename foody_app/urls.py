from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.show_all),
    path('dashboard/new', views.new),
    path('dashboard/create', views.create_restaurant),
    path("dashboard/<int:id>", views.one_restaurant),
    path('dashboard/search', views.search),
    path('dashboard/profile/<int:id>', views.my_profile),
    path('dashboard/profile/<int:id>/upload', views.image_upload_view),
    path('dashboard/user/<int:id>', views.user_profile),
    path("dashboard/<int:id>/delete", views.delete),
    path("join/<int:id>", views.join),
    path("leave/<int:id>", views.leave),
    path("follow/<int:id>", views.follow),
    path("unfollow/<int:id>", views.unfollow),
    path("logout", views.logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
