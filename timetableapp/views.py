from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Subject,Faculty,LoadAllocate

def home(request):
    c={}
    c.update(csrf(request))
    return render_to_response('home.html',c)


def loginvalidation(request):
    c={}
    c.update(csrf(request))
    uname = request.POST['Name']
    passwd = request.POST['Password']
    if(uname=="admin" and passwd=="admin"):
        return render_to_response('oddeven.html',c)

def oddevensemselect(request):
    c={}
    c.update(csrf(request))
    return render_to_response('oddeven.html',c)

def subjectadded(request):
    c={}
    c.update(csrf(request))
    sname=request.POST.get('subname')
    sem=request.POST.get('sem',0)
    theoryh=request.POST.get('theoryhours',0)
    practicalh=request.POST.get('practhours',0)
    s=Subject(sub_name=sname,semester=sem,theory_hours=theoryh,practical_hours=practicalh)
    s.save()
    return render_to_response('addsubject.html',c)

def facultyadded(request):
    c={}
    c.update(csrf(request))
    fname=request.POST.get('facname','')
    subname=request.POST.get('subname')
    theoryh=request.POST.get('theoryhours',0) 
    practicalh=request.POST.get('practhours',0)
    s=Faculty(faculty_name=fname,sub_name_id=subname,theory_hours=theoryh,practical_hours=practicalh)
    s.save()
    return render_to_response('addfaculty.html',c)

def loadallocation(request):
    c={}
    c.update(csrf(request))
    k=0
    l=0
    m=''
    x = Subject.objects.all()
    y = Faculty.objects.all()
    for i in x:
        k=0
        l=0
        for j in y:
            if(j.sub_name_id == i.sub_name):
                k+=j.theory_hours
                l+=j.practical_hours
                m=j.sub_name_id
        s=LoadAllocate(sub_name=m,theory_hours=k,pract_hours=l)
        s.save()
    la=LoadAllocate.objects.all()            
    return render(request,'load.html',{'load':la})


# Create your views here.
