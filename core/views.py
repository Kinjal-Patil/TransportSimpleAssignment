from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm, SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

class HomeView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'home.html'
    context_object_name = 'questions'
    login_url = '/accounts/login/'

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'question_detail.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.object)
        context['form'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
        return redirect('question_detail', pk=question.pk)

class AskQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'ask_question.html'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditQuestionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'edit_question.html'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user

class DeleteQuestionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'delete_question_confirm.html'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'

    def test_func(self):
        return self.request.user == self.get_object().user

class EditAnswerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'edit_answer.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})

    def test_func(self):
        return self.request.user == self.get_object().user

class DeleteAnswerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'delete_answer_confirm.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})

    def test_func(self):
        return self.request.user == self.get_object().user

class LikeAnswerView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        Like.objects.get_or_create(user=request.user, answer=answer)
        return redirect('question_detail', pk=answer.question.pk)

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')