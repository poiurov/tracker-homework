from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Skill, Goal

#render - собери текущую страницу
#reddirect - после выполнения переправь нас в ...

def home(request):
    skills = Skill.objects.all()
    skills_with_stats = []

    for skill in skills:
        goals = skill.goals.all()
        done_count = goals.filter(done=True).count()
        total_count = goals.count()

        skills_with_stats.append({
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "rank": skill.rank,
            "done_count": done_count,
            "total_count": total_count,
        })

    return render(request, "tracker/home.html", {
        "skills": skills_with_stats,
    })

def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    return render(request, "tracker/skill_detail.html", {
        "skill": skill,
        "skill_id": skill_id,
    })

def goal_detail(request, skill_id, goal_id):
    skill = SKILLS.get(skill_id)
    goals = skill['goals']
    goal = goals[goal_id-1]

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
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        description = request.POST.get("description", "").strip()

        if text and len(text) >= 3:
            goal = Goal(
                text=text,
                description=description,
                skill=skill,
                done=False,
            )

            if request.user.is_authenticated:
                goal.user = request.user

            goal.save()

            return redirect("skill_detail", skill_id=skill_id)

        else:
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