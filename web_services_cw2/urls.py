from django.contrib import admin
from django.urls import path
from local_guide import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/attractions", views.get_attractions, name="get_attractions"),
    path("api/tours", views.get_tours, name="get_tour"),
    path("api/categories", views.get_categories, name="get_categories"),
    path("api/discounts", views.get_discounts, name="get_discounts"),
    path("api/countries", views.get_countries, name="get_countries"),
    path("api/book", views.book, name="book"),
    path("api/make_tour", views.make_tour, name="make_tour"),
]
