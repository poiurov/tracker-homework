"""
URL configuration for RPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from tracker.views import home, skill_detail, goals_check, mark_goal_done, mark_goal_undone, goals_create, goal_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("skill/<int:skill_id>/", skill_detail, name="skill_detail",),
    path("skill/<int:skill_id>/goal/<int:goal_id>/", goal_detail, name="goal_detail",),
    path("goals_view/", goals_check, name="goals"),
    path("skill/<int:skill_id>/goals_new/", goals_create, name="goal_create",),
    path("goal/<int:skill_id>/<int:goal_id>/done/", mark_goal_done, name="goal_done",),
    path("goal/<int:skill_id>/<int:goal_id>/undone/", mark_goal_undone, name="goal_undone",),
]

#name = это ссылка для backend кода, а не ссылка как URL для пользователя
