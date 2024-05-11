from django.shortcuts import render
from register.models import CustomUser
from blog.models import post
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
# credentials = flow.run_console()
start_time =0
end_time=0
  
scopes = ['https://www.googleapis.com/auth/calendar']

credentials = pickle.load(open("token.pkl","rb"))
# Create your views here.
@login_required
def doctors(request):

    
    b = CustomUser.objects.filter( is_doctor=1)
    return render(request,"doctors.html",{"doctors":b})
@login_required
def bookform(request,pk):
    form = CustomUser.objects.get(id=pk)
    if request.method == 'POST':
        form = CustomUser.objects.get(id=pk)
        req = request.POST['req']
        start = request.POST['start']
        time = request.POST['time']
        email = request.POST['email']
        starts = start +' '+ time +':' '00'

        start_time = datetime.datetime.strptime(starts,"%Y-%m-%d %H:%M:%S")
        end_time  = start_time + timedelta(minutes=45)
        context = { 'req':req,'start':start,'time':time,'start_time':start_time, 'end_time':end_time,'email':email,'form':form}
        return  render(request, 'confirm.html',context)
    return render(request,'bookform.html',{'form':form})
@login_required
def confirm(request):
    service = build("calendar", "v3", credentials=credentials)
    if request.method == 'POST':
        req = request.POST['required']
        start = request.POST['starts']
        time = request.POST['time']
        email = request.POST['email']
        start = start +' '+ time +':' '00'
        start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
        end_time  = start_time + timedelta(minutes=45)
        timezone = 'Asia/Kolkata'
        print("Gsfgfd",start_time.isoformat(),'vdfdf',end_time.isoformat())
        print("dsdv",req)
        print("Gfdg",email),
        start_time_2 = start_time + timedelta(minutes=30,hours=5)
        end_time_2 = end_time + timedelta(minutes=30,hours=5)
        event = (
        service.events()
        .insert(
            calendarId="primary",
            body={
                    "summary": req,
                    "start": {"dateTime": start_time_2.isoformat(),'timeZone': timezone,},
                    "end": {"dateTime": end_time_2.isoformat(),'timeZone': timezone,},
                    "attendees":[{"email":email}]
                },
              )
        .execute()
         )
        return redirect('register:home')
    return render(request,'confirm.html')
@login_required
def viewevent(request):
    service = build("calendar", "v3", credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

        # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        email = event['attendees'][0:]
        print(start,email)

    return render(request,'viewevent.html',{'form':start})