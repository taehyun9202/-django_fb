from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import bcrypt

# Create your views here.
def main(request):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        context = {
            'loggedinuser' : userinSession,
        }
        return redirect('/home')

def register(request):
    errors = User.objects.registerVal(request.POST)
    if len(errors) > 0:
        for keys, val in errors.items():
           messages.error(request, val)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        password = pw_hash
    )
    if newuser:
        request.session['loginid'] = newuser.id
    return redirect('/home')

def login(request):
    errors = User.objects.loginVal(request.POST)
    if len(errors) > 0:
        for keys, val in errors.items():
           messages.error(request, val)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['loginid'] = logged_user.id
            return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect("/")

def edit(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    context = {
        'loggedinuser' : userinSession,
    }
    return render(request, 'edit.html', context)

def update(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    if bcrypt.checkpw(request.POST['password'].encode(), userinSession.password.encode()):
        if len(request.POST['newpw']) > 0:
            newpassword = request.POST['newpw']
            pw_hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt()).decode()
            userinSession.password = pw_hash
        if len(request.POST['firstName']) > 0:
            userinSession.firstName = request.POST['firstName']
        if len(request.POST['lastName']) > 0:
            userinSession.lastName = request.POST['lastName']
        userinSession.save()
        return redirect('/home')
    else:
        errors = User.objects.updateVal(request.POST)
        if request.POST['password']:
            errors['password'] ="Password does not match"
        if len(errors) > 0:
            for keys, val in errors.items():
                messages.error(request, val)
        return redirect('/edit')

def navbar(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    print("****************",friendslist)
    context = {
        'loggedinuser' : userinSession,
    }
    return render(request, "navbar.html", context)

def home(request):
    if 'loginid' not in request.session:
        return redirect('/')
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        getposts = Post.objects.all().order_by('-created_at')
        getcomment = Comment.objects.all()
        context = {
            'loggedinuser' : userinSession,
            'posts' : getposts,
            'comments' : getcomment
        }
    return render(request,'home.html', context)

def timeline(request, userid):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        getuser = User.objects.get(id = userid)
        getfriends = Friend.objects.exclude(id = userid).filter(creater = getuser)
        myfriends = Friend.objects.filter(creater = userinSession).values_list('flist', flat=True)
        getposts = Post.objects.filter(p_to = getuser).order_by('-created_at')
        getcomment = Comment.objects.all()
        ##########  friends  ##########
        paginator = Paginator(getfriends, 9)
        page = request.GET.get('page')
        friendspaginator = paginator.get_page(page)
        ###############################
        ###########  photos  ##########
        paginator = Paginator(getposts, 9)
        page = request.GET.get('page')
        photospaginator = paginator.get_page(page)
        ###############################
        print(getposts)
        context = {
                'loggedinuser' : userinSession,
                'user': getuser,
                'friends': getfriends,
                'myfriends': myfriends,
                'posts' : getposts,
                'comments' : getcomment,
                'friendpage' : friendspaginator,
                'phtopage' : photospaginator
        }
    return render(request, 'timeline.html', context)

def userfriends(request, userid):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        getuser = User.objects.get(id = userid)
        getfriends = Friend.objects.exclude(id = userid).filter(creater = getuser)
        myfriends = Friend.objects.filter(creater = userinSession).values_list('flist', flat=True)
        context = {
                'loggedinuser' : userinSession,
                'user': getuser,
                'friends': getfriends,
                'myfriends': myfriends,
        }
    return render(request, 'friend.html', context)


def updateinfo(request, userid):
    userinSession = User.objects.get(id = request.session['loginid'])
    userinSession.home = request.POST['home']
    userinSession.work = request.POST['work']
    userinSession.hometown = request.POST['hometown']
    userinSession.save()
    return redirect('/user/'+userid)

def post(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    if request.FILES:
        newPost = Post.objects.create(
            content = request.POST['content'], 
            p_creater = User.objects.get(id = request.session['loginid']),
            p_to = User.objects.get(id = request.POST['p_to']),
            image = request.FILES['image']
        )
    else:
        newPost = Post.objects.create(
            content = request.POST['content'], 
            p_creater = User.objects.get(id = request.session['loginid']),
            p_to = User.objects.get(id = request.POST['p_to']),
        )
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def showpost(request, postid):
    userinSession = User.objects.get(id = request.session['loginid'])
    getpost = Post.objects.get(id = postid)
    getcomment = Comment.objects.all()
    context = {
        'loggedinuser' : userinSession,
        'post' : getpost,
        'comments' : getcomment
    }
    return render(request, "post.html", context)

def reply(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    newComment = Comment.objects.create(
        c_creater = User.objects.get(id = request.session['loginid']),
        content = request.POST['content'], 
        c_message = Post.objects.get(id = request.POST['c_message'])
    )
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def photos(request, userid):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        getuser = User.objects.get(id = userid)
        myfriends = Friend.objects.filter(creater = userinSession).values_list('flist', flat=True)
        getphotos = Post.objects.filter(p_to = getuser).order_by('-created_at')
        getfriends = Friend.objects.exclude(id = userid).filter(creater = getuser)
        context = {
            'loggedinuser' : userinSession,
            'user': getuser,
            'friends': getfriends,
            'myfriends': myfriends,
            'photos': getphotos
        }
    return render(request, 'photo.html', context)

def changephoto(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    userinSession.pic = request.FILES['pic']
    userinSession.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def changecover(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    userinSession.cover = request.FILES['cover']
    userinSession.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def search(request):
    searchtext = request.POST['searchtext']
    request.session['searchtext'] = searchtext
    if searchtext:
        return redirect('/search/'+searchtext)
    else:
        return render(request, "search.html")

def searchbyname(request, searchtext):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        if searchtext == "all" or "All" or "ALL":
            searcheduser = User.objects.exclude(id = userinSession.id)
        else:
            searcheduser = User.objects.filter((Q(firstName__contains=request.session['searchtext']) |
                                        Q(lastName__contains=request.session['searchtext'])))
        print("************",searcheduser)
        context = {
            'loggedinuser' : userinSession,
            'searcheduser' : searcheduser
        }
    return render(request, "search.html", context)

def addfriend(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    newFriend = Friend.objects.create(
        creater = User.objects.get(id = request.session['loginid']),
        flist = User.objects.get(id = request.POST['flist']),
    )
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def deletepost(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    posttodelte = request.POST['postid']
    Post.objects.get(id = posttodelte).delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def deletecomment(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    commenttodelte = request.POST['commentid']
    Comment.objects.get(id = commenttodelte).delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def unfriend(request):
    userinSession = User.objects.get(id = request.session['loginid'])
    getfriendship = Friend.objects.filter((Q(creater=userinSession) |
                                           Q(flist = request.POST['flist']))).delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def contact(request):
    if 'loginid' not in request.session:
        return render(request, "main.html")
    else:
        userinSession = User.objects.get(id = request.session['loginid'])
        context = {
                'loggedinuser': userinSession
        }
    return render(request, 'contact.html', context)

def sendemail(request):
    # send_mail(sub, msg, from ,to, fail_silently=True) //form
    from_email = request.POST.get('email', '')
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    to_list = [settings.EMAIL_HOST_USER]
    if subject and message and from_email:
        send_mail(
            subject,
            from_email+" "+message,
            from_email,
            to_list,
            fail_silently=False)
    return redirect('/')
