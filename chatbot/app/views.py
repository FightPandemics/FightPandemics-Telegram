import abc


class AbstractPost(abc.ABC):
    def __init__(self, post_json):
        """Abstract class unifying the behaviour of Post and UserPost.
        Only how to extract the actual dictionary from the returned
        post data containing the relevant fields is left for the subclasses.
        """
        self._post_json = post_json

        self.title = self._extract_field('title')
        author_data = self._extract_field('author')
        self.author = author_data['name']
        self.categories = self._extract_field('categories')
        self.content = self._extract_field('content')
        self.title = self._extract_field('title')
        self.location = self._extract_location(author_data['location'])
        self.num_comments = self._extract_num_comments()

    def _extract_field(self, field):
        data = self._get_data_from_post_json()
        return data[field]

    @abc.abstractmethod
    def _get_data_from_post_json(self):
        pass

    @staticmethod
    def _extract_location(location_data):
        # TODO should the length of this list really depend on what's in the json?
        location = []
        for key in ['city', 'state', 'country']:
            entry = location_data.get(key)
            if entry is not None:
                location.append(entry)
        return location

    def _extract_num_comments(self):
        return str(self._post_json['numComments'])

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
