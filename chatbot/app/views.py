import abc
import logging
from chatbot.app import user_data


class AbstractPost(abc.ABC):
    def __init__(self, post_json):
        """Abstract class unifying the behaviour of Post and UserPost.
        Only how to extract the actual dictionary from the returned
        post data containing the relevant fields is left for the subclasses.
        """
        self._post_json = post_json

        self.title = self._extract_field(user_data.POST_TITLE)
        author_data = self._extract_field(user_data.AUTHOR)
        self.author = author_data[user_data.AUTHOR_NAME]
        self.categories = self._extract_field(user_data.POST_CATEGORIES)
        self.content = self._extract_field(user_data.POST_DESCRIPTION)
        self.location = self._extract_location(author_data[user_data.LOCATION])
        self.num_comments = self._extract_field('commentsCount')

    def _extract_field(self, field):
        data = self._get_data_from_post_json()
        value = data.get(field)
        if value is None:
            logging.warning("No field {field} in data")
        return data[field]

    @abc.abstractmethod
    def _get_data_from_post_json(self) -> dict:
        pass

    @staticmethod
    def _extract_location(location_data):
        if location_data is None:
            location_data = {}
        location = []
        # TODO should the length of this list really depend on what's in the json?
        for key in ['city', 'state', 'country']:
            entry = location_data.get(key)
            if entry is not None:
                location.append(entry)
        return location

    def display(self):
        """ Format UserPost in the following format to display on the UI

        # <Title>
        # By <Author Name> - <Location>
        # <Types>
        # <Content>
        # <Num > Comments
        """
        # TODO is this doc-string correct? If so the format should be updated?
        return f"""{self.title}

By {self.author} - {", ".join(self.location)}

{",".join(self.categories)}

{self.content}

{self.num_comments} Comments"""


class Post(AbstractPost):
    def _get_data_from_post_json(self):
        return self._post_json['post']


class UserPost(AbstractPost):
    def _get_data_from_post_json(self):
        return self._post_json


class UserProfile(object):

    def __init__(self, json_data):
        self.email = json_data['email']
        self.firstName = json_data['firstName']
        self.lastName = json_data['lastName']
        self.address = json_data['location']['address']
        self.is_volunteer = "No"
        if json_data['objectives']['volunteer']:
            self.is_volunteer = "Yes"

    def display(self):
        return f"""Name: {self.firstName} {self.lastName}
Email: {self.email}
Volunteer: {self.is_volunteer}
Address: {self.address}"""
