from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404

#render - собери текущую страницу
#reddirect - после выполнения переправь нас в ...

def home(request):
    skills_with_stats = {}

    for skill_id, skill in SKILLS.items():
        done_count = sum(goal["done"] for goal in skill['goals'])
        total_count = len(skill['goals'])

        skills_with_stats[skill_id] = {
            **skill,
            'done_count': done_count,
            'total_count': total_count,
        }

    return render(request, "tracker/home.html", {
        "skills": skills_with_stats,
    })


def skill_detail(request, skill_id):
    skill = SKILLS.get(skill_id)

    if skill is None:
        raise Http404("Skill not found")

    return render(request, "tracker/skill_detail.html", {
        "skill": skill,
    })

def goal_detail(request, skill_id, goal_id):
    skill = SKILLS.get(skill_id)
    goals = skill['goals']
    goal = goals[goal_id]

    if goal is None:
        raise Http404("Goal not found")

    return render(request, "tracker/goal_detail.html", {
        "goal": goal,
        "goals": goals,  # ← ПЕРЕДАЁМ ВСЕ goals
        "goal_description": goal["goal_description"],
    })

def goals_check(request):
    done_goals = []
    not_done_goals = []

    for skill_id, skill in SKILLS.items():
        skill_name = skill["name"]
        skill_description = skill["description"]

        # цикл - пройдись по целям в skill, выполненные помести вверх, невыполненные вниз
        for goal in skill["goals"]:
            goal_data = {
                "id": goal["id"],
                "text": goal["text"],
                "skill_id": skill_id,
                "skill_name": skill_name,
                "skill_description": skill_description
            }

            if goal["done"]:
                done_goals.append(goal_data)
            else:
                not_done_goals.append(goal_data)

    return render(
        request,
        "tracker/goals_view.html",
        {
            "done_goals": done_goals,
            "not_done_goals": not_done_goals,
        }
    )

def mark_goal_done(request, skill_id, goal_id):
    skill = SKILLS.get(skill_id)

    if not skill:
        raise Http404("Skill not found")

    goal_found = False

    for goal in skill["goals"]:
        if goal["id"] == goal_id:
            goal["done"] = True
            goal_found = True
            break

    if not goal_found:
        raise Http404("Goal not found")
    return redirect("goals")

def goals_create(request, skill_id):
    skill = SKILLS.get(skill_id)

    if not skill:
        raise Http404("Skill not found")

    if request.method == "POST":
        text = request.POST.get("text")
        description = request.POST.get("description")

        if text and len(text.strip()) >= 3:
            new_goal = {
                "id": len(skill["goals"]) + 1,
                "text": text,
                "done": False,
                "description": description,
            }

            skill["goals"].append(new_goal)

            return redirect("skill_detail", skill_id=skill_id)

        else:
            # ❗ ОШИБКА ВВОДА → ПОВТОРНЫЙ РЕНДЕР
            return render(
                request,
                "tracker/goal_create.html",
                {
                    "skill": skill,
                    "skill_id": skill_id,
                    "error": "Цель должна содержать минимум 3 символа",
                    "text": text,
                    "description": description,
                }
            )


    return render(
        request,
        "tracker/goal_create.html",
        {
            "skill": skill,
            "skill_id": skill_id,
        }
    )

def mark_goal_undone(request, skill_id, goal_id):
    skill = SKILLS.get(skill_id)

    if not skill:
        raise Http404("Skill not found")

    goal_found = False

    for goal in skill["goals"]:
        if goal["id"] == goal_id:
            goal["done"] = False
            goal_found = True
            break

        if not goal_found:
            raise Http404("Goal not found")
    return redirect("goals")

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
    },
    3: {
        'name': 'Guitar',
        'description': 'Master guitar',
        'goals': [
            {'id': 1, 'text': 'Видео курс', 'goal_description': 'Посмотри видео урок', 'done': False},
            {'id': 2, 'text': 'Мелодии', 'goal_description': 'Сыграть 3 мелодии', 'done': True},
            {'id': 3, 'text': 'Бой', 'goal_description': 'Выучить бой', 'done': False},
        ]
    }
}
