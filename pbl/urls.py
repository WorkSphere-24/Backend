
from django.contrib import admin
from django.urls import path,include
from app import views 
from app.views import CustomLoginView,CustomLoginAPIView
from rest_framework.routers import DefaultRouter
from django.conf import settings 
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

router=DefaultRouter()

router.register('task',views.TaskViewSet,basename='task')
router.register('priority',views.PriorityViewSet,basename="priority")
router.register('status',views.StatusViewSet,basename="status")
router.register('team',views.TeamViewSet,basename = 'team')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up',views.sign_up,name='sign_up'),
    # path('login',views.user_login,name='login'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.user_logout,name='logout'),
    path('changepass',views.user_change_pass,name='changepass'),
    path('userdetail/<int:id>',views.user_detail,name='userdetail'),
    path('api',include(router.urls)),
    path('get_team',views.get_team,name = "get_team"),
    path('users',views.list_users,name ='list_users')
]
# for url_pattern in urlpatterns:
#     url_pattern.callback = csrf_exempt(url_pattern.callback)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)