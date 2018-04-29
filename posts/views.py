# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import post,UserProfile
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from forms import UserProfileForm,PostForm
from django.template import RequestContext
from forms import RegistrationForm
from django.template.context_processors import csrf

# Create your views here.

#home Page post list

def post_list(request):
    queryset=post.objects.all()
    context={"posts":queryset
        }
    return render(request,"index.html",context)


def singlepost(request,id):
    instance=get_object_or_404(post,id=id)
    context={"post":instance}
    return render(request,"single_post.html",context)
#user logout------

def logout(request):
    auth.logout(request)
    msg="Sucessfully Logout...."
    queryset=post.objects.all()
    context={"posts":queryset,"msg":msg
        }
    return HttpResponseRedirect('/')

#user Dashboard------
@login_required(login_url='/login')
def dashboard(request):
    queryset=post.objects.filter(author_id=request.user.id)
    if request.user.is_authenticated():
        context={"posts":queryset,"menu":1}
    else:
        context={"posts":queryset}
    return render(request,"dashboard.html",context)

#user login---------

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    c={}
    c.update(csrf(request))
    return render(request, 'login.html',c)

def auth_view(request):
    username=request.POST.get('uname',"")
    password=request.POST.get('psw',"")
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/dashboard')
    else:
        msg="Wrong Username or Password ....Please Try again."
        return render(request, 'login.html',{'msg': msg})

#Author View -----------

def author(request,id):
    args={}
    author=get_object_or_404(User,id=id)
    args["author"] = author
    return render(request, 'author.html',args, RequestContext(request))
    


#user registration -----------    

def user_registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    args={}
    args.update(csrf(request))
    if request.method=="POST":
        form1=RegistrationForm(request.POST)
        form2=UserProfileForm(request.POST)
        args["err"] = form1.errors
        args["err2"]= form2.errors
        if form1.is_valid() * form2.is_valid():
            user=form1.save()
            userprofile=form2.save(commit=False)
            userprofile.user=user
            userprofile.save()
            return HttpResponseRedirect('/register_success')
    

    args["form"] = RegistrationForm()
    args["form2"] = UserProfileForm()
    args["form_title"]="Register"
    return render(request, 'register.html',args, RequestContext(request))

@login_required(login_url='/login')
def user_profile_edit(request):

    instance1=get_object_or_404(User,id=request.user.id)
    instance2=get_object_or_404(UserProfile,id=request.user.profile.id)
    args={}
    
    args.update(csrf(request))
    if request.method=="POST":
        form1=RegistrationForm(request.POST, instance=instance1)
        form2=UserProfileForm(request.POST,request.FILES, instance=instance2)
        args["err"] = form1.errors
        args["err2"]= form2.errors
        if form1.is_valid() * form2.is_valid():
            user=form1.save()
            userprofile=form2.save(commit=False)
            userprofile.user=user
            userprofile.save()
            return HttpResponseRedirect('/dashboard')
    

    args["form"] = RegistrationForm(instance=instance1)
    args["form2"] = UserProfileForm(instance=instance2)
    args["form_title"]="Edit Profile Info"
    return render(request, 'register.html',args, RequestContext(request))

@login_required(login_url='/login')
def post_submittion(request):
    args={}
    args.update(csrf(request))
    if request.method=="POST":
        form=PostForm(request.POST, request.FILES)
        args["err"] = form.errors
        if form.is_valid():
            post=form.save(commit=False)
            post.author_id=request.user.id
            post.save()
            return HttpResponseRedirect('/dashboard')
     

    args["form"] = PostForm()
    args["form_title"]="Submit Your Article"
    return render(request, 'register.html',args, RequestContext(request))

def post_delete(request,id=None):
    instance=get_object_or_404(post,id=id)
    if request.user.id==instance.author_id:
        
        instance.delete()
        context={"msg":"post successfully deleted"}
        return HttpResponseRedirect('/dashboard')
    else:
        context={"msg":"You are not allowed to perform this action","show":"alert-danger"}
        return render(request, 'dashboard.html',context)

@login_required(login_url='/login')
def post_edit(request,id):
    instance=get_object_or_404(post,id=id)
    if request.user.id==instance.author_id:
        args={}
        instance=get_object_or_404(post,id=id)
        
        args.update(csrf(request))
        if request.method=="POST":
            form=PostForm(request.POST, request.FILES, instance=instance)
            args["err"] = form.errors
            
            if form.is_valid():
                instance=form.save(commit=False)
                instance.author_id=request.user.id
                instance.save()
                return HttpResponseRedirect('/dashboard')
        args["form"]=PostForm(instance=instance)
        args["form_title"]="Edit Article"
        return render(request, 'register.html',args, RequestContext(request))
    else:
        context={"msg":"You are not allowed to perform this action","show":"alert-danger"}
        return render(request, 'dashboard.html',context)

def register_success(request):
    msg="Register Successful ...Please Login"
    return render(request, 'login.html',{'msg': msg})
