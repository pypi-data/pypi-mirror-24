from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SubscriptionCreateView

urlpatterns = {
    url(r'^stripe/subscription', SubscriptionCreateView.as_view(), name='lp_stripe_subscriptioncreate')
}

urlpatterns = format_suffix_patterns(urlpatterns)
