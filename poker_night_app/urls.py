from django.urls import path
from . import views


urlpatterns = [
    path('home',views.home),
    path('<int:user_id>/host', views.host),
    path('<int:user_id>/host/tournament', views.host_tournament),
    path('<int:user_id>/host/cash_game', views.host_cash_game),
    path('<int:user_id>/host/<str:game_type>/create', views.event_create),
    path('<int:event_id>/<str:game_type>/view', views.view),
    path('<int:event_id>/cash_game/edit', views.edit_cash_game),
    path('<int:event_id>/tournament/edit', views.edit_tournament),
    path('<int:event_id>/<str:game_type>/update', views.event_update),
    path('<int:event_id>/cancel', views.event_cancel),
    path('<int:event_id>/<str:game_type>/register', views.game_register),
    path('<int:event_id>/unregister', views.game_unregister),
    path('<int:user_id>/my_events', views.my_events),
    path('<int:event_id>/comment', views.comment),
    path('<int:event_id>/reply', views.reply),
    
]