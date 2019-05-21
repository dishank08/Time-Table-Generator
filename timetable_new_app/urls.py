from timetable_new_app.views import generatetimetable,home,loginvalidation,oddevensemselect,subjectadded,facultyadded,loadallocation,subjectselect,facultyselect
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns=[
        url(r'^home/',home),
        url(r'^loginvalidation/',loginvalidation),
        url(r'^oddevensemselect/',oddevensemselect),
        url(r'^subjectadded/',subjectadded),
        url(r'^facultyadded/',facultyadded),
        url(r'^subjectselect/',subjectselect),
        url(r'^facultyselect/',facultyselect),
        url(r'^loadallocation/',loadallocation),
        url(r'^generatetimetable/',generatetimetable),
        url(r'^$',home),
]
