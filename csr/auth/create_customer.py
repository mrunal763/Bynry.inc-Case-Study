from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from csr.models import GasUtilCustomers
import uuid

class OrgCustomerCreation:

    email = None
    __password = None
    user_group = None
    first_name = None
    last_name = None
    employee_id = None

    def __init__(self, **kwargs) -> None:
        self.email = kwargs['email']
        self.__password = kwargs['password']
        self.user_group = kwargs['user_group']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.employee_id = kwargs['employee_id']

    def __generate_pbdkf2_code(self):
        try:
            validate_password(self.__password)
            self.__password = make_password(self.__password)
            print(self.__password)
            return True
        except Exception as e:
            print(e)
            return False
        
    
    def __generate_username(self):
        print(self.email.split('@')[0])
        return self.email.split('@')[0]

    def add_user_to_db(self):
        if self.__generate_pbdkf2_code():
            try:
                user_obj = User.objects.create_user(email=self.email, username=self.__generate_username(), password=self.__password, is_active=True, first_name=self.first_name, last_name = self.last_name)

                GasUtilCustomers.objects.create(customer_ref=user_obj, csr_employee_ref=User.objects.get(id=self.employee_id), unique_customer_tracking_id=str(uuid.uuid4()))
                
                user_obj.groups.set([self.__add_to_group()])

                return True

            except Exception as e:
                print(e)
                return False

    def __add_to_group(self):
        group_obj = Group.objects.get(name=self.user_group)
        print(group_obj)
        return group_obj
        
