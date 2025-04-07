from django.urls import path
from .views import HomeView, QuestionDetailView, AskQuestionView, EditQuestionView, DeleteQuestionView, EditAnswerView, DeleteAnswerView, LikeAnswerView, SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/edit/', EditQuestionView.as_view(), name='edit_question'),
    path('question/<int:pk>/delete/', DeleteQuestionView.as_view(), name='delete_question'),
    path('answer/<int:pk>/edit/', EditAnswerView.as_view(), name='edit_answer'),
    path('answer/<int:pk>/delete/', DeleteAnswerView.as_view(), name='delete_answer'),
    path('answer/<int:pk>/like/', LikeAnswerView.as_view(), name='like_answer'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]