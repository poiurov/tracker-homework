from django.shortcuts import render, redirect, get_object_or_404 #Частые операции с html
from django.http import Http404
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
            "level": skill.level,
            "done_count": done_count,
            "total_count": total_count,
            "slug": skill.slug,
        })

    return render(request, "tracker/home.html", {
        "skills": skills_with_stats,
    })


def skill_detail(request, skill_slug:str):
    skill = get_object_or_404(Skill, slug=skill_slug)

    done_goals = []
    undone_goals = []
    archive_goals = []

    for goal in skill.goals.all():
        if goal.archived:
            archive_goals.append(goal)
        elif goal.done:
            done_goals.append(goal)
        else:
            undone_goals.append(goal)


    return render(request, "tracker/skill_detail.html", {
        "skill": skill,
        "skill_slug": skill_slug,
        "done_goals": done_goals,
        "not_done_goals": undone_goals,
        "archive_goals": archive_goals,
    })


def skill_edit(request, skill_slug:str):
    skill = get_object_or_404(Skill, slug=skill_slug)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            skill.name = name
            skill.save()

        return redirect("skill_detail", skill_slug=skill_slug)

    return redirect("skill_detail", skill_slug=skill_slug)


def goal_detail(request, skill_slug:str, goal_id,):

    skill = get_object_or_404(Skill, slug=skill_slug)
    goal = get_object_or_404(Goal, id=goal_id, skill=skill)

    return render(request, "tracker/show_undone_goals.html", {
        "goal": goal,
        "skill": skill,
    })

def goals_check(request, skill_slug:str):
    skill = get_object_or_404(Skill, slug=skill_slug)

    done_goals = []
    not_done_goals = []

    for goal in skill.goals.all():
        goal_data = {
            "id": goal.id,
            "text": goal.text,
            "skill_slug": skill_slug,
            "skill_name": skill.name,
            "skill_description": skill.description,
        }

        if goal.done:
            done_goals.append(goal_data)
        else:
            not_done_goals.append(goal_data)

    return render(request, "tracker/goals_check.html", {
        "skill": skill,
        "done_goals": done_goals,
        "not_done_goals": not_done_goals,
    })

def mark_goal_done(request, skill_slug:str, goal_id):
    skill = get_object_or_404(Skill, slug=skill_slug)
    goal = get_object_or_404(Goal, id=goal_id, skill=skill)

    goal.done = True
    goal.save()

    return redirect("show_undone_goals")

def mark_goal_undone(request, skill_slug:str, goal_id):
    skill = get_object_or_404(Skill, slug=skill_slug)
    goal = get_object_or_404(Goal, id=goal_id, skill=skill)

    goal.done = False
    goal.save()

    return redirect("goals_check", skill_slug=skill_slug)

def mark_goal_archived(request, skill_slug:str, goal_id):
    skill = get_object_or_404(Skill, slug=skill_slug)
    goal = get_object_or_404(Goal, id=goal_id, skill=skill)

    if request.method == "POST":
        goal.archived = True
        goal.save()

    return redirect("skill_detail", skill_slug=skill_slug)

def show_undone_goals(request):
    goals = Goal.objects.filter(done=False).select_related("skill")

    return render(request, "tracker/show_undone_goals.html", {
        "goals": goals,
    })


def goal_delete(request, skill_slug:str, goal_id):
    skill = get_object_or_404(Skill, slug=skill_slug)
    goal = get_object_or_404(Goal, id=goal_id, skill=skill)

    if request.method == "POST":
        goal.delete()

    return redirect("goals_check", skill_slug=skill_slug)

def goals_create(request, skill_slug:str):
    skill = get_object_or_404(Skill, slug=skill_slug)

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

            return redirect("skill_detail", skill_slug=skill_slug)

        else:
            return render(
                request,
                "tracker/goal_create.html",
                {
                    "skill": skill,
                    "skill_id": skill.id,
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