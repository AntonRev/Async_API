from enum import Enum


class MessageText(str, Enum):
    """
    Messages returned to user (e.g. in case of an error)
    """
    FILM_NOT_FOUND = 'film not found'
    PERSON_NOT_FOUND = 'person not found'
    GENRE_NOT_FOUND = 'genre not found'
