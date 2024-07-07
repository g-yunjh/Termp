from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_deck, name='select_deck'),
    path('main/', views.main, name='main'),
    path('show_current_word/', views.show_current_word, name='show_current_word'),
    path('show_answer/', views.show_answer, name='show_answer'),
    path('move_word/', views.move_word, name='move_word'),
    path('next_round/', views.next_round, name='next_round'),
    path('end_of_study/', views.end_of_study, name='end_of_study'),
    path('summary/', views.summary, name='summary')
]
