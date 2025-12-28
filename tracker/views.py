from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    skills_with_stats = {}

    for skill_id, skill in SKILLS.items():
        done_count = sum(1 for goal in skill['goals'] if goal['done'])
        total_count = len(skill['goals'])

        skills_with_stats[skill_id] = {
            **skill,
            'done_count': done_count,
            'total_count': total_count,
        }

    return render(request, "tracker/home.html", {
        "skills": skills_with_stats,
    })

SKILLS = {
 1: {
 'name': 'Python',
 'description': 'Master Python programming',
 'goals': [
 {'id': 1, 'text': 'Изучить основы Python', 'goal_description': 'Прочти книгу', 'done': True},
 {'id': 2, 'text': 'Изучить основы словарей', 'goal_description': 'Посмотри видео урок', 'done': False},
 ]
 },
 2: {
 'name': 'Django',
 'description': 'Master Django framework',
 'goals': [
 {'id': 1, 'text': 'Изучить архитектуру Django', 'goal_description': 'Посмотри видео урок', 'done': True},
 {'id': 2, 'text': 'Изучить модуль views', 'goal_description': 'Посмотри видео урок', 'done': True},
 {'id': 3, 'text': 'Изучить модуль urls', 'goal_description': 'Посмотри видео урок', 'done': False},
 ]
 }
}
