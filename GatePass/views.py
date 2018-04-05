from django.shortcuts import render
import pyrebase
from django.contrib import auth


config = {
    "apiKey": "AIzaSyA1ICSW1mhNu4eOHi94YZgmbD6T2AUxOhg",
    "authDomain": "gatepassfirebasesaurabh.firebaseapp.com",
    "databaseURL": "https://gatepassfirebasesaurabh.firebaseio.com",
    "projectId": "gatepassfirebasesaurabh",
    "storageBucket": "gatepassfirebasesaurabh.appspot.com",
    "messagingSenderId": "729609868972",
  }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def singIn(request):
    return render(request, "signin.html")

def postsign(request):
    # import datetime

    # idtoken = request.session['uid']
    # # print(idtoken)
    # a = authe.get_account_info(idtoken)
    # print(a)
    # a = a['users']
    # a = a[0]
    # a = a['localId']

    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"signin.html",{"msg":message})
    # print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    # name = database.child("students").child(a).child("name").get().val()
    return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,"signin.html")

def signUp(request):
    return render(request,"signup.html")

def postsignup(request):
    name=request.POST.get('name')
    college_id=request.POST.get('college_id')
    mobile_no_father=request.POST.get('mobile_no_father')
    mobile_no_mother=request.POST.get('mobile_no_mother')
    mobile_no_self=request.POST.get('mobile_no_self')
    room_no=request.POST.get('room_no')
    semester=request.POST.get('semester')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    # try:
    user=authe.create_user_with_email_and_password(email,passw)
    # except:
    # message="Unable to create account, Try Again"
    # return render(request,"signin.html",{"messg":message})
    uid = user['localId']
    data={"name":name,
        "college_id":college_id,
        "mobile_no_father":mobile_no_father,
        "mobile_no_mother":mobile_no_mother,
        "mobile_no_self":mobile_no_self,
        "room_no":room_no,
        "semester":semester,
        "status":"1"}
    database.child("students").child(uid).set(data)
    return render(request,"signin.html")

def normal(request):
    return render(request,"normal.html")

def normalCreate(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    print(tz)
    time_now = datetime.now(timezone.utc).astimezone(tz)
    print(time_now)
    millis = int(time.mktime(time_now.timetuple()))
    print(time_now.timetuple())
    print(time.mktime(time_now.timetuple()))
    print(millis)

    i = float(millis)

    dt = datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    print(dt)
    print(type(dt))

    date_of_going=request.POST.get('date_of_going')
    reason=request.POST.get('reason')
    time_in=request.POST.get('time_in')
    time_out=request.POST.get('time_out')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    # print(str(a))
    data={"date_of_going":date_of_going,
        "reason":reason,
        "time_in":time_in,
        "time_out":time_out,
        "status":"Pending",
        "time_of_applying":dt
        }
    database.child("normal").child(a).child(millis).set(data)
    # database.child("normal").child(a).set(data)
    return render(request,"welcome.html")

def normalView(request):
    import datetime

    idtoken = request.session['uid']
    # print(idtoken)
    a = authe.get_account_info(idtoken)
    print(a)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('normal').child(a).shallow().get().val()
    list_time = []
    for i in timestamps:
        list_time.append(i)
    list_time.sort(reverse=True)
    # print(list_time) # seconds id

    date_list = []
    status_list = []
    for i in list_time:
        dat = database.child("normal").child(a).child(i).child("date_of_going").get().val()
        date_list.append(dat)
        statu = database.child("normal").child(a).child(i).child("status").get().val()
        status_list.append(statu)
    # print(date_list) # Date of going
    # print(status_list)

    date_time = []
    for i in list_time:
        i = float(i)
        dt = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date_time.append(dt)
    # print(date_time) # date time

    combined_list = zip(list_time,date_time,date_list,status_list)
    name = database.child("students").child(a).child("name").get().val()
    return render(request,"view_normal.html",{"combined_list":combined_list,
                                                "e":name
                                                })

def postNormalView(request):
    import datetime

    t = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    date_of_going = database.child("normal").child(a).child(t).child("date_of_going").get().val()
    reason = database.child("normal").child(a).child(t).child("reason").get().val()
    status = database.child("normal").child(a).child(t).child("status").get().val()
    time_in = database.child("normal").child(a).child(t).child("time_in").get().val()
    time_out = database.child("normal").child(a).child(t).child("time_out").get().val()

    i = float(t)

    dt = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child("students").child(a).child("name").get().val()

    if status == "Approved":
        return render(request,"post_view_normal_approved.html",{"d":date_of_going,
                                                    "r":reason,
                                                    "s":status,
                                                    "ti":time_in,
                                                    "to":time_out,
                                                    "dt":dt,
                                                    "e":name})
    elif status == "Rejected":
        return render(request,"post_view_normal_rejected.html",{"d":date_of_going,
                                                    "r":reason,
                                                    "s":status,
                                                    "ti":time_in,
                                                    "to":time_out,
                                                    "dt":dt,
                                                    "e":name})
    else:
        return render(request,"post_view_normal.html",{"d":date_of_going,
                                                    "r":reason,
                                                    "s":status,
                                                    "ti":time_in,
                                                    "to":time_out,
                                                    "dt":dt,
                                                    "e":name})
