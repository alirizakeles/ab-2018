class DB:
    GITHUB_STAR_KEY = 'Github:Stars:{}'
    GITLAB_STAR_KEY = 'Gitlab:Stars:{}'
    GITHUB_REPO_KEY = 'Github:Repos:{}'
    GITLAB_REPO_KEY = 'Github:Repos:{}'
    USER_KEY = 'User:{}'
    TEMP_USER_KEY = 'temp:User:{}'

class QUEUE:
    GITHUB_WORKER_QUEUE = 'github_queue'
    GITLAB_WORKER_QUEUE = 'gitlab_queue'
    SCHEDULE_NOTIFIER_QUEUE = 'schedule_notifier_queue'
    NEW_USER_QUEUE = 'schedule_queue'
