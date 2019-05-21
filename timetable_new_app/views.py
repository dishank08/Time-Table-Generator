from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import *
from django.db.models import Max
from numpy import empty,zeros
from operator import itemgetter
import random
from .resource import *
from xlwt import Workbook,easyxf

faculty_id=0

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
        return render_to_response('addsubject.html',c)
    else:
        return render(request,'home.html',{'msg':"Invalid credentials"})

def oddevensemselect(request):
    c={}
    c.update(csrf(request))
    return render_to_response('oddeven.html',c)

def subjectselect(request):
    c={}
    c.update(csrf(request))
    return render_to_response('addsubject.html',c)

def facultyselect(request):
    c={}
    c.update(csrf(request))
    return render_to_response('addfaculty.html',c)

def subjectadded(request):
    c={}
    c.update(csrf(request))
    sname=request.POST.get('subname','')
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
    subname=request.POST.get('subname','')
    theoryh=request.POST.get('theoryhours') 
    practicalh=request.POST.get('practhours')
    global faculty_id
    temp=Faculty.objects.filter(faculty_name=fname)
    if temp.exists()==True:
        if Faculty.objects.filter(faculty_name=fname,sub_name_id=subname).exists()==True:
            temp_new=Faculty.objects.filter(faculty_name=fname,sub_name_id=subname)
            for i in temp_new:
                temp_new_var=i.fac_id
                faculty_id=temp_new_var
                temp_new.delete()
                f = Faculty(fac_id=faculty_id,faculty_name=fname,sub_name_id=subname,theory_hours=theoryh,practical_hours=practicalh)
                f.save()
        else:
            for i in temp:
                temp_new_var=i.fac_id
                faculty_id=temp_new_var
                f = Faculty(fac_id=faculty_id,faculty_name=fname,sub_name_id=subname,theory_hours=theoryh,practical_hours=practicalh)
                f.save()
    else:     
        #faculty_id=faculty_id+1
        #fac=Faculty(fac_id=faculty_id)
        while True:
            faculty_id=faculty_id+1
            fac=Faculty.objects.filter(fac_id=faculty_id)
            if fac.exists()==True:
                continue
            else:
                break
        f = Faculty(fac_id=faculty_id,faculty_name=fname,sub_name_id=subname,theory_hours=theoryh,practical_hours=practicalh)
        f.save()
    #temp=Faculty.Objects.get(faculty_name=fname,sub_name_id=subname)
    #fac=Faculty_Subject_Totalhours(faculty_name_id=temp.fname,sub_name_id=temp.sub_name,total_hours=temp.theoryh+temp.practicalh)
    #fac.save()
    return render_to_response('addfaculty.html',c)


def generatetimetable(request):
    c={}
    c.update(csrf(request))
    lab_alloc=[]
    lec_c_div=[]
    lec_d_div=[]
    sub_practical=[]
    sub_theory=[]
    hours=0
    length_of_lab_alloc=0
    record=Faculty.objects.filter(practical_hours__gt=hours)
    #print("record")
    #print(record)
    #print(len(record))
    for i in record:
        fname=i.faculty_name
        facultyid=i.fac_id
        subname=i.sub_name_id
        practhours=i.practical_hours
        sem_sub=Subject.objects.filter(sub_name=subname)
        for j in sem_sub:
            semester=j.semester
            t=[fname,facultyid,subname,semester,practhours]
            lab_alloc.append(t)
    length_of_lab_alloc=len(lab_alloc)
    fname=" "
    facultyid=-1
    subname=" "
    semester=100
    practhours=100
    t=[fname,facultyid,subname,semester,practhours]
    lab_alloc.append(t)
    max_id=0
    test_id = Faculty.objects.filter().aggregate(Max('fac_id'))
    for i in test_id:
        max_id=test_id[i]
    print("max id is : ",max_id)
    sub=Subject.objects.all()
    record_lec_c=Faculty.objects.filter(theory_hours__gt=hours)
    max_val=0
    for i in sub:
        if i.theory_hours>0:
            subname_with_fac=i.sub_name
            #print("subject : ",subname_with_fac)
            total_fac=Faculty.objects.filter(sub_name_id=subname_with_fac,theory_hours__gt=hours).count()
            #print("total faculties of that subject: ",total_fac)
            facs=Faculty.objects.filter(sub_name_id=subname_with_fac,theory_hours__gt=hours)
            if total_fac==2:
                for j in facs:
                    fac_th_name=j.faculty_name
                    fac_th_id=j.fac_id
                    sub_th=j.sub_name_id
                    sem_th=i.semester
                    th_hours=int(j.theory_hours/2)
                    th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                    th2=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                    #print("th1 inside 2 facs :",th1)
                    #print("th2 inside 2 facs :",th2)
                    lec_c_div.append(th1)
                    lec_d_div.append(th2)
            elif total_fac>2:
                max_val=0
                max_hours=Faculty.objects.filter(sub_name_id=subname_with_fac).aggregate(Max('theory_hours'))
                for j in max_hours:
                    max_val=max_hours[j]
                    #print("max_val is : ",max_val)
                take_one=Faculty.objects.filter(sub_name_id=subname_with_fac,theory_hours=max_val)
                for j in take_one:
                    fac_th_name=j.faculty_name
                    fac_th_id=j.fac_id
                    sub_th=j.sub_name_id
                    sem_th=i.semester
                    th_hours=int(j.theory_hours/2)
                    th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                    th2=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                    #print("th1 inside max hours of facs : ",th1)
                    #print("th2 inside max hours of facs : ",th2)
                    lec_c_div.append(th1)
                    lec_d_div.append(th2)
                    
                flag_allocated=0
                
                for j in facs:
                    if j.theory_hours!=max_val:
                        if flag_allocated==0:
                            fac_th_name=j.faculty_name
                            fac_th_id=j.fac_id
                            sub_th=j.sub_name_id
                            sem_th=i.semester
                            th_hours=j.theory_hours
                            th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                            #print("if th1 inside not max of facs : ",th1)
                            lec_c_div.append(th1)
                            flag_allocated=1
                        else:
                            fac_th_name=j.faculty_name
                            fac_th_id=j.fac_id
                            sub_th=j.sub_name_id
                            sem_th=i.semester
                            th_hours=j.theory_hours
                            th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
                            #print("else th1 inside not max of facs : ",th1)
                            lec_d_div.append(th1)
                            flag_allocated=0
    #
    fac_th_name="---"
    fac_th_id=-1
    sub_th="---"
    sem_th=1000
    th_hours=1000
    th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
    lec_c_div.append(th1)                                   # lec_c_div has all faculties which take subject in c div
    lec_d_div.append(th1)                                   # lec_d_div has all faculties which take subject in d div
    len_of_c=len(lec_c_div)
    len_of_d=len(lec_d_div)
    sorted_lab_alloc = sorted(lab_alloc,key=itemgetter(4))
    sorted_lec_c_div = sorted(lec_c_div,key=itemgetter(4))
    sorted_lec_d_div = sorted(lec_d_div,key=itemgetter(4))
    print("lab_alloc")
    print(sorted_lab_alloc)
    print("lec_c_div")
    print(sorted_lec_c_div)
    print("lec_d_div")
    print(sorted_lec_d_div)
    #print("lec_c_div", len(lec_c_div))
    #print("lec_d_div", len(lec_d_div))
    fac_th_name="$$$"
    fac_th_id=-1
    sub_th="$$$"
    sem_th=1000
    th_hours=1000
    th1=[fac_th_name,fac_th_id,sub_th,sem_th,th_hours]
    sorted_lec_c_div.append(th1)
    sorted_lec_d_div.append(th1)
    #
    subjects=Subject.objects.all()
    for j in subjects:
        if j.practical_hours>0:
            subname=j.sub_name
            sem=j.semester
            theory=j.theory_hours
            pract=j.practical_hours
            allocated=0
            t1=[subname,sem,(theory*2),(pract*8),allocated]
            sub_practical.append(t1)
        if j.theory_hours>0:
            subname=j.sub_name
            sem=j.semester
            theory=j.theory_hours
            pract=j.practical_hours
            allocated=0
            t2=[subname,sem,(theory*2),(pract*8),allocated]
            sub_theory.append(t2)
    #print("sub theory")
    #print(sub_theory)
    #print(sorted_sub_practical)
    #print(len(sub_theory))
    sub_theory_len=len(sub_theory)
    sub_practical_len=len(sub_practical)
    sorted_sub_practical=sorted(sub_practical,key=itemgetter(1))               # semester wise sorted list of all practical subjects
    sorted_sub_theory=sorted(sub_theory,key=itemgetter(1))
    print("sub practical")                                                     # semester wise sorted list of all theory subjects
    print(sorted_sub_practical)
    print("sub theory")
    print(sorted_sub_theory)
    sizesem4pract=0
    sizesem4theory=0
    sizesem6pract=0
    sizesem6theory=0
    for i in sorted_sub_theory:
        if i[1] == 4 and i[2] != 0:
            sizesem4theory = int(sizesem4theory) + 1
        if i[1] == 6 and i[2] != 0:
            sizesem6theory = int(sizesem6theory) + 1

    for i in sorted_sub_practical:
        if i[1] == 4 and i[3] != 0:
            sizesem4pract = int(sizesem4pract) + 1
        if i[1] == 6 and i[3] != 0:
            sizesem6pract = int(sizesem6pract) + 1
                    
    print("sizesem6theory:",sizesem6theory)
    print("sizesem4theory:",sizesem4theory)
    print("sizesem6pract:",sizesem6pract)
    print("sizesem4pract:",sizesem4pract)


    #sub_practical.sort(key=sortSecond)
    #sub_theory.sort(key=sortSecond)
    #print("sub theory :",sorted_sub_theory)
    #print("sub practical ",len(sorted_sub_practical))
    #print("sub theory len %d",sub_theory_len)
    #print("sub practical len %d",sub_practical_len)
    sth=[4,5,5]                                                                # no of theory subjects in sem 2,4,6
    spr=[4,7,5]                                                                # no of practical subjects in sem 2,4,6
    total_fac = int(max_id)
    faculty_hours = empty(int(max_id)+1)
    new_faculty_hours = faculty_hours.astype(int)
    for i in range(0,int(max_id)+1):
        new_faculty_hours[i] = 0

    old_a=empty([int(max_id)+1,8])
    a=old_a.astype(int)
    for i in range(0,int(max_id)+1):
        for j in range(0,8):
            a[i][j]=0                                                          # a[24][8] = 24 faculties with 8 slots

    old_alloc_lab=empty([6,6,8])
    alloc_lab=old_alloc_lab.astype(int)

    for i in range(0,6):
        for j in range(0,6):
            for k in range(0,8):
                alloc_lab[i][j][k]=0                                           # to keep track of previous day's practical allocation

    r=0
    k=0
    m=0
    total=length_of_lab_alloc
    #print("total : ",total)
    allocated=empty([sub_theory_len,6])
    alc=allocated.astype(int)
    for i in range(0,sub_theory_len):
        for j in range(0,6):
            alc[i][j]=0

    allocated1=empty([sub_practical_len])
    alc_lab=allocated1.astype(int)
    for i in range(0,sub_practical_len):
        alc_lab[i]=0

    old_theory=empty([5,6,8])
    old_prac=empty([5,6,4])
    theory=old_theory.astype(int)
    prac=old_prac.astype(int)
    for i in range(0,5):
        for j in range(0,6):
            for k in range(0,4):
                prac[i][j][k]=length_of_lab_alloc
            for k in range(0,8):
                theory[i][j][k]=int(len_of_c)-1                                             # day , semester and slot of theory subject

    sp=[[4,2,6,2,0,4],[4,2,6,2,0,4],[4,2,6,2,0,4],[4,2,6,2,0,4],[4,2,6,2,0,4]]
    st=[[(0,1,2,3),(4,5,6,7),(2,3,4,5),(4,5,6,7),(2,3,4,5),(0,1,2,3)],[(0,1,2,3),(4,5,6,7),(2,3,4,5),(4,5,6,7),(2,3,4,5),(0,1,2,3)],[(0,1,2,3),(4,5,6,7),(2,3,4,5),(4,5,6,7),(2,3,4,5),(0,1,2,3)],[(0,1,2,3),(4,5,6,7),(2,3,4,5),(4,5,6,7),(2,3,4,5),(0,1,2,3)],[(0,1,2,3),(4,5,6,7),(2,3,4,5),(4,5,6,7),(2,3,4,5),(0,1,2,3)]]
    #sp=[[4,2,0,4,6,2],[6,2,4,2,0,4],[0,4,6,2,4,2],[0,4,4,2,6,2],[6,2,0,4,4,2]]
    #st=[[(0,1,2,3),(4,5,6,7),(2,3,4,5),(2,3,6,7),(2,3,4,5),(0,1,4,5)],[(2,3,4,5),(0,1,4,5),(0,1,2,3),(4,5,6,7),(2,3,4,5),(2,3,6,7)],[(2,3,4,5),(2,3,6,7),(2,3,4,5),(0,1,4,5),(0,1,2,3),(4,5,6,7)],[(2,3,4,5),(2,3,6,7),(0,1,2,3),(4,5,6,7),(2,3,4,5),(0,1,4,5)],[(2,3,4,5),(0,1,4,5),(2,3,4,5),(2,3,6,7),(0,1,2,3),(4,5,6,7)]]
    #sp=[[4,2,4,6,6,2],[6,2,6,4,2,0],[0,4,4,6,2,6],[0,4,6,6,4,0],[6,2,6,4,0,2]]                                                          # slot no for practical allocation for sem 2,4,6
    #st=[[(0,1,2,3),(4,5,6,7),(0,1,2,3),(2,3,4,5),(2,3,4,5),(0,1,4,5)],[(2,3,4,5),(0,1,4,5),(2,3,4,5),(0,1,2,3),(0,1,4,5),(2,3,4,5)],[(2,3,4,5),(2,3,6,7),(0,1,2,3),(2,3,4,5),(0,1,4,5),(0,1,4,5)],[(2,3,4,5),(2,3,6,7),(2,3,4,5),(2,3,4,5),(0,1,2,3),(2,3,6,7)],[(2,3,4,5),(0,1,4,5),(2,3,4,5),(0,1,2,3),(2,3,4,5),(0,1,4,5)]]          # slot no for theory allocation for sem 2,4,6
    theoryslots=0
    remaining_theory=[]
    for x in range(0,5):
        ind=111        
        #theory allocation
        for i in range(2,6):
            for p in range(0,4):
                r=0
                k=0
                counter2=0
                m=random.randrange(0,500)
                while True:
                    #print("inside theory while")
                    #r=(m)%sth[int(i/2)]
                    #m=int(m)+1
                    if i>=2 and i<4:
                        m=m+1
                        r=(m)%int(sizesem4theory)
                        #print("r:",r)
                    elif i>=4 and i<6:
                        m=m+1
                        r=(m)%int(sizesem6theory)
                        r=r+int(sizesem4theory)
                        #print("r:",r)
                    if int(ind)!=int(r):
                        if i==2 or i==4:
                            #print("inside i==2 || i==4 ")
                            for k in range(0,int(len_of_c)):
                                #print("hello")
                                if int(x)==4 and sorted_lec_c_div[k][2] == sorted_sub_theory[r][0] and a[sorted_lec_c_div[k][1]][st[x][i][p]] == 0 and sorted_lec_c_div[k][4]>=1:
                                    break
                                if sorted_lec_c_div[k][2] == sorted_sub_theory[r][0] and a[sorted_lec_c_div[k][1]][st[x][i][p]] == 0 and sorted_lec_c_div[k][4]>=1 and new_faculty_hours[sorted_lab_alloc[k][1]] < 4 and alc[r][i]!=k:
                                    if int(st[x][i][p]) >=1 and int(st[x][i][p]) <=6 :
                                        if a[sorted_lec_c_div[k][1]][int(st[x][i][p])-1] == 0 and a[sorted_lec_c_div[k][1]][int(st[x][i][p])+1] == 0:
                                            #if int(st[x][i][p])==6:
                                                #if a[sorted_lec_c_div[k][1]][int(st[x][i][p])-6] == 0:
                                            break
                                            #else:
                                                #break
                                        else:
                                            continue
                                    
                                    elif int(st[x][i][p])==7:
                                        if a[sorted_lec_c_div[k][1]][int(st[x][i][p])-1] == 0:
                                            #a[sorted_lec_c_div[k][1]][int(st[x][i][p])-6] == 0:
                                            break
                                        else:
                                            continue
                                    elif int(st[x][i][p])==0:
                                        if a[sorted_lec_c_div[k][1]][int(st[x][i][p])+1] == 0:
                                            #a[sorted_lec_c_div[k][1]][int(st[x][i][p])+6] ==0:
                                            break
                                        else:
                                            continue
                                    else:
                                        break

                            if k!=int(len_of_c)-1:
                                #print("k is :",k)
                                ind=int(r)
                                sorted_lec_c_div[k][4]=int(sorted_lec_c_div[k][4])-1
                                theory[x][i][st[x][i][p]]=k
                                print("theory:",x,i,st[x][i][p])
                                print("a:",k)
                                a[sorted_lec_c_div[k][1]][st[x][i][p]]=1
                                new_faculty_hours[sorted_lec_c_div[k][1]] = int(new_faculty_hours[sorted_lec_c_div[k][1]]) + 1
                                alc[r][i] = k
                                break
                            else:
                                counter2=counter2+1
                                print("counter2",counter2)
                                if counter2==20:
                                    k=int(len_of_c)
                                    counter2=0
                                    theory[x][i][st[x][i][p]]=k
                                    print("theory:",x,i,st[x][i][p])
                                    print("a:",k)
                                    break
                                continue
                                #print("inside else part")
                                
                        else:
                            for k in range(0,int(len_of_d)):
                                if x==4 and sorted_lec_c_div[k][2] == sorted_sub_theory[r][0] and a[sorted_lec_c_div[k][1]][st[x][i][p]] == 0 and sorted_lec_c_div[k][4]>=1:
                                    break
                                if sorted_lec_d_div[k][2] == sorted_sub_theory[r][0] and a[sorted_lec_d_div[k][1]][st[x][i][p]] == 0 and sorted_lec_d_div[k][4]>=1 and new_faculty_hours[sorted_lab_alloc[k][1]] < 4 and alc[r][i]!=k:
                                    if int(st[x][i][p]) >=1 and int(st[x][i][p]) <=6 :
                                        if a[sorted_lec_d_div[k][1]][int(st[x][i][p])-1] == 0 and a[sorted_lec_d_div[k][1]][int(st[x][i][p])+1] == 0:
                                            #if int(st[x][i][p])==6:
                                                #if a[sorted_lec_d_div[k][1]][int(st[x][i][p])-6] == 0:
                                            break
                                            #else:
                                                #break
                                        else:
                                            continue
                                    
                                    elif int(st[x][i][p])==7:
                                        if a[sorted_lec_d_div[k][1]][int(st[x][i][p])-1] == 0:
                                            #a[sorted_lec_d_div[k][1]][int(st[x][i][p])-6] == 0:
                                            break
                                        else:
                                            continue
                                    elif int(st[x][i][p])==0:
                                        if a[sorted_lec_d_div[k][1]][int(st[x][i][p])+1] == 0:
                                            #a[sorted_lec_d_div[k][1]][int(st[x][i][p])+6] ==0:
                                            break
                                        else:
                                            continue
                                    else:
                                        break

                            if k!=int(len_of_d)-1:
                                ind=int(r)
                                sorted_lec_d_div[k][4]=int(sorted_lec_d_div[k][4])-1
                                theory[x][i][st[x][i][p]]=k
                                print("theory:",x,i,st[x][i][p])
                                print("a:",k)
                                a[sorted_lec_d_div[k][1]][st[x][i][p]]=1
                                new_faculty_hours[sorted_lec_d_div[k][1]] = int(new_faculty_hours[sorted_lec_d_div[k][1]]) + 1
                                alc[r][i] = k
                                break
                            else:
                                counter2=counter2+1
                                print("counter2",counter2)
                                if counter2==20:
                                    k=int(len_of_d)
                                    counter2=0
                                    theory[x][i][st[x][i][p]]=k
                                    print("theory:",x,i,st[x][i][p])
                                    print("a:",k)
                                    break
                                continue        
        print("practical allocation started")
        #practical allocation
        for i in range(2,6):
            #print("lab allocation")
            for p in range(0,4):
                #print("p : ",p)
                r=0
                k=0
            #print("i:",i)
                m=random.randrange(0,500)
                counter1=0
                counter2=0
                while True:
                    #print("inside while true")
                    
                    #m=m+random.randrange(100)
                    #print("r:",r)
                    if i>=2 and i<4:
                        m=m+1;
                        r=((m)%(int(sizesem4pract)) + int(sizesem4pract))%int(sizesem4pract)
                        #print("r :",r)
                        for k in range(0,total+1):
                            if x==4 and sorted_lab_alloc[k][2]==sorted_sub_practical[r][0] and a[sorted_lab_alloc[k][1]][sp[x][i]]==0 and a[sorted_lab_alloc[k][1]][sp[x][i]+1]==0 and sorted_lab_alloc[k][4]>=2:
                                break
                            if sorted_lab_alloc[k][2]==sorted_sub_practical[r][0] and a[sorted_lab_alloc[k][1]][sp[x][i]]==0 and a[sorted_lab_alloc[k][1]][sp[x][i]+1]==0 and sorted_lab_alloc[k][4]>=2 and alc_lab[r]!=k:
                                if int(sp[x][i]) >= 2 and int(sp[x][i]) <=5:
                                    if a[sorted_lab_alloc[k][1]][int(sp[x][i])-1] != 2 and a[sorted_lab_alloc[k][1]][int(sp[x][i])+2] != 2:
                                        break
                                elif int(sp[x][i]) > 5:
                                    if a[sorted_lab_alloc[k][1]][int(sp[x][i])-1] != 2:
                                        #a[sorted_lab_alloc[k][1]][int(sp[x][i])-6] == 0:
                                        break
                                #elif int(sp[x][i]) <= 1:
                                    #if a[sorted_lab_alloc[k][1]][int(sp[x][i])+6] == 0:
                                        #break
                                else:
                                    break

                        if k==int(total):
                            counter1=counter1+1
                            print("counter1",counter1)
                            if counter1==10:
                                #print("practical subject remaining is sem 4 : ",r)
                                k=total
                                    #print("k1:",k)
                                counter1=0
                                break
                            continue

                    if i>=4 and i<6:
                        m=m+1;
                        r=((m)%(int(sizesem6pract)) + int(sizesem6pract))%int(sizesem6pract)
                        r=r+int(sizesem4pract)
                        #print("r:",r)
                        #print("i :",i)
                        for k in range(0,total+1):
                            if x==4 and sorted_lab_alloc[k][2]==sorted_sub_practical[r][0] and a[sorted_lab_alloc[k][1]][sp[x][i]]==0 and a[sorted_lab_alloc[k][1]][sp[x][i]+1]==0 and sorted_lab_alloc[k][4]>=2:
                                break
                            if sorted_lab_alloc[k][2]==sorted_sub_practical[r][0] and a[sorted_lab_alloc[k][1]][sp[x][i]]==0 and a[sorted_lab_alloc[k][1]][sp[x][i]+1]==0 and sorted_lab_alloc[k][4]>=2 and new_faculty_hours[sorted_lab_alloc[k][1]] < 4 and alc_lab[r]!=k:
                                if int(sp[x][i]) >= 2 and int(sp[x][i]) <=5:
                                    if a[sorted_lab_alloc[k][1]][int(sp[x][i])-1] != 2 and a[sorted_lab_alloc[k][1]][int(sp[x][i])+2] != 2:
                                        break
                                elif int(sp[x][i]) > 5:
                                    if a[sorted_lab_alloc[k][1]][int(sp[x][i])-1] != 2:
                                        #a[sorted_lab_alloc[k][1]][int(sp[x][i])-6] == 0:
                                        break
                                #elif int(sp[x][i]) <= 1:
                                    #if a[sorted_lab_alloc[k][1]][int(sp[x][i])+6] == 0:
                                        #break
                                else:
                                    break

                        if k==(int(total)):
                                #r=r-7
                            counter2=counter2+1
                            print("counter2",counter2)
                            if counter2==10:
                                #print("practical subject remaining is sem 6 : ",r)
                                k=total
                                #print("k1:",k)
                                counter2=0
                                r=r-int(sizesem4pract)
                                break
                            continue
                    r=r-int(sizesem4pract)            
                    if alloc_lab[i][p][r]==0:
                        counter2=0
                        counter1=0
                        break
                alloc_lab[i][p][r]=1
                #print("before for loop")
                #print("total ",total)
                
                #print("outside for loop")
                #print("k2:",k)
                sorted_lab_alloc[k][4]=int(sorted_lab_alloc[k][4])-2
                prac[x][i][p]=k
                alc_lab[r]=k
                print("practical:",x,i,p)
                print("a:",k)
                a[sorted_lab_alloc[k][1]][sp[x][i]]=2
                a[sorted_lab_alloc[k][1]][sp[x][i]+1]=2
                new_faculty_hours[sorted_lab_alloc[k][1]] = int(new_faculty_hours[sorted_lab_alloc[k][1]]) + 2
                #print("hjbchsd")
                #print("outside p loop")
            for p in range(0,sub_practical_len):
                sorted_sub_practical[p][4]=0

        for i in range(1,int(max_id)+1):
            new_faculty_hours[i] = 0
                        
        for i in range(1,total_fac+1):
            for j in range(0,8):
                a[i][j]=0
    #
    not_allocated=[]
    for j in range(0,5):
        for p in range(2,6):
            for q in range(0,4):
                if p>=2 and p<4:
                    for m in range(0,7):
                        if alloc_lab[p][q][m] == 0:
                            break
                    if m!=6:
                        not_allocated.append(m)
                    
                else:
                    for m in range(7,sub_practical_len):
                        if sorted_sub_practical[m][4] == 0:
                            break
    #


    print("remaining theroy subjects : ",remaining_theory)
    print("theory")
    print(" ")
    Sem_4_C.objects.all().delete()
    Sem_4_D.objects.all().delete()
    Sem_6_C.objects.all().delete()
    Sem_6_D.objects.all().delete()
    Monday.objects.all().delete()
    Tuesday.objects.all().delete()
    Wednesday.objects.all().delete()
    Thursday.objects.all().delete()
    Friday.objects.all().delete()
    rooms = ["R1","R2","R3","R4"]
    labs = ["L1","L2","L3","L4","L5","L6","L7","L8"]
    indexofroom = 0
    indexoflab = 0
    for i in range(0,5):
        print("day: %d",i+1)
        print(" ")
        for j in range(2,6):
            if j%2==0:
                if j==2:
                    slot_theory=[]
                    slot_practical=[]
                    for k in range(0,8):
                        sub1=sorted_lec_c_div[theory[i][j][k]][0]+" ( "+sorted_lec_c_div[theory[i][j][k]][2]+" )"
                        if str(sorted_lec_c_div[theory[i][j][k]][0]) != "---":
                            sub1=sub1+" - "+rooms[int(indexofroom)%4]+" "
                        slot_theory.append(sub1)
                    indexofroom = int(indexofroom)+1

                    indexoflab=random.randrange(0,7)
                    for k in range(0,4):
                        subject1=sorted_lab_alloc[prac[i][j][k]][0]+" ( "+sorted_lab_alloc[prac[i][j][k]][2]+" )"
                        subject1=subject1+" - "+labs[int(indexoflab)%8]+" "
                        slot_practical.append(subject1)
                        indexoflab = int(indexoflab)+1
                        #print(sub1)
                        #print("4c div theory[i][j][k]  ",theory[i][j][k])
                        #print("%s { %s }",lec_c_div[theory[i][j][k]][0],lec_c_div[theory[i][j][k]][2])
                    #print("sem 4 c day %d",i+1)
                    #print(slot_theory)
                    four_labs=str(slot_practical[0]+"\n"+slot_practical[1]+"\n"+slot_practical[2]+"\n"+slot_practical[3]+"\n")
                    if sp[int(i)][int(j)]==0:   
                        s=Sem_4_C(slot1=four_labs,slot2=" ",slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==2:
                        s=Sem_4_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=four_labs,slot4=" ",slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==4:
                        s=Sem_4_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=four_labs,slot6=" ",slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    else:
                        s=Sem_4_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=four_labs,slot8=" ")
                        s.save()
                else:
                    slot_theory=[]
                    slot_practical=[]
                    for k in range(0,8):
                        sub1=sorted_lec_c_div[theory[i][j][k]][0]+" ( "+sorted_lec_c_div[theory[i][j][k]][2]+" ) "
                        if str(sorted_lec_c_div[theory[i][j][k]][0]) != "---":
                            sub1=sub1+" - "+rooms[int(indexofroom)%4]+" "
                        slot_theory.append(sub1)
                    indexofroom = int(indexofroom)+1

                    indexoflab=random.randrange(0,7)
                    for k in range(0,4):
                        subject1=sorted_lab_alloc[prac[i][j][k]][0]+" ( "+sorted_lab_alloc[prac[i][j][k]][2]+" )"
                        subject1=subject1+" - "+labs[int(indexoflab)%8]+" "
                        slot_practical.append(subject1)
                        indexoflab = int(indexoflab)+1
                        #print("6c div theory[i][j][k]  ",theory[i][j][k])
                        #print("%s { %s }",lec_c_div[theory[i][j][k]][0],lec_c_div[theory[i][j][k]][2])
                    #print("sem 6 c day %d",i+1)
                    #print(slot_theory)
                    four_labs=str(slot_practical[0]+"\n"+slot_practical[1]+"\n"+slot_practical[2]+"\n"+slot_practical[3]+"\n")
                    if sp[int(i)][int(j)]==0:   
                        s=Sem_6_C(slot1=four_labs,slot2=" ",slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==2:
                        s=Sem_6_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=four_labs,slot4=" ",slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==4:
                        s=Sem_6_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=four_labs,slot6=" ",slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    else:
                        s=Sem_6_C(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=four_labs,slot8=" ")
                        s.save()
                    #print(" ")
            else:
                if j==3:
                    slot_theory=[]
                    slot_practical=[]
                    for k in range(0,8):
                        sub1=sorted_lec_d_div[theory[i][j][k]][0]+" ( "+sorted_lec_d_div[theory[i][j][k]][2]+" )"
                        if str(sorted_lec_c_div[theory[i][j][k]][0]) != "---":
                            sub1=sub1+" - "+rooms[int(indexofroom)%4]+" "
                        slot_theory.append(sub1)
                    indexofroom = int(indexofroom)+1

                    indexoflab=random.randrange(0,7)
                    for k in range(0,4):
                        subject1=sorted_lab_alloc[prac[i][j][k]][0]+" ( "+sorted_lab_alloc[prac[i][j][k]][2]+" )"
                        subject1=subject1+" - "+labs[int(indexoflab)%8]+" "
                        indexoflab = int(indexoflab)+1
                        slot_practical.append(subject1)
                        #print("4d div theory[i][j][k]  ",theory[i][j][k])
                        #print("%s { %s }",lec_d_div[theory[i][j][k]][0],lec_d_div[theory[i][j][k]][2])
                    #print(" ")
                    #print("sem 4 d day %d",i+1)
                    #print(slot_theory)
                    four_labs=str(slot_practical[0]+"\n"+slot_practical[1]+"\n"+slot_practical[2]+"\n"+slot_practical[3]+"\n")
                    if sp[int(i)][int(j)]==0:   
                        s=Sem_4_D(slot1=four_labs,slot2=" ",slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==2:
                        s=Sem_4_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=four_labs,slot4=" ",slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==4:
                        s=Sem_4_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=four_labs,slot6=" ",slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    else:
                        s=Sem_4_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=four_labs,slot8=" ")
                        s.save()
                else:
                    slot_theory=[]
                    slot_practical=[]
                    for k in range(0,8):
                        sub1=sorted_lec_d_div[theory[i][j][k]][0]+" ( "+sorted_lec_d_div[theory[i][j][k]][2]+" )"
                        if str(sorted_lec_c_div[theory[i][j][k]][0]) != "---":
                            sub1=sub1+" - "+rooms[int(indexofroom)%4]+" "
                        slot_theory.append(sub1)
                    indexofroom = int(indexofroom)+1

                    indexoflab=random.randrange(0,7)
                    for k in range(0,4):
                        subject1=sorted_lab_alloc[prac[i][j][k]][0]+" ( "+sorted_lab_alloc[prac[i][j][k]][2]+" )"
                        subject1=subject1+" - "+labs[int(indexoflab)%8]+" "
                        indexoflab = int(indexoflab)+1
                        slot_practical.append(subject1)
                        #print("6d div theory[i][j][k]  ",theory[i][j][k])
                        #print("%s { %s }",lec_d_div[theory[i][j][k]][0],lec_d_div[theory[i][j][k]][2])
                    #print("sem 6 d day %d",i+1)
                    #print(slot_theory)
                    four_labs=str(slot_practical[0]+"\n"+slot_practical[1]+"\n"+slot_practical[2]+"\n"+slot_practical[3]+"\n")
                    if sp[int(i)][int(j)]==0:   
                        s=Sem_6_D(slot1=four_labs,slot2=" ",slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==2:
                        s=Sem_6_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=four_labs,slot4=" ",slot5=slot_theory[4],slot6=slot_theory[5],slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    elif sp[int(i)][int(j)]==4:
                        s=Sem_6_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=four_labs,slot6=" ",slot7=slot_theory[6],slot8=slot_theory[7])
                        s.save()
                    else:
                        s=Sem_6_D(slot1=slot_theory[0],slot2=slot_theory[1],slot3=slot_theory[2],slot4=slot_theory[3],slot5=slot_theory[4],slot6=slot_theory[5],slot7=four_labs,slot8=" ")
                        s.save()
    
    sem4c_data = Sem_4_C.objects.all()
    sem4d_data = Sem_4_D.objects.all()
    sem6c_data = Sem_6_C.objects.all()
    sem6d_data = Sem_6_D.objects.all()

    final4c = []
    final4d = []
    final6c = []
    final6d = []
    for j in sem4c_data:
        l1 = [j.slot1,j.slot2,j.slot3,j.slot4,j.slot5,j.slot6,j.slot7,j.slot8]
        final4c.append(l1)
    for j in sem4d_data:
        l1 = [j.slot1,j.slot2,j.slot3,j.slot4,j.slot5,j.slot6,j.slot7,j.slot8]
        final4d.append(l1)
    for j in sem6c_data:
        l1 = [j.slot1,j.slot2,j.slot3,j.slot4,j.slot5,j.slot6,j.slot7,j.slot8]
        final6c.append(l1)
    for j in sem6d_data:
        l1 = [j.slot1,j.slot2,j.slot3,j.slot4,j.slot5,j.slot6,j.slot7,j.slot8]
        final6d.append(l1)


    for i in range(0,5):
        if i==0:
            s=Monday(slot1=final4c[i][0],slot2=final4c[i][1],slot3=final4c[i][2],slot4=final4c[i][3],slot5=final4c[i][4],slot6=final4c[i][5],slot7=final4c[i][6],slot8=final4c[i][7])
            s.save()
            s=Monday(slot1=final4d[i][0],slot2=final4d[i][1],slot3=final4d[i][2],slot4=final4d[i][3],slot5=final4d[i][4],slot6=final4d[i][5],slot7=final4d[i][6],slot8=final4d[i][7])
            s.save()
            s=Monday(slot1=final6c[i][0],slot2=final6c[i][1],slot3=final6c[i][2],slot4=final6c[i][3],slot5=final6c[i][4],slot6=final6c[i][5],slot7=final6c[i][6],slot8=final6c[i][7])
            s.save()
            s=Monday(slot1=final6d[i][0],slot2=final6d[i][1],slot3=final6d[i][2],slot4=final6d[i][3],slot5=final6d[i][4],slot6=final6d[i][5],slot7=final6d[i][6],slot8=final6d[i][7])
            s.save()
        elif i==1:
            s=Tuesday(slot1=final4c[i][0],slot2=final4c[i][1],slot3=final4c[i][2],slot4=final4c[i][3],slot5=final4c[i][4],slot6=final4c[i][5],slot7=final4c[i][6],slot8=final4c[i][7])
            s.save()
            s=Tuesday(slot1=final4d[i][0],slot2=final4d[i][1],slot3=final4d[i][2],slot4=final4d[i][3],slot5=final4d[i][4],slot6=final4d[i][5],slot7=final4d[i][6],slot8=final4d[i][7])
            s.save()
            s=Tuesday(slot1=final6c[i][0],slot2=final6c[i][1],slot3=final6c[i][2],slot4=final6c[i][3],slot5=final6c[i][4],slot6=final6c[i][5],slot7=final6c[i][6],slot8=final6c[i][7])
            s.save()
            s=Tuesday(slot1=final6d[i][0],slot2=final6d[i][1],slot3=final6d[i][2],slot4=final6d[i][3],slot5=final6d[i][4],slot6=final6d[i][5],slot7=final6d[i][6],slot8=final6d[i][7])
            s.save()
        elif i==2:
            s=Wednesday(slot1=final4c[i][0],slot2=final4c[i][1],slot3=final4c[i][2],slot4=final4c[i][3],slot5=final4c[i][4],slot6=final4c[i][5],slot7=final4c[i][6],slot8=final4c[i][7])
            s.save()
            s=Wednesday(slot1=final4d[i][0],slot2=final4d[i][1],slot3=final4d[i][2],slot4=final4d[i][3],slot5=final4d[i][4],slot6=final4d[i][5],slot7=final4d[i][6],slot8=final4d[i][7])
            s.save()
            s=Wednesday(slot1=final6c[i][0],slot2=final6c[i][1],slot3=final6c[i][2],slot4=final6c[i][3],slot5=final6c[i][4],slot6=final6c[i][5],slot7=final6c[i][6],slot8=final6c[i][7])
            s.save()
            s=Wednesday(slot1=final6d[i][0],slot2=final6d[i][1],slot3=final6d[i][2],slot4=final6d[i][3],slot5=final6d[i][4],slot6=final6d[i][5],slot7=final6d[i][6],slot8=final6d[i][7])
            s.save()
        elif i==3:
            s=Thursday(slot1=final4c[i][0],slot2=final4c[i][1],slot3=final4c[i][2],slot4=final4c[i][3],slot5=final4c[i][4],slot6=final4c[i][5],slot7=final4c[i][6],slot8=final4c[i][7])
            s.save()
            s=Thursday(slot1=final4d[i][0],slot2=final4d[i][1],slot3=final4d[i][2],slot4=final4d[i][3],slot5=final4d[i][4],slot6=final4d[i][5],slot7=final4d[i][6],slot8=final4d[i][7])
            s.save()
            s=Thursday(slot1=final6c[i][0],slot2=final6c[i][1],slot3=final6c[i][2],slot4=final6c[i][3],slot5=final6c[i][4],slot6=final6c[i][5],slot7=final6c[i][6],slot8=final6c[i][7])
            s.save()
            s=Thursday(slot1=final6d[i][0],slot2=final6d[i][1],slot3=final6d[i][2],slot4=final6d[i][3],slot5=final6d[i][4],slot6=final6d[i][5],slot7=final6d[i][6],slot8=final6d[i][7])
            s.save()
        else:
            s=Friday(slot1=final4c[i][0],slot2=final4c[i][1],slot3=final4c[i][2],slot4=final4c[i][3],slot5=final4c[i][4],slot6=final4c[i][5],slot7=final4c[i][6],slot8=final4c[i][7])
            s.save()
            s=Friday(slot1=final4d[i][0],slot2=final4d[i][1],slot3=final4d[i][2],slot4=final4d[i][3],slot5=final4d[i][4],slot6=final4d[i][5],slot7=final4d[i][6],slot8=final4d[i][7])
            s.save()
            s=Friday(slot1=final6c[i][0],slot2=final6c[i][1],slot3=final6c[i][2],slot4=final6c[i][3],slot5=final6c[i][4],slot6=final6c[i][5],slot7=final6c[i][6],slot8=final6c[i][7])
            s.save()
            s=Friday(slot1=final6d[i][0],slot2=final6d[i][1],slot3=final6d[i][2],slot4=final6d[i][3],slot5=final6d[i][4],slot6=final6d[i][5],slot7=final6d[i][6],slot8=final6d[i][7])
            s.save()

    print("4c final  ",final4c)
    print('')
    print("4d final  ",final4d)
    print('')
    print("6c final  ",final6c)
    print('')
    print("6d final  ",final6d)
    print('')
    #for i in range(0,5):

    wb3 = Workbook()
    sheet1 = wb3.add_sheet('MONDAY')
    sheet2 = wb3.add_sheet('TUESDAY')
    sheet3 = wb3.add_sheet('WEDNESDAY')
    sheet4 = wb3.add_sheet('THURSDAY')
    sheet5 = wb3.add_sheet('FRIDAY')
    style1 = easyxf('pattern: pattern solid, fore_colour yellow; align: vert centre, horiz centre')
    text_align_center = easyxf('align: vert centre, horiz centre')
    sheet1.write(0,1,"8:30 to 9:30", style1)
    sheet1.write(0,2,"9:30 to 10:30", style1)
    sheet1.write(0,3,"10:45 to 11:45", style1)
    sheet1.write(0,4,"11:45 to 12:45", style1)
    sheet1.write(0,5,"1:30 to 2:30", style1)
    sheet1.write(0,6,"2:30 to 3:30", style1)
    sheet1.write(0,7,"3:30 to 4:30", style1)
    sheet1.write(0,8,"4:30 to 5:30", style1)
    sheet1.write(1,0,"SEM 4 C DIV", style1)
    sheet1.write(2,0,"SEM 4 D DIV", style1)
    sheet1.write(3,0,"SEM 6 C DIV", style1)
    sheet1.write(4,0,"SEM 6 D DIV", style1)

    sheet2.write(0,1,"8:30 to 9:30", style1)
    sheet2.write(0,2,"9:30 to 10:30", style1)
    sheet2.write(0,3,"10:45 to 11:45", style1)
    sheet2.write(0,4,"11:45 to 12:45", style1)
    sheet2.write(0,5,"1:30 to 2:30", style1)
    sheet2.write(0,6,"2:30 to 3:30", style1)
    sheet2.write(0,7,"3:30 to 4:30", style1)
    sheet2.write(0,8,"4:30 to 5:30", style1)
    sheet2.write(1,0,"SEM 4 C DIV", style1)
    sheet2.write(2,0,"SEM 4 D DIV", style1)
    sheet2.write(3,0,"SEM 6 C DIV", style1)
    sheet2.write(4,0,"SEM 6 D DIV", style1)

    sheet3.write(0,1,"8:30 to 9:30", style1)
    sheet3.write(0,2,"9:30 to 10:30", style1)
    sheet3.write(0,3,"10:45 to 11:45", style1)
    sheet3.write(0,4,"11:45 to 12:45", style1)
    sheet3.write(0,5,"1:30 to 2:30", style1)
    sheet3.write(0,6,"2:30 to 3:30", style1)
    sheet3.write(0,7,"3:30 to 4:30", style1)
    sheet3.write(0,8,"4:30 to 5:30", style1)
    sheet3.write(1,0,"SEM 4 C DIV", style1)
    sheet3.write(2,0,"SEM 4 D DIV", style1)
    sheet3.write(3,0,"SEM 6 C DIV", style1)
    sheet3.write(4,0,"SEM 6 D DIV", style1)

    sheet4.write(0,1,"8:30 to 9:30", style1)
    sheet4.write(0,2,"9:30 to 10:30", style1)
    sheet4.write(0,3,"10:45 to 11:45", style1)
    sheet4.write(0,4,"11:45 to 12:45", style1)
    sheet4.write(0,5,"1:30 to 2:30", style1)
    sheet4.write(0,6,"2:30 to 3:30", style1)
    sheet4.write(0,7,"3:30 to 4:30", style1)
    sheet4.write(0,8,"4:30 to 5:30", style1)
    sheet4.write(1,0,"SEM 4 C DIV", style1)
    sheet4.write(2,0,"SEM 4 D DIV", style1)
    sheet4.write(3,0,"SEM 6 C DIV", style1)
    sheet4.write(4,0,"SEM 6 D DIV", style1)

    sheet5.write(0,1,"8:30 to 9:30", style1)
    sheet5.write(0,2,"9:30 to 10:30", style1)
    sheet5.write(0,3,"10:45 to 11:45", style1)
    sheet5.write(0,4,"11:45 to 12:45", style1)
    sheet5.write(0,5,"1:30 to 2:30", style1)
    sheet5.write(0,6,"2:30 to 3:30", style1)
    sheet5.write(0,7,"3:30 to 4:30", style1)
    sheet5.write(0,8,"4:30 to 5:30", style1)
    sheet5.write(1,0,"SEM 4 C DIV", style1)
    sheet5.write(2,0,"SEM 4 D DIV", style1)
    sheet5.write(3,0,"SEM 6 C DIV", style1)
    sheet5.write(4,0,"SEM 6 D DIV", style1)


    for j in range(1,9):
        sheet1.col(j).width = 5000
        sheet1.row(j).height = 3000
        sheet2.col(j).width = 5000
        sheet2.row(j).height = 3000
        sheet3.col(j).width = 5000
        sheet3.row(j).height = 3000
        sheet4.col(j).width = 5000
        sheet4.row(j).height = 3000
        sheet5.row(j).height = 3000
        sheet5.col(j).width = 5000

    day1 = Monday.objects.all()
    day2 = Tuesday.objects.all()
    day3 = Wednesday.objects.all()
    day4 = Thursday.objects.all()
    day5 = Friday.objects.all()

    finalday1 = []
    finalday2 = []
    finalday3 = []
    finalday4 = []
    finalday5 = []

    for i in day1:
        l1 = [i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        finalday1.append(l1)

    for i in day2:
        l1 = [i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        finalday2.append(l1)

    for i in day3:
        l1 = [i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        finalday3.append(l1)

    for i in day4:
        l1 = [i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        finalday4.append(l1)

    for i in day5:
        l1 = [i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        finalday5.append(l1)

    for r in range(1,5):
        sheet1.write(r,1,finalday1[int(r)-1][0],text_align_center)
        sheet1.write(r,2,finalday1[int(r)-1][1],text_align_center)
        sheet1.write(r,3,finalday1[int(r)-1][2],text_align_center)
        sheet1.write(r,4,finalday1[int(r)-1][3],text_align_center)
        sheet1.write(r,5,finalday1[int(r)-1][4],text_align_center)
        sheet1.write(r,6,finalday1[int(r)-1][5],text_align_center)
        sheet1.write(r,7,finalday1[int(r)-1][6],text_align_center)
        sheet1.write(r,8,finalday1[int(r)-1][7],text_align_center)

    for r in range(1,5):
        sheet2.write(r,1,finalday2[int(r)-1][0],text_align_center)
        sheet2.write(r,2,finalday2[int(r)-1][1],text_align_center)
        sheet2.write(r,3,finalday2[int(r)-1][2],text_align_center)
        sheet2.write(r,4,finalday2[int(r)-1][3],text_align_center)
        sheet2.write(r,5,finalday2[int(r)-1][4],text_align_center)
        sheet2.write(r,6,finalday2[int(r)-1][5],text_align_center)
        sheet2.write(r,7,finalday2[int(r)-1][6],text_align_center)
        sheet2.write(r,8,finalday2[int(r)-1][7],text_align_center)

    for r in range(1,5):
        sheet3.write(r,1,finalday3[int(r)-1][0],text_align_center)
        sheet3.write(r,2,finalday3[int(r)-1][1],text_align_center)
        sheet3.write(r,3,finalday3[int(r)-1][2],text_align_center)
        sheet3.write(r,4,finalday3[int(r)-1][3],text_align_center)
        sheet3.write(r,5,finalday3[int(r)-1][4],text_align_center)
        sheet3.write(r,6,finalday3[int(r)-1][5],text_align_center)
        sheet3.write(r,7,finalday3[int(r)-1][6],text_align_center)
        sheet3.write(r,8,finalday3[int(r)-1][7],text_align_center)

    for r in range(1,5):
        sheet4.write(r,1,finalday4[int(r)-1][0],text_align_center)
        sheet4.write(r,2,finalday4[int(r)-1][1],text_align_center)
        sheet4.write(r,3,finalday4[int(r)-1][2],text_align_center)
        sheet4.write(r,4,finalday4[int(r)-1][3],text_align_center)
        sheet4.write(r,5,finalday4[int(r)-1][4],text_align_center)
        sheet4.write(r,6,finalday4[int(r)-1][5],text_align_center)
        sheet4.write(r,7,finalday4[int(r)-1][6],text_align_center)
        sheet4.write(r,8,finalday4[int(r)-1][7],text_align_center)

    for r in range(1,5):
        sheet5.write(r,1,finalday5[int(r)-1][0],text_align_center)
        sheet5.write(r,2,finalday5[int(r)-1][1],text_align_center)
        sheet5.write(r,3,finalday5[int(r)-1][2],text_align_center)
        sheet5.write(r,4,finalday5[int(r)-1][3],text_align_center)
        sheet5.write(r,5,finalday5[int(r)-1][4],text_align_center)
        sheet5.write(r,6,finalday5[int(r)-1][5],text_align_center)
        sheet5.write(r,7,finalday5[int(r)-1][6],text_align_center)
        sheet5.write(r,8,finalday5[int(r)-1][7],text_align_center)

    wb3.save('DAYWISE.xls')

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet2 = wb.add_sheet('Sheet 2')
    sheet3 = wb.add_sheet('Sheet 3')
    sheet4 = wb.add_sheet('Sheet 4')
    style1 = easyxf('pattern: pattern solid, fore_colour yellow; align: vert centre, horiz centre')
    text_align_center = easyxf('align: vert centre, horiz centre')
    sheet1.write(0,1,"8:30 to 9:30", style1)
    sheet1.write(0,2,"9:30 to 10:30", style1)
    sheet1.write(0,3,"10:45 to 11:45", style1)
    sheet1.write(0,4,"11:45 to 12:45", style1)
    sheet1.write(0,5,"1:30 to 2:30", style1)
    sheet1.write(0,6,"2:30 to 3:30", style1)
    sheet1.write(0,7,"3:30 to 4:30", style1)
    sheet1.write(0,8,"4:30 to 5:30", style1)
    sheet1.write(1,0,"Mon", style1)
    sheet1.write(2,0,"Tue", style1)
    sheet1.write(3,0,"Wed", style1)
    sheet1.write(4,0,"Thu", style1)
    sheet1.write(5,0,"Fri", style1)

    sheet2.write(0,1,"8:30 to 9:30", style1)
    sheet2.write(0,2,"9:30 to 10:30", style1)
    sheet2.write(0,3,"10:45 to 11:45", style1)
    sheet2.write(0,4,"11:45 to 12:45", style1)
    sheet2.write(0,5,"1:30 to 2:30", style1)
    sheet2.write(0,6,"2:30 to 3:30", style1)
    sheet2.write(0,7,"3:30 to 4:30", style1)
    sheet2.write(0,8,"4:30 to 5:30", style1)
    sheet2.write(1,0,"Mon", style1)
    sheet2.write(2,0,"Tue", style1)
    sheet2.write(3,0,"Wed", style1)
    sheet2.write(4,0,"Thu", style1)
    sheet2.write(5,0,"Fri", style1)

    sheet3.write(0,1,"8:30 to 9:30", style1)
    sheet3.write(0,2,"9:30 to 10:30", style1)
    sheet3.write(0,3,"10:45 to 11:45", style1)
    sheet3.write(0,4,"11:45 to 12:45", style1)
    sheet3.write(0,5,"1:30 to 2:30", style1)
    sheet3.write(0,6,"2:30 to 3:30", style1)
    sheet3.write(0,7,"3:30 to 4:30", style1)
    sheet3.write(0,8,"4:30 to 5:30", style1)
    sheet3.write(1,0,"Mon", style1)
    sheet3.write(2,0,"Tue", style1)
    sheet3.write(3,0,"Wed", style1)
    sheet3.write(4,0,"Thu", style1)
    sheet3.write(5,0,"Fri", style1)

    sheet4.write(0,1,"8:30 to 9:30", style1)
    sheet4.write(0,2,"9:30 to 10:30", style1)
    sheet4.write(0,3,"10:45 to 11:45", style1)
    sheet4.write(0,4,"11:45 to 12:45", style1)
    sheet4.write(0,5,"1:30 to 2:30", style1)
    sheet4.write(0,6,"2:30 to 3:30", style1)
    sheet4.write(0,7,"3:30 to 4:30", style1)
    sheet4.write(0,8,"4:30 to 5:30", style1)
    sheet4.write(1,0,"Mon", style1)
    sheet4.write(2,0,"Tue", style1)
    sheet4.write(3,0,"Wed", style1)
    sheet4.write(4,0,"Thu", style1)
    sheet4.write(5,0,"Fri", style1)

    for j in range(1,9):
        sheet1.col(j).width = 5000
        sheet1.row(j).height = 3000
        sheet2.col(j).width = 5000
        sheet2.row(j).height = 3000
        sheet3.col(j).width = 5000
        sheet3.row(j).height = 3000
        sheet4.col(j).width = 5000
        sheet4.row(j).height = 3000

    t1=Sem_4_C.objects.all()
    t2=Sem_4_D.objects.all()
    t3=Sem_6_C.objects.all()
    t4=Sem_6_D.objects.all()
    all_sub1=[]
    all_sub2=[]
    all_sub3=[]
    all_sub4=[]
    for i in t1:
        l1=[i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        all_sub1.append(l1)
    
    for r in range(1,6):
        sheet1.write(r,1,all_sub1[int(r)-1][0],text_align_center)
        sheet1.write(r,2,all_sub1[int(r)-1][1],text_align_center)
        sheet1.write(r,3,all_sub1[int(r)-1][2],text_align_center)
        sheet1.write(r,4,all_sub1[int(r)-1][3],text_align_center)
        sheet1.write(r,5,all_sub1[int(r)-1][4],text_align_center)
        sheet1.write(r,6,all_sub1[int(r)-1][5],text_align_center)
        sheet1.write(r,7,all_sub1[int(r)-1][6],text_align_center)
        sheet1.write(r,8,all_sub1[int(r)-1][7],text_align_center)

    for i in t2:
        l1=[i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        all_sub2.append(l1)
    
    for r in range(1,6):
        sheet2.write(r,1,all_sub2[int(r)-1][0],text_align_center)
        sheet2.write(r,2,all_sub2[int(r)-1][1],text_align_center)
        sheet2.write(r,3,all_sub2[int(r)-1][2],text_align_center)
        sheet2.write(r,4,all_sub2[int(r)-1][3],text_align_center)
        sheet2.write(r,5,all_sub2[int(r)-1][4],text_align_center)
        sheet2.write(r,6,all_sub2[int(r)-1][5],text_align_center)
        sheet2.write(r,7,all_sub2[int(r)-1][6],text_align_center)
        sheet2.write(r,8,all_sub2[int(r)-1][7],text_align_center)

    for i in t3:
        l1=[i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        all_sub3.append(l1)
    
    for r in range(1,6):
        sheet3.write(r,1,all_sub3[int(r)-1][0],text_align_center)
        sheet3.write(r,2,all_sub3[int(r)-1][1],text_align_center)
        sheet3.write(r,3,all_sub3[int(r)-1][2],text_align_center)
        sheet3.write(r,4,all_sub3[int(r)-1][3],text_align_center)
        sheet3.write(r,5,all_sub3[int(r)-1][4],text_align_center)
        sheet3.write(r,6,all_sub3[int(r)-1][5],text_align_center)
        sheet3.write(r,7,all_sub3[int(r)-1][6],text_align_center)
        sheet3.write(r,8,all_sub3[int(r)-1][7],text_align_center)

    for i in t4:
        l1=[i.slot1,i.slot2,i.slot3,i.slot4,i.slot5,i.slot6,i.slot7,i.slot8]
        all_sub4.append(l1)
    
    for r in range(1,6):
        sheet4.write(r,1,all_sub4[int(r)-1][0],text_align_center)
        sheet4.write(r,2,all_sub4[int(r)-1][1],text_align_center)
        sheet4.write(r,3,all_sub4[int(r)-1][2],text_align_center)
        sheet4.write(r,4,all_sub4[int(r)-1][3],text_align_center)
        sheet4.write(r,5,all_sub4[int(r)-1][4],text_align_center)
        sheet4.write(r,6,all_sub4[int(r)-1][5],text_align_center)
        sheet4.write(r,7,all_sub4[int(r)-1][6],text_align_center)
        sheet4.write(r,8,all_sub4[int(r)-1][7],text_align_center)

    wb.save('TimeTable.xls')
    wb2 = Workbook()
    sh1 = wb2.add_sheet("sheet1")
    sh1.col(0).width = 7000
    sh1.write(0,0,"Theory",style1)
    #print("theory")
    #print("")
    mycounter = 2
    for i in range(0,len(sorted_sub_theory)):
        for j in range(0,len(sorted_lec_c_div)):
            if sorted_sub_theory[i][0] == sorted_lec_c_div[j][2]:
                if sorted_lec_c_div[j][4] > 0:
                    cell_value = "c division "+str(sorted_lec_c_div[j][0])+" : "+str(sorted_lec_c_div[j][2])+" : "+str(sorted_lec_c_div[j][4])+" "
                    sh1.write(mycounter,0,cell_value,text_align_center)
                    mycounter = int(mycounter) + 1
                    #print("c division  ",sorted_lec_c_div[j][0]," : ",sorted_lec_c_div[j][2]," : ",sorted_lec_c_div[j][4])
                    #print("")
        for l in range(0,len(sorted_lec_d_div)):
            if sorted_sub_theory[i][0] == sorted_lec_d_div[l][2]:
                if sorted_lec_d_div[l][4] > 0:
                    cell_value = "d division "+str(sorted_lec_d_div[l][0])+" : "+str(sorted_lec_d_div[l][2])+" : "+str(sorted_lec_d_div[l][4])+" "
                    sh1.write(mycounter,0,cell_value,text_align_center)
                    mycounter = int(mycounter) + 1
                    #print("d division  ",sorted_lec_d_div[l][0]," : ",sorted_lec_d_div[l][2]," : ",sorted_lec_d_div[l][4])
                    #print("")
    sh1.write(int(mycounter)+1,0,"Practical",style1)
    mycounter = int(mycounter) + 3
    #print("practical")
    #print("")
    for i in range(0,len(sorted_lab_alloc)):
        if sorted_lab_alloc[i][4] > 0 and sorted_lab_alloc[i][0] != " ":
            cell_value = "lab "+str(sorted_lab_alloc[i][0])+" : "+str(sorted_lab_alloc[i][2])+" : "+str(sorted_lab_alloc[i][4])+" "
            sh1.write(mycounter,0,cell_value,text_align_center)
            mycounter = int(mycounter) + 1
            #print(sorted_lab_alloc[i][0]," : ",sorted_lab_alloc[i][2]," : ",sorted_lab_alloc[i][4])
            #print("")

    wb2.save("Remaining Hours.xls")
    '''for i in range(0,len(lec_c_div)):
        print(lec_c_div[i])
        print("")
    for i in range(0,len(lec_d_div)):
        print(lec_d_div[i])
        print("")
    print("practical")
    for i in range(0,len(lab_alloc)):
        print(lab_alloc[i])
        print("")'''


    '''sem4_timetable = Sem_4_C_Timetable()
    sem4 = sem4_timetable.export()
    response = HttpResponse(sem4.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sem4C.xls"'
    print(response)

    sem4_timetable = Sem_4_D_Timetable()
    sem4 = sem4_timetable.export()
    response = HttpResponse(sem4.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sem4D.xls"'
    print(response)

    sem6_timetable = Sem_6_C_Timetable()
    sem6 = sem4_timetable.export()
    response = HttpResponse(sem4.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sem6C.xls"'
    print(response)

    sem6_timetable = Sem_6_D_Timetable()
    sem6 = sem6_timetable.export()
    response = HttpResponse(sem4.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sem6D.xls"'
    print(response)

                #print(" ")      
    slot_practical=[]
    print(" ")
    print("practical")
    print(" ")
    Sem_4_C_lab.objects.all().delete()
    Sem_4_D_lab.objects.all().delete()
    Sem_6_C_lab.objects.all().delete()
    Sem_6_D_lab.objects.all().delete()
    for i in range(0,5):
        print("day: %d",i+1)
        print(" ")
        for j in range(2,6):
            #print("Lab:")
            #print(" ")
            if j==2:
                slot_practical=[]
                for k in range(0,4):
                    subject1=lab_alloc[prac[i][j][k]][0]+" ( "+lab_alloc[prac[i][j][k]][2]+" )"
                    slot_practical.append(subject1)
                s=Sem_4_C_lab(batch1=slot_practical[0],batch2=slot_practical[1],batch3=slot_practical[2],batch4=slot_practical[3])
                s.save()
            elif j==3:
                slot_practical=[]
                for k in range(0,4):
                    subject1=lab_alloc[prac[i][j][k]][0]+" ( "+lab_alloc[prac[i][j][k]][2]+" )"
                    slot_practical.append(subject1)
                s=Sem_4_D_lab(batch1=slot_practical[0],batch2=slot_practical[1],batch3=slot_practical[2],batch4=slot_practical[3])
                s.save()
            elif j==4:
                slot_practical=[]
                for k in range(0,4):
                    subject1=lab_alloc[prac[i][j][k]][0]+" ( "+lab_alloc[prac[i][j][k]][2]+" )"
                    slot_practical.append(subject1)
                s=Sem_6_C_lab(batch1=slot_practical[0],batch2=slot_practical[1],batch3=slot_practical[2],batch4=slot_practical[3])
                s.save()
            else:
                slot_practical=[]
                for k in range(0,4):
                    subject1=lab_alloc[prac[i][j][k]][0]+" ( "+lab_alloc[prac[i][j][k]][2]+" )"
                    slot_practical.append(subject1)
                s=Sem_6_D_lab(batch1=slot_practical[0],batch2=slot_practical[1],batch3=slot_practical[2],batch4=slot_practical[3])
                s.save()
            #print(" ")'''        
    return render_to_response('home.html',c)




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
