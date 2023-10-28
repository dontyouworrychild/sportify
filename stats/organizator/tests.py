from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Organizator
import os

class OrganizatorViewsetsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # print("Current working directory:", os.getcwd())

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../common/test_images/image.png'))
        image = SimpleUploadedFile(name='image.png', content=open(image_path, 'rb').read(), content_type='image/png')
        cls.organizator = Organizator.objects.create_user(
            username="organizator_user",
            password="password",
            first_name="Test",
            last_name="User",
            phone_number="+77759727595",
            image=image
        )
    def tearDown(self):
        # Delete the image file after the test
        image_path = self.organizator.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
            # Delete the empty image folder if it's left behind
            image_dir = os.path.dirname(image_path)
            if not os.listdir(image_dir):
                os.rmdir(image_dir)
        
    def setUp(self):
        login_url = '/api/v1/auth/login/'
        self.client = APIClient()
        response = self.client.post(login_url, data={"username": "organizator_user", "password": "password"})
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {response.data["access"]}'

    def assert_organizator_data(self, data):
        self.assertEqual(data["username"], "organizator_user")
        self.assertEqual(data["role"], "organizator")
        self.assertEqual(data["phone_number"], "+77759727595")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "User")

        role = data["role"]
        id = data["id"]
        self.assertEqual(data["image"], f"http://testserver/media/{role}/{id}.png")

    def test_list_organizators(self):
        url = '/api/v1/organizators/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assert_organizator_data(response.data[0])

    def test_retrieve_organizator(self):
        url = f'/api/v1/organizators/{self.organizator.id}/' 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_organizator_data(response.data)

    def test_update_organizator(self):
        # Create a new image for the update
        new_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../common/test_images/new_image.png'))
        new_image = SimpleUploadedFile(name='new_image.png', content=open(new_image_path, 'rb').read(), content_type='image/png')

        # Send a PATCH request to update the image
        url = f'/api/v1/organizators/{self.organizator.id}/'
        data = {"image": new_image}
        response = self.client.patch(url, data, format='multipart')

        # Check the response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Image updated successfully")
        self.assertTrue(self.organizator.image)