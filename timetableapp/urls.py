from timetableapp.views import home,loginvalidation,oddevensemselect,subjectadded,facultyadded,loadallocation
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns=[
        url(r'^home/',home),
        url(r'^loginvalidation/',loginvalidation),
        url(r'^oddevensemselect/',oddevensemselect),
        url(r'^subjectadded/',subjectadded),
        url(r'^facultyadded/',facultyadded),
        url(r'^loadallocation/',loadallocation),
        url(r'^$',home),
]
