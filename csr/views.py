from typing import Any
from django.shortcuts import render, redirect

from django.views import View
from .auth.login import OrgAuth
from .auth.create_customer import OrgCustomerCreation

from uuid import uuid4
import datetime

from csr.models import GasUtilCustomers, GasUtilServiceRequest, GasUtilServiceRequestAttachments

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import GasUtilServiceRequestSerializer


# Login view for the gas utility
class GasUtilLoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        is_validated = None
        role = None

        org_auth_obj = OrgAuth(request, request.POST.get('email'), request.POST.get('password'))

        # sets the message if user is valid
        is_validated = org_auth_obj.return_if_is_authenticated()
        print(is_validated)
        
        role = org_auth_obj.role_redirect()
        
        if is_validated is False:
            return render(request, "login.html", {'auth_validated':is_validated})
            # return redirect(role)

        # returns the admin/employee for travel/recruitment
        if(role is not None and is_validated is not False):
            return redirect(role)

        return render(request, 'login.html', {'auth_validated':is_validated})
    


# logout for gas utility
class GasUtilUserLogout(View, LoginRequiredMixin):

    def get(self, request):
        logout(request)
        return redirect('gas-utility-login')


# CSR facing customer handling portal
class CSRCustomers(View, LoginRequiredMixin):

    total_customers_present = None
    customer_objects = None


    def get(self, request):
        customer_objects = GasUtilCustomers.objects.filter(csr_employee_ref=request.user.id)
        return render(request, 'csr/customers.html', {'cust_count':customer_objects.count(), 'customers':customer_objects})

    def post(self, request):

        customer_objects = GasUtilCustomers.objects.filter(csr_employee_ref=request.user.id)

        org_customer_creation = OrgCustomerCreation(
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            employee_id=request.user.id,
            user_group='customer',
        )

        status_of_user_created = org_customer_creation.add_user_to_db()

        return render(request, 'csr/customers.html', {'cust_count':customer_objects.count(), 'customers':customer_objects, 'user_created_status': status_of_user_created})
    


# customer facing CSR handler
class GasUtilCustSR(View, LoginRequiredMixin):

    total_sr_present = None
    service_request_objects = None

    def get(self, request):
        service_request_objects = GasUtilServiceRequest.objects.filter(customer_ref__customer_ref=request.user.id)
        return render(request, 'customer/service_request.html', {'sr_count':service_request_objects.count(), 'service_requests':service_request_objects})
    

    def post(self, request):
        service_request_objects = GasUtilServiceRequest.objects.filter(customer_ref__customer_ref=request.user.id)
        try:
            gas_util_service_request = GasUtilServiceRequest.objects.create(
                customer_ref = GasUtilCustomers.objects.get(customer_ref=request.user.id),
                type_of_service = request.POST['type_of_service'],
                service_request_details = request.POST['service_request_details']
            )

            sr_all_attachments = dict(request.FILES)
            sr_attachment_objects_to_be_created = [GasUtilServiceRequestAttachments(gas_util_service_request_ref=gas_util_service_request, attachment=file) for file in sr_all_attachments['sr_attachments']]

            #bulk_create
            objs = GasUtilServiceRequestAttachments.objects.bulk_create(
                sr_attachment_objects_to_be_created
            )

        except Exception as e:
            print(e)
            status = False

        return render(request, 'customer/service_request.html', {'sr_count':service_request_objects.count(), 'service_requests':service_request_objects})
    


# CSR facing request handling tool
class GasUtilCSRHandlingTool(View, LoginRequiredMixin):

    total_sr_present = None
    service_request_objects = None

    
    def get(self, request):
        service_request_objects = GasUtilServiceRequest.objects.filter(customer_ref__csr_employee_ref=request.user.id)
        return render(request, 'csr/sr_tool.html', {'sr_count':service_request_objects.count(), 'service_requests':service_request_objects})


# customer facing specific SR details
class GasUtilSpecificSR(View, LoginRequiredMixin):

    def get(self, request, pk):

        gas_util_specific_sr = GasUtilServiceRequest.objects.get(id=pk)
        gas_util_specific_sr_attachments = GasUtilServiceRequestAttachments.objects.filter(gas_util_service_request_ref=pk)

        return render(request, 'customer/sr_details.html', {'sr_id': pk, 'gas_util_specific_sr':gas_util_specific_sr, 'gas_util_specific_sr_attachments': gas_util_specific_sr_attachments})



class GasUtilAccountInfo(View, LoginRequiredMixin):

    def get(self, request):

        sr_info_per_account = {
            "pending_count": GasUtilServiceRequest.objects.filter(customer_ref__customer_ref=request.user.id, status=0).count(),
            "resolved_count": GasUtilServiceRequest.objects.filter(customer_ref__customer_ref=request.user.id, status=1).count(),
            "paid_count": GasUtilServiceRequest.objects.filter(customer_ref__customer_ref=request.user.id, status=2).count()
        }

        customer_info = GasUtilCustomers.objects.get(customer_ref=request.user.id)

        return render(request, 'customer/account_information.html', {'sr_info_per_account':sr_info_per_account, 'customer_info':customer_info})




# API to change the state of the SR
class APIGasUtilSRStateToggle(APIView):


    response_obj = {'code': status.HTTP_204_NO_CONTENT}

    def __return_status_code_for_sr(self, data, status_string):

        match status_string:
            case "pending":
                data['status'] = 0
            case "resolved":
                data['status'] = 1
                data['resolved_on'] = datetime.datetime.now()
            case "paid":
                data['status'] = 2
                data['service_paid_on'] = datetime.datetime.now()
            case _:
                raise ValueError('Invalid status format')
        
        return data

    def put(self, request, format=None):

        data = request.data.copy()
        try:
            gas_util_sr_object = GasUtilServiceRequest.objects.get(id=data.get('id'))
            data = self.__return_status_code_for_sr(data, data.get('status'))
            data.pop('csrfmiddlewaretoken')
            
            gas_util_service_request_serializer = GasUtilServiceRequestSerializer(gas_util_sr_object, data=data, partial=True)

            if gas_util_service_request_serializer.is_valid():
                gas_util_service_request_serializer.save()
                self.response_obj['code'] = status.HTTP_200_OK
            else:
                print(gas_util_service_request_serializer.errors)
                self.response_obj['code'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        except Exception as e:
            print(e)
            self.response_obj['code'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(self.response_obj)
    