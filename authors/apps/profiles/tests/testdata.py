
"""Contains test data to emulate user request bodys and params"""
user_profile ={
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": True
  }
}
user_profile2={
  "profile": {
    "username": "joey",
    "bio": "I work at statefarm too",
    "image": "image-link",
    "following": False
  }
}

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

new_bio={
    "profile":{
        "bio":"Am an updated bio"
    }
}
valid_profile_update_data={
     "profile": {
    "username": "joey",
    "bio": "I work at statefarm too",
    "image": "image-link"
  }
}

no_avator_update_data={
     "profile": {
    "username": "joey",
    "bio": "I work at statefarm too",
    "image": "image-link"
  }
}
no_avator_and_username_update_data={
     "profile": {
    "username": "joey",
    "bio": "I work at statefarm too",
    "image": "image-link"
  }
}
no_user_name_profile={
    "bio": "I work at statefarm too",
    "image": "image-link"


}