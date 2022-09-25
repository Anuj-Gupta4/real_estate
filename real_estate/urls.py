from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from listings.views import (
    index,
    CustomLoginView,
    RegisterPage,
    LogoutView,
    predict,
    listing_list, 
    listing_retrieve, 
    listing_create, 
    listing_update, 
    listing_delete,
    listing_search,
    user_specific_listings
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('predict', predict, name='predict'),
    path('listings/', listing_list, name='listing_list'),
    path('listings/<pk>/', listing_retrieve, name='listing_retrieve'),
    path('user_specific_listings/', user_specific_listings, name='user_specific_listings'),
    path('add-listing', listing_create.as_view(), name='listing_create'),
    path('listings/<pk>/edit/', listing_update, name='listing_update'),
    path('listings/<pk>/delete/', listing_delete, name='listing_delete'),
    path('listing_search', listing_search, name='listing_search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)