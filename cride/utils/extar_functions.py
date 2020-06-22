"""Extra function."""

# Generals
import csv
import random
import string

# Models
from cride.circles.models import Circle


def random_about(n):
    """
    This function create a random about, it's base it in
    https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    :return: str[N]
    """
    about = """Lorem Ipsum is simply dummy text of the printing and typesetting
    industry. Lorem Ipsum has been the industry's standard dummy text ever
    since the 1500s, when an unknown printer took a galley of type and scrambled
    it to make a type specimen book. It has survived not only five centuries,
    but also the leap into electronic typesetting, remaining essentially unchanged.
    It was popularised in the 1960s with the release of Letraset sheets containing Lorem
    Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker
    including versions of Lorem Ipsum."""
    first = random.randint(0, n)
    last = (first + n) % len(about)
    return about[first:last]


def load_data_from_csv_to_circles(file_name):
    """
    This function upload data from csv to the circles table in the data base
    :param file_name: str name of the csv
    :return: none
    """

    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            members_limit = int(row['members_limit'])
            if members_limit > 0:
                is_limited = True
            else:
                is_limited = False

            about = random_about(100)

            data = {
                'name': row['name'],
                'slug_name': row['slug_name'],
                'about': about,
                'picture': '',
                'rides_offered': 0,
                'rides_taken': 0,
                'verified': row['verified'],
                'is_public': row['is_public'],
                'is_limited': is_limited,
                'members_limit': members_limit
            }
            c = Circle.objects.create(**data)
