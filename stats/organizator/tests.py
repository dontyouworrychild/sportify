from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Organizator

class OrganizatorViewsetsTest(APITestCase):
    def setUp(self):
        self.organizator = Organizator.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            image="test.jpg",
        )

    def test_list_organizators(self):
        url = '/organizators/'  # URL for listing organizators
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "testuser")

    def test_retrieve_organizator(self):
        url = f'/organizators/{self.organizator.id}/'  # URL for retrieving a specific organizator
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_organizator(self):
        url = f'/organizator/{self.organizator.id}/'  # URL for updating an existing organizator
        image_file = SimpleUploadedFile("updated.jpg", b"updated_content", content_type="image/jpeg")
        data = {
            "image": image_file,
        }
        response = self.client.patch(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organizator.refresh_from_db()
        self.assertTrue(self.organizator.image)