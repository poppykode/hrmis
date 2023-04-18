from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('all',views.boards, name='boards'),
    path('add-board',views.add_board, name='add_board'),
    path('board-update/<int:pk>',views.board_update, name='board_update'),
    path('board-delete/<int:pk>',views.board_delete, name='board_delete'),
    path('board-details/<int:pk>',views.board_details, name='board_details'),

]
