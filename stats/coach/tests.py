from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Coach
from club.models import Club
import os

class CoachViewsetsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../common/test_images/image.png'))
        image = SimpleUploadedFile(name='image.png', content=open(image_path, 'rb').read(), content_type='image/png')
        cls.club = Club.objects.create(
            name = "Khamza",
            location = "Atyrau"
        )

        cls.coach = Coach.objects.create_user(
            username="carter",
            password="password",
            first_name="Test",
            last_name="Coach",
            image=image,
            club=cls.club,
            location="Almaty",
            phone_number="+77013552239",
        )

    def setUp(self):
        login_url = '/api/v1/auth/login/'
        self.client = APIClient()
        response = self.client.post(login_url, data={"username": "carter", "password": "password"})
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {response.data["access"]}'

    def tearDown(self):
        image_path = self.coach.image.path
        if os.path.exists(image_path):
            os.remove(image_path)

    def assert_coach_data(self, data):
        self.assertEqual(data["username"], "carter")
        self.assertEqual(data["role"], "coach")
        self.assertEqual(data["phone_number"], "+77013552239")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "Coach")
        self.assertEqual(data["location"], "Almaty")

        role = data["role"]
        id = data["id"]
        self.assertEqual(data["image"], f"http://testserver/media/{role}/{id}.png")

    def test_list_coaches(self):
        url = '/api/v1/coaches/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assert_coach_data(response.data[0])

    def test_retrieve_coach(self):
        url = f'/api/v1/coaches/{self.coach.id}/' 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_coach_data(response.data)

    def test_partial_update_coach(self):
        # Create a new image for the update
        new_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../common/test_images/new_image.png'))
        new_image = SimpleUploadedFile(name='image.png', content=open(new_image_path, 'rb').read(), content_type='image/png')

        url = f'/api/v1/coaches/{self.coach.id}/'
        data = {"image": new_image}
        response = self.client.patch(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Image updated successfully")

    def test_students_action(self):
        url = f'/api/v1/coaches/{self.coach.id}/students/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)