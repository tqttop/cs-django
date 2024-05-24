from django.urls import path
from app01 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('sendVerifycode/', views.SendVerifyCode.as_view(), name='sendVerifycode'),
                  path('register/', views.RegisterView.as_view(), name='register'),
                  path('login/', views.LoginView.as_view(), name='login'),
                  path('userList/', views.UserListView.as_view(), name='userList'),
                  path('banList/', views.BanlistView.as_view(), name='banList'),
                  path('search/', views.SearchView.as_view(), name='search'),
                  path('change/name/', views.ChangeNameView.as_view(), name='changeName'),
                  path('change/password/', views.ChangePasswordView.as_view(), name='changePassword'),
                  path('change/img/', views.UploadImgView.as_view(), name='changeImg'),
                  path('documents/', views.DocumentView.as_view(), name='documents'),
                  path('videos/<str:pk>/', views.getVideos),
                  path('ArticleDetail/', views.ArticleDetailView.as_view(), name='ArticleDetail'),
                  path('ArticleLike/',views.ArticleLikeView.as_view(),name='ArticleLike'),
                  path('Comment/', views.CommentView.as_view(), name='Comment'),
                  path('Article/', views.ArticleView.as_view(), name='Article'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
