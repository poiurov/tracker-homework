"""
URL configuration for RPGproj project.

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
from django.http import HttpResponse
from tracker.views import (
    home,
    skill_detail,
    goals_check,
    mark_goal_done,
    mark_goal_undone,
    goals_create,
    goal_detail,
    skill_edit,
    goal_delete,
    show_undone_goals,
    mark_goal_archived
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("skill/<slug:skill_slug>/", skill_detail, name="skill_detail"),
    path("skill/<slug:skill_slug>/goal/<int:goal_id>/", goal_detail, name="goal_detail"),
    path("skill/<slug:skill_slug>/goals_new/", goals_create, name="goal_create"),
    path("skill/<slug:skill_slug>/edit/", skill_edit, name="skill_edit"),
    path("show_undone_goals/", show_undone_goals, name="show_undone_goals"),
    path("goals/<slug:skill_slug>/", goals_check, name="goals_check"),
    path("goals/<slug:skill_slug>/<int:goal_id>/delete/", goal_delete, name="goal_delete"),
    path("goal/<slug:skill_slug>/<int:goal_id>/done/", mark_goal_done, name="goal_done"),
    path("goal/<slug:skill_slug>/<int:goal_id>/undone/", mark_goal_undone, name="goal_undone"),
    path("skill/<slug:skill_slug>/goal/<int:goal_id>/archive/", mark_goal_archived, name="mark_goal_archived"),
]

#name = это ссылка для backend кода, а не ссылка как URL для пользователя
