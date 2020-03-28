from datetime import datetime
from recipeApp.users.models import Profile


class ProfileFactory:

    @staticmethod
    def create(user):
        profile = Profile()
        profile.user = user
        profile.profile_info = ''
        profile.profile_picture = '/images/default-profile.png'
        profile.created_date = datetime.now()
        return profile
