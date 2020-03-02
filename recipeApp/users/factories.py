from datetime import datetime
from recipeApp.users.models import Profile


class AuthorFactory:

    @staticmethod
    def create(user):
        author = Profile()
        author.user = user
        author.profile_info = ''
        author.profile_picture = None
        author.created_date = datetime.now()
        return author
