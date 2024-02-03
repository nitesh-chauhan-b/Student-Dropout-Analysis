from django.contrib import admin
from django.urls import path, include
from home import views
from .views import school_signup
from .views import government_signup
from .views import delete_student_data
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('',views.index, name="home"),
    path('school_index',views.school_index, name="school_index"),
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('gov_index',views.gov_index, name="gov_index"),
    path('logingov',views.loginUsergov, name="logingov"),
    path('logoutgov',views.logoutUsergov,name="logoutgov"),
    path('school-signup/', school_signup, name='school_signup'),
    path('government-signup/', government_signup, name='government_signup'),
    path('saveenquiry',views.saveEnquiry,name='saveenquiry'),
    path('delete-student/<int:pk>/', delete_student_data, name='delete_student_data'),
    path('district_index',views.district_index, name="district_index"),
    path('logindis',views.loginUserdis, name="logindis"),
    path('logoutdis',views.logoutUserdis,name="logoutdis"),
    path('district_signup/', views.district_signup, name='district_signup'),
    path('suggestion',views.suggestion,name='suggestion'),
    path('Suggestion_G_to_S',views.Suggestion_G_to_S,name='Suggestion_G_to_S'),
    path('getback',views.index, name="getback"),
    path('suggestionDist',views.suggestionDist,name='suggestionDist'),
    path('predict_dropout',views.predict_dropout,name='predict_dropout'),
    path('approve_school/<int:school_id>/', views.approve_school, name='approve_school'),
    path('approve_district/<int:distrct_id>/', views.approve_district, name='approve_district'),
    path('district_index_filtered/', views.district_index_filtered, name='district_index_filtered'),
    path('gov_index_filtered/', views.gov_index_filtered, name='gov_index_filtered'),
    path('SchoolYearDataStore',views.SchoolYearDataStore,name='SchoolYearDataStore'),
    path('predict_batch_dropout', views.predict_batch_dropout, name='predict_batch_dropout'),
    path('delete_suggesstion_from_district_to_school/<int:pk>/', views.delete_suggesstion_from_district_to_school, name='delete_suggesstion_from_district_to_school'),
    path('delete_suggesstion_from_government_to_district/<int:pk>/', views.delete_suggesstion_from_government_to_district, name='delete_suggesstion_from_government_to_district'),
    path('delete_suggesstion_from_state_to_school/<int:pk>/', views.delete_suggesstion_from_state_to_school, name='delete_suggesstion_from_state_to_school'),





]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)