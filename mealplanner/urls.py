"""
URL configuration for mealplanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    path('category/',views.category,name='category'),
    path('recipe_list/',views.recipe_list,name='recipe_list'),
    path('recipe_list/category/<int:category_id>/', views.recipe_list, name='recipe_list_by_id'), # for meal plan button
    path('recipe_list/filter/<str:category>/', views.recipe_list, name='recipe_list_by_name'),  # for filter buttons
    path('recipe/<int:id>/',views.recipe_detail,name='recipe_detail'),
    path('recipe/add/',views.add_recipe,name='add_recipe'),
    path('addtomealplan/<int:recipe_id>/',views.add_to_mealplan,name='add_to_mealplan'),
    path('meal_plan/',views.meal_plan,name='meal_plan'),
    path('meal_plan/remove/<int:recipe_id>/',views.remove_from_mealplan,name='remove_from_mealplan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
