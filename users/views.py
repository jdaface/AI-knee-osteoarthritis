from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.views.generic import TemplateView
from django.template.context import RequestContext
from users.forms import (
    UserRegForm,
    DoctorRegForm,
    DoctorLoginForm,
    PatientRegForm,
    PatientLoginForm,
    CommentForm,
    QuestionaireForm,
)
from users.models import Patient
# Create your views here.
def docReg(request):
    user_form_class = UserRegForm
    doc_form_class = DoctorRegForm
    user_form = user_form_class(request.POST or None)
    doc_form = doc_form_class(request.POST or None)

    if request.method == "POST":

        if user_form.is_valid() and doc_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            user.doctor.email = doc_form.clean_data.get("email")
            user.doctor.hpname = doc_form.clean_data.get("hpname")
            user.doctor.specialty = doc_form.clean_data.get("specialty")
            user.doctor.password1 = doc_form.clean_data.get("password1")
            user.doctor.password2 = doc_form.clean_data.get("password2")
            user.doctor.save()

        else:
            user_form = UserRegForm(prefix="UF")
            doc_form = DoctorRegForm(prefix="DF")


    return render(
        request,
        "registration/d_reg.html",
        {"user_form": user_form, "doc_form": doc_form, },
    )


def patReg(request):
    form_class = PatientRegForm
    form = form_class(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            user = form.save(commit=False)

            user.patient.email = form.clean_data.get("email")
            user.patient.fullname = form.clean_data.get("fullname")
            user.patient.phonenumber = form.clean_data.get("phonenumber")
            user.patient.birthday = form.clean_data.get("birthday")
            user.patient.gender = form.clean_data.get("gender")

            user.patient.save()

        else:
            form = PatientRegForm(prefix="PF")
    
    return render(request, "registration/p_reg.html", {"form": form, })


def docLogin(request):
    form_class = DoctorLoginForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = request.POST.get("email")  # Get email value from form
            # Get password value from form
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_authenticated and user.is_doctor:
                    return HttpResponseRedirect("predict/")

    return render(request, "registration/d_login.html", {"form": form})


@login_required(login_url="docLogin")
def patLogin(request):
    form_class = PatientLoginForm
    p_form = form_class(request.POST or None)
    if request.method == "POST":
        if p_form.is_valid():
            fullname = request.POST.get("fullname")
            user = authenticate(request, fullname=fullname)

            if user is not None:
                login(request, user)
                if user.is_authenticated:
                    return HttpResponseRedirect("create/")

    return render(request, "classification_form.html", {"p_form": p_form})


def docLogout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="docLogin")
def patLogout(request):
    logout(request)
    return HttpResponseRedirect("about/")


def questioinaire(request):
    form_class = QuestionaireForm
    q_form = form_class(request.POST or None)
    if request.method == "POST":

        if q_form.is_valid():
            questionaire = q_form.save(commit=False)
            questionaire.weight = q_form.clean_data.get("weight")
            questionaire.height = q_form.clean_data.get("height")
            questionaire.occupation = q_form.clean_data.get("occupation")
            questionaire.knee_pain = q_form.clean_data.get("knee_pain")
            questionaire.walking = q_form.clean_data.get("walking")
            questionaire.getting_up = q_form.clean_data.get("getting_up")
            questionaire.stiffness = q_form.clean_data.get("stiffness")
            questionaire.prosthesis = q_form.clean_data.get("prosthesis")
            questionaire.surgery = q_form.clean_data.get("surgery")

            Patient.questionaire.save()

        else:
            q_form = QuestionaireForm()

    return render(request, "classification_form.html", {"q_form": q_form})


def comment(request):
    form_class = CommentForm
    c_form = form_class(request.POST or None)
    if request.method == "POST":
        if c_form.is_valid():
            recomd = c_form.save(commit=False)
            recomd.recommendation = c_form.clean_data.get("recommendation")
            Patient.recomd.save(commit=True)
        else:
            c_form = CommentForm()

    return render(request, "classification_list.html",  {"c_form": c_form})

@login_required(login_url="/")
def HomePageView(request):
    template_name = "home.html"
    return render(request, template_name,)

def AboutPageView(request):
    template_name = "about.html"
    return render(request, template_name)

def HowToPageView(request):
    template_name = "how_to.html"
    return render(request, template_name,)

def predictPage(request):
    return render(request, "predict.html",)
