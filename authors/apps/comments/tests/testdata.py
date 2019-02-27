
"""Contains test data to emulate user request bodys and params"""
user = {
    "user": {
        "username": "jake",
        "email": "jake@gmail.com",
        "password": "test12!U"
    }
}
user2 = {
    "user": {
        "username": "jakee",
        "email": "jakee@gmail.com",
        "password": "test12!Ue"
    }
}
comment = {
    "comment": {
        "article": 1,
        "body": "hello World",
        "author": {
            "username": "jake",
            "bio": "I work at statefarm",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
            "following": False
        }
    }
}
comment_no_article = {
    "comment": {
        "body": "hello World",
        "author": {
            "username": "jake",
            "bio": "I work at statefarm",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
            "following": False
        }
    }
}
comment_no_body = {
    "comment": {
        "article": 1,

        "author": {
            "username": "jake",
            "bio": "I work at statefarm",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
            "following": False
        }
    }
}
comment_no_author = {
    "comment": {
        "article": 1,
        "body": "It takes a Jacobian",

    }
}

user = {
    "user": {
        "email": "jake@jake.jake",
        "bio": "I like to skateboard",
        "image": "https://i.stack.imgur.com/xHWG8.jpg"
    }
}
article_response = {
    "article": {
        "slug": "how-to-train-your-dragon",
        "title": "How to train your dragon",
        "description": "Ever wonder how?",
        "body": "It takes a Jacobian to say hello World",
        "tagList": ["dragons", "training"],
        "createdAt": "2016-02-18T03:22:56.637Z",
        "updatedAt": "2016-02-18T03:48:35.824Z",
        "favorited": False,
        "favoritesCount": 0,
        "author": {
            "username": "jake",
            "bio": "I work at statefarm",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
            "following": False
        }
    }
}
article = {
    "article": {
        "slug": "how-to-train-your-dragon",
        "title": "How to train your dragon",
        "description": "Ever wonder how?",
        "body": "It takes a Jacobian",
        "tagList": ["dragons", "training"],
        "author": {
            "username": "jake",
            "bio": "I work at statefarm",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
            "following": False
        }
    }
}
single_reply = {
    "reply": {
        "body": "Hello world"
    }
}
