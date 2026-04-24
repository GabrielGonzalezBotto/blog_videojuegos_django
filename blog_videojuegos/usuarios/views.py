from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from  forms import RegistroForm, loginForm
from django.contrib import messages

# Create your views here.


