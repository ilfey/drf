from django.test import TestCase

from django.contrib.auth.models import User
from .models import Snippet


# Create your tests here.
class SnippetTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="john", email="8f2p6@example.com", password="glass onion"
        )

        self.test_snippet = Snippet.objects.create(
            owner=self.test_user,
        )

    def test_create(self):
        Snippet(
            owner=self.test_user,
        ).save()

        self.assertTrue(Snippet.objects.filter(owner=self.test_user).count() > 0)

    def test_delete(self):
        self.assertTrue(Snippet.objects.filter(owner=self.test_user).count() > 0)

        self.test_snippet.delete()

        self.assertFalse(Snippet.objects.filter(owner=self.test_user).exists())

    def test_update(self):
        self.test_snippet.title = "new title"
        self.test_snippet.save()

        self.assertEqual(Snippet.objects.get(pk=self.test_snippet.pk).title, "new title")


class ViewSetTestCase(TestCase):
    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(
            username="john", email="8f2p6@example.com", password="glass onion"
        )

        for i in range(5):
            Snippet.objects.create(
                title=f"title {i}",
                owner=test_user,
            )

    def test_list(self):
        response = self.client.get("/api/snippets/")

        self.assertTrue(response.data['count'] > 4)

    def test_detail(self):
        response = self.client.get("/api/snippets/1/")

        self.assertEqual(response.data['id'], 1)

    def test_create(self):
        response = self.client.post("/api/snippets/", {
            "title": "title",
        })

        self.assertEqual(response.status_code, 403)

    def test_update(self):
        response = self.client.put("/api/snippets/1/", {
            "title": "title",
        })

        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        response = self.client.delete("/api/snippets/1/")

        self.assertEqual(response.status_code, 403)
