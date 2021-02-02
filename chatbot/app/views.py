class Post(object):

    def __init__(self, post_json):
        self.title = post_json['post']['title']
        self.author = post_json['post']['author']['name']
        self.categories = post_json['post']['categories']
        self.content = post_json['post']['content']
        self.num_comments = str(post_json['numComments'])
        self.location = []
        loc = post_json['post']['author']['location']
        for key in ['city', 'state', 'country']:
            if key in loc:
                self.location.append(loc[key])

    def display(self):
        """ Format UserPost in the following format to display on the UI

        # <Title>
        # By <Author Name> - <Location>
        # <Types>
        # <Content>
        # <Num > Comments
        """
        post_info = list()
        post_info.append(self.title)
        post_info.append('By {} - {}'.format(self.author, ", ".join(self.location)))
        post_info.append(", ".join(self.categories))
        post_info.append(self.content)
        post_info.append(self.num_comments + " Comments")
        return "\n\n".join(post_info)

### Ideally we should have a single object for post but POST api retruns different post objects
### when querying all posts by a user vs querying a single post. Untill, this discrepency is fixed, we will
### use two different objects


class UserPost(object):

    def __init__(self, post_json):
        self.title = post_json['title']
        self.author = post_json['author']['name']
        self.categories = post_json['categories']
        self.content = post_json['content']
        self.num_comments = str(post_json['commentsCount'])
        self.location = []
        loc = post_json['author']['location']
        for key in ['city', 'state', 'country']:
            if key in loc:
                self.location.append(loc[key])

    def display(self):
        """ Format UserPost in the following format to display on the UI

        # <Title>
        # By <Author Name> - <Location>
        # <Types>
        # <Content>
        # <Num > Comments
        """
        return "{} - {}  - {} comments".format(
            self.title, self.content[:50], self.num_comments)


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
        user_info = list()
        user_info.append("Name : {}".format(" ".join([self.firstName, self.lastName])))
        user_info.append("Email : {}".format(self.email))
        user_info.append("Volunteer : {}".format(self.is_volunteer))
        user_info.append("Address : {}".format(self.address))
        return "\n".join(user_info)






