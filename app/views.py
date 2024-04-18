from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,AuthenticationForm,PasswordChangeForm
from .forms import SignUpForm,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth  import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User,Group
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .permissions import JWTAuthentication
import jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import CustomLoginSerializer,TaskSerializer,PrioritySerializer,StatusSerializer,TeamSerializer

from rest_framework import viewsets,permissions
from .models import Task,CustomUser,Priority,Status,Team,Chat


def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,"Account Created Successfully")
            fm.save()
    else:
        fm=SignUpForm
    return render(request,'signup.html',{'form':fm})

def index(request,group_name):
    print("Group name...",group_name)
    group = Group.objects.filter(name = group_name).first()
    chats=[]
    if group:
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
    return render(request,'index.html',{'groupname':group_name,'chats':chats})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('profile')
    else:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect("profile")
        fm = AuthenticationForm()
        return render(request,'userlogin.html',{'form':fm})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('login')


def profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            if request.user.is_superuser:
                fm = EditAdminProfileForm(request.POST,instance=request.user)
                users=User.objects.all()
            else:
                fm=EditUserProfileForm(request.POST,instance=request.user)
                users=None
            if fm.is_valid():
                messages.success(request,"Profile Updated")
                fm.save()
        else:
           if request.user.is_superuser:
               fm=EditAdminProfileForm(instance=request.user)
               users=User.objects.all()
           else:
                fm=EditUserProfileForm(instance=request.user)
                users=User.objects.all()
        return render(request,'profile.html',{'name':request.user,'form':fm,'users':users})
    else:
        return HttpResponseRedirect('login')
    
def user_change_pass(request):
    if request.user.is_authenticated :
        if request.method=="POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'Password Changed Successfully')
                return HttpResponseRedirect('profile')
        else:
            fm=PasswordChangeForm(user=request.user)
        return render(request,'changepass.html',{'form':fm})
    else:
        return HttpResponseRedirect('login')
    
def user_detail(request,id):
    if request.user.is_authenticated:
        pi=User.objects.get(pk=id)
        fm=EditAdminProfileForm(instance=id)
        return render(request,'userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('login')
    

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class= CustomLoginForm
    success_url=reverse_lazy('profile')

class CustomLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        print("serializer  ",serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')
            print(email)
            print(password)
            user = authenticate(request,email=email,password=password)
            print("user  ",user)
            if user:
                login(request, user)
                # email = user.name
                # token, created = Token.objects.get_or_create(user=user)
                payload = {
                'email' :email
                }
                #Generating Token and storing in COOKIE
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {'jwt': token,'email':email}
                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = []
    def get_queryset(self):
        token = self.request.COOKIES.get("jwt")
        print(token)
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        print("abcd",payload)
        email = payload["email"]
        print("abcd",email)
        user = CustomUser.objects.get(email = email)
        print(user)
        team_id = Team.objects.get(members = user)
        print(team_id)
        queryset = Task.objects.all()
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [permissions.IsAuthenticated]

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]

# class TeamviewSet(viewsets.MOdelViewSet):
#     queryset = 

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes =[permissions.IsAuthenticated]


def tid(request):
    token = request.COOKIES.get("jwt")
    print(token)
    payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    print("abcd",payload)
    email = payload["email"]
    print("abcd",email)
    user = CustomUser.objects.get(email = email)
    print(user)
    team_id = Team.objects.get(members = user)
    print(team_id)
    return team_id

def get_team(request):
    team_id = tid(request)
    return HttpResponseRedirect(f"apitask/?team_id = {team_id}")


def list_users(request):
    token = request.COOKIES.get("jwt")
    queryset = CustomUser.objects.all()
    # print("heelo")
    print(queryset)
    return HttpResponseRedirect('api')