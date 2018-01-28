import github_worker_auth

class User:

    def __init__(self):
        self.github_subs = ['vrct','alirizakeles']
        self.gitlab_subs = []

    def get_subs_stars(self):

        for sub in self.github_subs:
            github_worker_auth.get_stars(sub)

ahmet = User()

ahmet.get_subs_stars()
