from django.urls import path
from inventorymgmt import views

urlpatterns = [
    path('', views.home, name="home"),
    path('list_items/', views.list_items, name="list_items"),
    path('add_items/', views.add_items, name="add_items"),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('stock_details/<str:pk>/', views.stock_details, name="stock_details"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('list_history/', views.list_history, name="list_history"),
    path('history/delete/<int:pk>/',views.delete_history,name= 'delete_history'),

]

    