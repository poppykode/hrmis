from django.urls import path
from . import views

app_name = 'app_settings'
urlpatterns = [
    path('all',views.blocked_sites, name='blocked_sites'),
    path('add-site-to-block-list',views.add_site_to_block_list, name='add_site_to_block_list'),
    path('blocked-site-update/<int:pk>',views.blocked_site_update, name='blocked_site_update'),
    path('blocked-site-delete/<int:pk>',views.blocked_site_delete, name='blocked_site_delete'),

]
