from django.test import TestCase
from django.urls import reverse
from .models import Skill, Goal

class SkillTestCase(TestCase):
    def test_skill_name(self):
        skill = Skill.objects.create(name="Test Skill")
        self.assertEqual(skill.name, "Test Skill")

class ShowUndoneGoalsTestCase(TestCase):
    def test_show_undone_goals_page_displays_only_undone_goals(self):
        skill = Skill.objects.create(name="English")

        Goal.objects.create(
            skill=skill,
            text="Undone goal",
            done=False
        )

        Goal.objects.create(
            skill=skill,
            text="Done goal",
            done=True
        )

        response = self.client.get(reverse("show_undone_goals"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Undone goal")
        self.assertNotContains(response, "Done goal")

from django.test import TestCase
from django.urls import reverse
from .models import Skill, Goal


class UrlsTestCase(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="English",
            slug="english"
        )

        self.goal = Goal.objects.create(
            skill=self.skill,
            text="Test goal",
            done=False
        )

    def test_home_url_opens(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_skill_detail_url_opens(self):
        response = self.client.get(
            reverse("skill_detail", kwargs={"skill_slug": self.skill.slug})
        )

        self.assertEqual(response.status_code, 200)

    def test_goal_detail_url_opens(self):
        response = self.client.get(
            reverse(
                "goal_detail",
                kwargs={
                    "skill_slug": self.skill.slug,
                    "goal_id": self.goal.id
                }
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_goal_create_url_opens(self):
        response = self.client.get(
            reverse("goal_create", kwargs={"skill_slug": self.skill.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_skill_edit_url_opens(self):
        response = self.client.get(
            reverse("skill_edit", kwargs={"skill_slug": self.skill.slug})        )
        self.assertEqual(response.status_code, 200)

    def test_show_undone_goals_url_opens(self):
        response = self.client.get(reverse("show_undone_goals"))
        self.assertEqual(response.status_code, 200)

    def test_goals_check_url_opens(self):
        response = self.client.get(
            reverse("goals_check", kwargs={"skill_slug": self.skill.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_goal_delete_url_opens(self):
        response = self.client.get(
            reverse(
                "goal_delete",
                kwargs={
                    "skill_slug": self.skill.slug,
                    "goal_id": self.goal.id
                }
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_goal_done_url_opens(self):
        response = self.client.get(
            reverse(
                "goal_done",
                kwargs={
                    "skill_slug": self.skill.slug,
                    "goal_id": self.goal.id
                }
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_goal_undone_url_opens(self):
        response = self.client.get(
            reverse(
                "goal_undone",
                kwargs={
                    "skill_slug": self.skill.slug,
                    "goal_id": self.goal.id
                }
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_mark_goal_archived_url_opens(self):
        response = self.client.get(
            reverse(
                "mark_goal_archived",
                kwargs={
                    "skill_slug": self.skill.slug,
                    "goal_id": self.goal.id
                }
            )
        )
        self.assertEqual(response.status_code, 302)