import requests
import os
import json
import random

from scripts_data import clubs, coaches, organizators, regions, federations, competitions, students, CATEGORIES

url = "http://77.243.80.52:8000"
auth_url = f"{url}/api/v1/auth/login/"
club_url = f"{url}/api/v1/clubs/"
coach_url = f"{url}/api/v1/coaches/"
organizator_url = f"{url}/api/v1/organizators/"
federation_url = f"{url}/api/v1/federations/"
competition_url = f"{url}/api/v1/competitions/"
region_url = f"{url}/api/v1/regions/"
student_url = f"{url}/api/v1/students/"
participant_url = f"{url}/api/v1/participants/"
game_url = f"{url}/api/v1/games/"

def login(username, password):
    credentials = {
        "username": username,
        "password": password
    }
    auth_response = requests.post(auth_url, data=credentials)

    if auth_response.status_code == 200:
        access = auth_response.json().get("access") 
        return access


club_infos = [] # ['id', 'location']
coach_infos = [] # ['id', 'location', 'club_id']
organizator_infos = [] # ['id']
region_infos = [] # ['id']

def upload_club(club_data, headers, directory_path, url):
    # Construct the full path to the image
    image_path = os.path.join(directory_path, club_data['logoUrl'])

    if image_path.lower().endswith('.jpeg') or image_path.lower().endswith('.jpg'):
        mime_type = 'image/jpeg'
    elif image_path.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format for file: {image_path}")
    
    # Open the image in binary mode
    with open(image_path, 'rb') as image_file:
        files = {'logo': (club_data['logoUrl'], image_file, mime_type)}
        # Remove logoUrl from data since it's not needed in the POST data
        data = {
            'name': club_data['name'],
            'location': club_data['location'],
        }
        # POST request to create a club with the image and data
        response = requests.post(url, headers=headers, data=data, files=files)
        return response

def upload_coach(coach_data, club_data, headers, directory_path, url):
    image_path = os.path.join(directory_path, coach_data['image'])
    if image_path.lower().endswith('.jpeg') or image_path.lower().endswith('.jpg'):
        mime_type = 'image/jpeg'
    elif image_path.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format for file: {image_path}")

    with open(image_path, 'rb') as image_file:
        files = {'image': (coach_data['image'], image_file, mime_type)}
        # Remove logoUrl from data since it's not needed in the POST data
        data = {
            'username': coach_data['username'],
            'password': coach_data['password'],
            'phone_number': coach_data['phone_number'],
            'first_name': coach_data['first_name'],
            'last_name': coach_data['last_name'],
            'club': club_data['id'],
            'location': club_data['location']
        }
        print(data)
        # POST request to create a club with the image and data
        response = requests.post(url, headers=headers, data=data, files=files)
        print(response.json())
        return response
    
def upload_organizator(organizator_data, headers, directory_path, url):
    image_path = os.path.join(directory_path, organizator_data['image'])
    if image_path.lower().endswith('.jpeg') or image_path.lower().endswith('.jpg'):
        mime_type = 'image/jpeg'
    elif image_path.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format for file: {image_path}")
    
    with open(image_path, 'rb') as image_file:
        files = {'image': (organizator_data['image'], image_file, mime_type)}
        # Remove logoUrl from data since it's not needed in the POST data
        data = {
            'username': organizator_data['username'],
            'password': organizator_data['password'],
            'phone_number': organizator_data['phone_number'],
            'first_name': organizator_data['first_name'],
            'last_name': organizator_data['last_name'],
        }
        # POST request to create a club with the image and data
        response = requests.post(url, headers=headers, data=data, files=files)
        return response

def upload_region(region_data, headers, directory_path, url):
    image_path = os.path.join(directory_path, region_data['image'])
    if image_path.lower().endswith('.jpeg') or image_path.lower().endswith('.jpg'):
        mime_type = 'image/jpeg'
    elif image_path.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format for file: {image_path}")
    
    with open(image_path, 'rb') as image_file:
        files = {'image': (region_data['image'], image_file, mime_type)}
        # Remove logoUrl from data since it's not needed in the POST data
        data = {
            'slug': region_data['slug'],
            'region': region_data['region']
        }
        # POST request to create a club with the image and data
        response = requests.post(url, headers=headers, data=data, files=files)
        return response

def upload_federation(federation_data, headers, url):
    data = {
        'name': federation_data['name']
    }
    response = requests.post(url, headers=headers, data=data)

# response = upload_competition(competition, headers, competition_url, federations, organizators, federation_index, organizator_index)

def upload_competition(competition_data, headers, url, federations, organizators, federation_index, organizator_index):
    data = {
        'name': competition_data['name'],
        'start_date': competition_data['start_date'],
        'end_date': competition_data['end_date'],
        'location': competition_data['location'],
        'competition_type': competition_data['competition_type'],
        'address': competition_data['address'],
        'federation': federations[federation_index]['id'],
        'organizator': organizators[organizator_index]['id']
    }
    if data['competition_type'] == 'regional':
        region_response = requests.get(region_url, headers)
        regions = []
        if region_response.status_code == 200:
            regions = region_response.json()['data']

        random_index = random.randint(0, len(regions) - 1)
        data['region'] = regions[random_index]['id']

    response = requests.post(url, headers=headers, data=data)

def upload_student(coach_data, student_data, url, directory_path):
    access = login(coach_data['username'], "password") # po idee, president bolu kerek myna zherde
    headers = {
        "Authorization": f"Bearer {access}",
    }
    image_path = os.path.join(directory_path, student_data['image'])
    if image_path.lower().endswith('.jpeg') or image_path.lower().endswith('.jpg'):
        mime_type = 'image/jpeg'
    elif image_path.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format for file: {image_path}")

    with open(image_path, 'rb') as image_file:
        files = {'image': (student_data['image'], image_file, mime_type)}
        data = {
            'first_name': student_data['first_name'],
            'last_name': student_data['last_name'],
            'date_of_birth': student_data['date_of_birth'],
            'coach': coach_data['id'],
            'club': coach_data['club']['id'],
            'location': coach_data['club']['location']
        }
        response = requests.post(url, headers=headers, data=data, files=files)
        return response

def upload_participant(participant_data, competition_id, student_id, coach_id, competition_url):
    retrieve_coach_url = f"{coach_url}{coach_id}" # /coaches/{coach_id}
    coach = requests.get(retrieve_coach_url).json()
    access = login(coach['username'], "password")
    headers = {
        "Authorization": f"Bearer {access}",
    }

    url = f"{competition_url}{competition_id}/register_student/"

    data = {
        'competition': competition_id,
        'student': student_id,
        'age_category': participant_data['age_category'],
        'weight_category': participant_data['weight_category'],
    }

    response = requests.post(url, headers=headers, data=data)

def generate_game(competition_data, organizator_data, competition_url):
    retrieve_organizator_url = f"{organizator_url}{organizator_data['id']}"
    organizator = requests.get(retrieve_organizator_url).json()
    access = login(organizator['username'], "password")
    headers = {
        "Authorization": f"Bearer {access}",
    }

    url = f"{competition_url}{competition_data['id']}/generate_tournament_bracket/"
    response = requests.post(url, headers=headers)

def select_current_game_winner(winner_id, game, headers):
    if game is not None and winner_id is not None:
        url = f"{game_url}{game['id']}/select_winner/"
        data = {
            'winner': winner_id
        }
        response = requests.post(url, data=data, headers=headers)

def select_current_game_level_winners(games, headers):
    for game in games:
        red_corner = game['red_corner']
        blue_corner = game['blue_corner']
        winner_id = None
        if red_corner is not None and blue_corner is not None:
            random_index = random.randint(0, 1)
            if random_index == 1:
                winner_id = blue_corner['id']
            else:
                winner_id = red_corner['id']
            # select_current_game_winner(winner_id, game, headers)
        elif red_corner is not None:
            winner_id = red_corner['id']
            # select_current_game_winner(winner_id, game, headers)
        elif blue_corner is not None:
            winner_id = blue_corner['id']
        select_current_game_winner(winner_id, game, headers)
    
def select_current_category_winners(age, weight, competition, competition_url, headers):
    for level in range(3, 0, -1):
        url = f"{competition_url}{competition['id']}/games/?age={age}&weight={weight}&level={level}"
        games = requests.get(url).json().get('data', [])
        if age == "16-17" and weight == "48kg":
            print(f"In weight={weight}, age={age}, level {level}: \n")
            print(f"In competition {competition['name']}: \n")
            for game in games:
                if game is not None:
                    print("game : ", game)
                print("\n")
            print("\n\n\n")
        select_current_game_level_winners(games, headers)

def select_current_competition_winners(competition, organizator_data, competition_url):

    organizator = requests.get(f"{organizator_url}{organizator_data['id']}").json()

    access = login(organizator['username'], "password")
    headers = {
        "Authorization": f"Bearer {access}",
    }

    for age, weight_categories in CATEGORIES.items():
        for weight in weight_categories:
            select_current_category_winners(age, weight, competition, competition_url, headers)
        

def handle_upload_clubs():
    access = login("admin", "password")
    headers = {
        "Authorization": f"Bearer {access}"
    }
    directory_path = 'scripting_images'
    for club in clubs:
        response = upload_club(club, headers, directory_path, club_url)
        club_infos.append([response.json().get('id'), response.json().get('location')])

def handle_upload_coaches():
    access = login("admin", "password")
    headers = {
        "Authorization": f"Bearer {access}"
    }
    directory_path = 'scripting_images'

    used_indexes = []

    for coach in coaches:
        club = None
        club_response = requests.get(club_url)
        if club_response.status_code == 200:
            clubs = club_response.json()
            random_index = 0

            while random.randint(0, len(clubs) - 1) not in used_indexes:
                random_index = random.randint(0, len(clubs) - 1)
                used_indexes.append(random_index)

            club = clubs[random_index]
            response = upload_coach(coach, club, headers, directory_path, coach_url)
    
def handle_upload_organizators():
    access = login("admin", "password")
    headers = {
        "Authorization": f"Bearer {access}"
    }
    directory_path = 'scripting_images'
    for organizator in organizators:
        response = upload_organizator(organizator, headers, directory_path, organizator_url)
        organizator_infos.append(response.json().get('id'))

def handle_upload_regions():
    access = login("admin", "password")
    headers = {
        "Authorization": f"Bearer {access}"
    }
    directory_path = 'scripting_images'
    for region in regions:
        response = upload_region(region, headers, directory_path, region_url)
        region_infos.append(response.json().get('id'))

def handle_upload_federations():
    access = login("admin", "password") # po idee, president bolu kerek myna zherde
    headers = {
        "Authorization": f"Bearer {access}"
    }
    for federation in federations:
        response = upload_federation(federation, headers, federation_url)

def handle_upload_competitions():
    access = login("admin", "password") # po idee, president bolu kerek myna zherde
    headers = {
        "Authorization": f"Bearer {access}"
    }

    federations = []
    organizators = []
    federation_response = requests.get(federation_url, headers=headers)
    if federation_response.status_code == 200:
        federations = federation_response.json()['data']
    else:
        print("There is a problem in fetching federations")


    organizator_response = requests.get(organizator_url, headers=headers)
    if organizator_response.status_code == 200:
        organizators = organizator_response.json()
    else:
        print("There is a problem in fetching organizators")


    # organizators = requests.get(organizator_url, headers=headers).json()
    if len(federations) == 0 or len(organizators) == 0:
        return "No federations or organizators"
    federation_index = 0
    organizator_index = 0

    for competition in competitions:
        response = upload_competition(competition, headers, competition_url, federations, organizators, federation_index, organizator_index)

def handle_upload_students():
    directory_path = 'scripting_images'
    for student in students:
        coach = None
        coach_response = requests.get(coach_url)
        if coach_response.status_code == 200:
            coaches = coach_response.json()
            random_index = random.randint(0, len(coaches) - 1)
            coach = coaches[random_index]
            response = upload_student(coach, student, student_url, directory_path)


def handle_upload_participants():
    
    regions = requests.get(region_url).json()

    competitions = requests.get(competition_url).json().get('data', [])

    for region in regions['data']:
        current_url = f"{competition_url}?region={region['slug']}"
        regional_competitions = requests.get(current_url).json().get('data', [])
        for regional_competition in regional_competitions:
            competitions.append(regional_competition)

    students = requests.get(student_url).json()
    
    age_categories = ['16-17', '14-15']
    weight_categories = ['44kg', '48kg']

    for competition in competitions:
        index = 1
        for student in students:
            participant_data = {}
            if index <= 8:
                participant_data = {'age_category': '16-17', 'weight_category': '48kg'}
            else:
                participant_data = {'age_category': '14-15', 'weight_category': '44kg'}

            index += 1
            upload_participant(participant_data, competition['id'], student['id'], student['coach']['id'], competition_url)

def handle_generate_games():
    competitions = requests.get(competition_url).json().get('data', [])
    regions = requests.get(region_url).json()
    for region in regions['data']:
        current_url = f"{competition_url}?region={region['slug']}"
        regional_competitions = requests.get(current_url).json().get('data', [])
        print(f"in region: {region}")
        print(regional_competitions)
        for regional_competition in regional_competitions:
            competitions.append(regional_competition)
    
    # print(competitions)

    for competition in competitions:
        generate_game(competition, competition['organizator'], competition_url)

def handle_randomly_selected_winners():
    competitions = requests.get(competition_url).json().get('data', [])
    regions = requests.get(region_url).json()
    for region in regions['data']:
        current_url = f"{competition_url}?region={region['slug']}"
        regional_competitions = requests.get(current_url).json().get('data', [])
        for regional_competition in regional_competitions:
            competitions.append(regional_competition)

    for competition in competitions:
        select_current_competition_winners(competition, competition['organizator'], competition_url)


if __name__ == "__main__":
    handle_upload_clubs()
    handle_upload_coaches()
    handle_upload_organizators()
    handle_upload_regions()
    handle_upload_federations()
    handle_upload_competitions()
    handle_upload_students()
    handle_upload_participants()
    handle_generate_games()
    handle_randomly_selected_winners()

