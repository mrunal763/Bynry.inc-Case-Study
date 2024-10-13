from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

class OrgAuth:

    # class variables to manage auth ops 
    __request = None
    email = None
    password = None
    __user_obj = None

    
    # loading constructor with request, email and password of auth form
    def __init__(self, request, email, password) -> None:
        self.__request = request
        self.email = email
        self.password = password
    
    # [private] returns username referencing email passed
    # IMP: DO NOT MAKE THIS FUNCTION PUBLIC. Use request.user if needed.
    def __get_username(self):
        try:
            self.__user_obj = User.objects.get(email=self.email)
            return True
        except Exception as e:
            print(e)
            return False
        
    # returns boolean if user is authenticated or not
    # [NEWSOL] return type will be object to pass a custom message to be set as response
    def return_if_is_authenticated(self):
        if(self.__get_username()):
            print('username: ', self.__user_obj.username, ' password: ', self.password)
            self.__user_obj = authenticate(username=self.__user_obj.username, password=self.password)
            if self.__user_obj is not None:
                try:
                    login(self.__request, self.__user_obj)
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                print('Entering else for auth')
                return False

    # returns group type for the authenticated user only
    # IMP: DO NOT MAKE THIS FUNCTION PUBLIC. Use role_redirect() if needed.
    def __return_auth_group(self):
        user_groups = self.__user_obj.groups.all().values_list('name', flat=True)
        return list(user_groups)
    
    
    # returns path for redirecting the user to its designated dashboard
    # IMP: Do not use the code below 3.10.0 since match support is >3.10.0
    def role_redirect(self):
        try:
            match self.__return_auth_group()[0]:
                case "csr":
                    return '/csr/customers'
                case "customer":
                    return '/csr/customer/service_request'
                case _:
                    return '/csr/login'
        except Exception as e:
            return '/csr/login'