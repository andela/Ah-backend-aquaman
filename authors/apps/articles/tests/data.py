"""
    File holding the data for the tests
"""
new_user = {
    "user": {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing123"
    }
}

post_article = {
    "article": {
        "title": "Importance of github",
        "content": "Github helps us manage version control",
        "tags": ["science", "technology"]
    }
}
post_article_2 = {
    "article": {
        "title": "test post",
        "content": "this is a test post",
        "tags": ["python", "technology", "programming"]
    }
}

article_missing_data = {
    "article": {
        "title": "The use of slack",
        "content": "Slack is one of the tools used for communication amongest agile teams"
    }
}

update_article = {
    "article": {
        "title": "Ruby on Rails",
        "content": "Ruby on rails has emerged as one of the fastest growing development tools"
    }
}
