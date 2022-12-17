import uuid


class QueryData:
    FILM = {
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': str(uuid.uuid4()), 'name': 'Ann'},
            {'id': str(uuid.uuid4()), 'name': 'Bob'}
        ],
        'writers': [
            {'id': str(uuid.uuid4()), 'name': 'Ben'},
            {'id': str(uuid.uuid4()), 'name': 'Howard'}
        ],
    }

    GENRE = {
        'id': str(uuid.uuid4()),
        'name': 'Comedy',
        'description': 'Well... comedy is very subjective.',
        'films': [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    }

    PERSON = {
        'id': str(uuid.uuid4()),
        'full_name': 'Ann',
        'roles': ['Acter', 'Director'],
        'films': [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    }
