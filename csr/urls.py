from django.urls import path
from csr.views import GasUtilLoginView, CSRCustomers, GasUtilCustSR, GasUtilUserLogout, GasUtilCSRHandlingTool, APIGasUtilSRStateToggle, GasUtilSpecificSR, GasUtilAccountInfo

urlpatterns = [
    # auth
    path('login', GasUtilLoginView.as_view(), name="gas-utility-login"),
    path('logout', GasUtilUserLogout.as_view(), name="gas-utility-logout"),

    #CSR-facing
    path('customers', CSRCustomers.as_view(), name="csr-customers"),
    path('srmanager', GasUtilCSRHandlingTool.as_view(), name='gas-util-csr-sr-manager'),

    # customer-facing
    path('customer/service_request', GasUtilCustSR.as_view(), name='gas-util-cust-SR'),
    path('customer/service_request/<int:pk>', GasUtilSpecificSR.as_view(), name='gas-util-cust-SR-specific'),
    path('customer/account_info', GasUtilAccountInfo.as_view(), name='gas-util-cust-account-info'),

    # api paths
    path('csr_sr_state_toggler', APIGasUtilSRStateToggle.as_view(), name='gas-util-csr-sr-state-toggle'),

]