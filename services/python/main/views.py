from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from models import CatUser, CatRecord
from forms import AddRecordForm
from super_secret_crypto import super_secret_hash


@login_required(login_url='/accounts/login/')
def main_view(request):
    if request.method == "POST":
        form = AddRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AddRecordForm()

    images = CatRecord.objects.filter(is_private=False).order_by('id')[:10]
    if len(images) % 2 == 1:
        last_image = images[len(images)-1]
    else:
        last_image = None

    images_left = images[::2]
    images_right = images[1::2]
    images_list = zip(images_left, images_right)

    context = RequestContext(request)
    context['friend_token'] = CatUser.objects.get(pk=request.user.pk).friend_token
    context['form'] = form
    context['images'] = images_list
    context['last_image'] = last_image
    return render_to_response('index.html', context)


def registration(request):
    if request.method == "POST":
        data = request.POST
        user_login = data['login']
        user_password = data['password']
        if user_login and user_password:
            test_user = CatUser.objects.filter(username=user_login)
            if len(test_user):
                return HttpResponse('already existed user!')

            user = CatUser.objects.create_user(user_login, None, user_password)
            user.save()
            return redirect('/accounts/login/')
    else:
        context = RequestContext(request)
        return render_to_response('registration/register.html', context)


def render_images_list(request, images):
    if len(images) % 2 == 1:
        last_image = images[len(images)-1]
    else:
        last_image = None

    images_left = images[::2]
    images_right = images[1::2]
    images_list = zip(images_left, images_right)

    context = RequestContext(request)
    context['friend_token'] = CatUser.objects.get(pk=request.user.pk).friend_token
    context['images'] = images_list
    context['last_image'] = last_image
    return render_to_response('index.html', context)


@login_required(login_url='/accounts/login/')
def search(request):
    fields = [x.name for x in CatRecord._meta.fields]
    data = request.GET or request.POST
    data_dict = {}
    for elem in data:
        data_dict[elem] = data[elem]

    if not 'is_private' in data_dict:
        data_dict['is_private'] = '0'

    if 'owner' in data_dict:
        data_dict['owner'] = get_object_or_404(CatUser, username=data['owner'])

    images = CatRecord.objects.all()
    for elem in data_dict:
        if elem in fields:
            temp_dict = {elem: data_dict[elem]}
            images = images.filter(**temp_dict)

    return render_images_list(request, images)


@login_required(login_url='/accounts/login/')
def user_images(request, user_name):
    data = request.GET
    user = get_object_or_404(CatUser, username=user_name)

    is_friend = False
    if 'friend_token' in data:
        is_friend = user.friend_token == data['friend_token']

    images_list = CatRecord.objects.filter(
        owner=user)
    if user.pk != request.user.pk and not is_friend:
        images_list = images_list.filter(
            is_private=False)

    return render_images_list(request, images_list)


def users_list(request):
    context = RequestContext(request)
    context['users'] = CatUser.objects.all()
    return render_to_response('users.html', context)
