from django.urls import path

from . import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('check_user_is_admin/', views.check_user_is_admin, name='check_user_is_admin'),
    path('get_admin_panel_data/', views.get_admin_panel_data, name='get_admin_panel_data'),
    path('get_user_profile/<int:profile_id>/', views.get_user_profile, name='get_user_profile'),
    path('user_block_management/<int:user>/', views.user_block_management, name='user_block_management'),
    path('edit-premium-plans/', views.edit_premium_plans, name='edit_premium_plans'),
    path('get_premium_plan_details/', views.get_premium_plan_details, name='get_premium_plan_details'),

]