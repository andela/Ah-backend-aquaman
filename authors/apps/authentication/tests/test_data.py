"""
authentication test data
"""
valid_user = {
    "user": {
        "username": "Bagzie12",
        "email": "bagendadeogracious@gmail.com",
        "password": "Password123"
    }
}

valid_login = {
    "user": {
        "email": "bagendadeogracious@gmail.com",
        "password": "Password123"
    }
}

valid_user_two = {
    "user": {
        "username": "crycetruly",
        "email": "crycetruly@gmail.com",
        "password": "xvq6thcuzy"
    }
}


valid_login_two = {
    "user": {
        "email": "crycetruly@gmail.com",
        "password": "xvq6thcuzy"
    }
}

wrong_password = {
    "user": {
        "email": "bagendadeogracious@gmail.com",
        "password": "Password12"
    }
}

wrong_email = {
    "user": {
        "email": "bagenda@gmail.com",
        "password": "Password123"
    }
}

missing_password_data = {
    "user": {
        "email": "Password123"
    }
}
missing_email_data = {
    "user": {
        "password": "Password123"
    }
}
empty_username = {
    "user": {
        "username": "",
        "email": "bagendadeogracious@gmail.com",
        "password": "Password123"
    }
}
empty_email = {
    "user": {
        "username": "Bagzie",
        "email": "",
        "password": "Password123"
    }
}
empty_password = {
    "user": {
        "username": "Bagzie",
        "email": "bagendadeogracious@gmail.com",
        "password": ""
    }
}
invalid_user_email = {
    "user": {
        "username": "Bagzie",
        "email": "bagendadegmail.com",
        "password": "Password123"
    }
}

short_password = {
    "user": {
        "username": "Bagzie",
        "email": "bagendadeogracious@gmail.com",
        "password": "Pass"
    }
}

missing_username_key = {
    "user": {
        "email": "bagendadeogracious@gmail.com",
        "password": "Password123"
    }
}


invalid_token = "eyJ0eXiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFoZWJ3YTEiLCJlbWFpbCI6ImNyeWNldHJ1bHlAZ21haWwuY29tIiwiZXhwIjoxNTUxNzc2Mzk0fQ.PFimaBvSaxR_cKwLmeRMod7LHkhNTcem22IXTrrg7Ko"
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFoZWJ3YTEiLCJlbWFpbCI6ImNyeWNldHJ1bHlAZ21haWwuY29tIiwiZXhwIjoxNTUxNzc2Mzk0fQ.PFimaBvSaxR_cKwLmeRMod7LHkhNTcem22IXTrrg7Ko"

invalid_username = {
    "user": {
        "username": "testus i",
        "email": "testuser@gmail.com",
        "password": "testing123"
    }
}

invalid_password = {
    "user": {
        "username": "testuser12",
        "email": "testuser@gmail.com",
        "password": "testingui"
    }
}

same_email = {
    "user": {
        "username": "roy12",
        "email": "bagendadeogracious@gmail.com",
        "password": "Password123"
    }
}

same_username = {
    "user": {
        "username": "Bagzie12",
        "email": "roywaisibani@gmail.com",
        "password": "Password123"
    }
}

responses = {
    'test_login_with_invalid_user_fails':{
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },

    'invalid_username':{
        "errors":{
            "username": [
                "Username cannot contain special characters."
            ]
        }
    },

    'invalid_email':{
        "errors":{
            "email": [
                "Enter a valid email address."
            ]
        }
    },


    'test_login_with_missing_email_fails': {
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },
    'email_already_exists':{
            "errors": {
                "email": [
                    "user with this email already exists."
                ]
            }
        },
    'password_is_too_short': {
            "errors": {
                "password": [
                    "Password should be atleast 8 characters"
                ]
            }
        },
    'password_is_weak':  {
            "errors": {
                "password": [
                    "Password should at least contain a number, capital and small letter."
                ]
            }
        },
    'username_already_exists': {
            "errors": {
                "username": [
                    "user with this username already exists."
                ]
            }
        }
}
