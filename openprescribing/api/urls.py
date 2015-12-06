from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
import api.views_bnf_codes as views_bnf_codes
import api.views_spending as views_spending
import api.views_org_codes as views_org_codes
import api.views_org_details as views_org_details
import api.views_org_location as views_org_location

urlpatterns = [

    url(r'^spending/$', views_spending.total_spending, name='total_spending'),
    url(r'^spending_by_ccg/$', views_spending.spending_by_ccg, name='spending_by_ccg'),
    url(r'^spending_by_practice/$', views_spending.spending_by_practice, name='spending_by_practice'),
    url(r'^org_details/$', views_org_details.org_details),
    url(r'^bnf_code/$', views_bnf_codes.bnf_codes),
    url(r'^org_code/$', views_org_codes.org_codes),
    url(r'^org_location/$', views_org_location.org_location),

    url(r'^docs/', include('rest_framework_swagger.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns,
                                     allowed=['json', 'csv'])
