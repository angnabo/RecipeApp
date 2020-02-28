from datetime import datetime
from recipeApp.users.models import Author


class AuthorFactory:

    @staticmethod
    def create(user):
        author = Author()
        author.user = user
        author.full_name = user.get_full_name()
        author.profile_info = ''
        author.profile_picture = None
        author.created_date = datetime.now()
        return author
