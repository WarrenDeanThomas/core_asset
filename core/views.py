import qrcode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic

from .models import Core, CoreHistory, CoreReminders
from .forms import CoreForm, CoreHistoryForm, CoreReminderForm
from django.contrib import messages
from qr_code.qrcode.utils import QRCodeOptions
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
# from django.contrib.sessions import base_session
from datetime import date
from django.shortcuts import render
from qr_code.qrcode.utils import MeCard, VCard, EpcData, WifiConfig, Coordinates, QRCodeOptions
from django.shortcuts import get_object_or_404
import mimetypes


# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind = engine)
# session = Session()

# Create your views here.
@login_required
def index(request):
    core = Core.objects.all()
    core_count = core.count()
    history_count = CoreHistory.objects.all().count()
    reminders_count = CoreReminders.objects.all().count()
    users_count = User.objects.all().count()
    context = {
        'cores': core,
        'cores_count': core_count,
        'history_count': history_count,
        'reminders_count': reminders_count,
        'users_count': users_count
    }
    # return HttpResponse('This is the staff page')
    return render(request, 'core/index.html', context)


@login_required
def indexuser(request):
    # cores = core.objects.all()
    # workers_count = workers.count()
    # orders_count = Order.objects.all().count()
    # products_count = Product.objects.all().count()
    # context = {
    #     'cores': cores,
    #     # 'workers_count': workers_count,
    #     # 'orders_count': orders_count,
    #     # 'products_count': products_count
    # }
    # return HttpResponse('This is the staff page')
    return render(request, 'core/index_user.html')


def core(request):
    cores = Core.objects.all()
    cores_count = cores.count()

    # orders_count = Order.objects.all().count()
    # products_count = Product.objects.all().count()
    if request.method == 'POST':
        form = CoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance = form.save(commit=False)
            instance.owner_id = request.user
            instance.save()
            registration = form.cleaned_data.get('registration')
            messages.success(request, f'{instance.name} has been added')
            return redirect('core-core')
    else:
        form = CoreForm()
    context = {
        'cores': cores,
        'cores_count': cores_count,
        'form': form
        # 'orders_count': orders_count,
        # 'products_count': products_count
    }
    # return HttpResponse('This is the staff page')
    return render(request, 'core/core.html', context)


def save_qr_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.image.save("image.jpg", File(img_temp), save=True)


# def qr_test(request):
#     qr = qrcode.QRCode(
#         version=1,
#         box_size=15,
#         border=5
#     )
#     data = 'test'
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', backcolor='white')
#     img.save('test.png')


# def download_image(request, pk):
#     current_site = get_current_site(request)
#     qr_image = Core.objects.get(id=pk)
#     product_image_url = qr_image.product_image_url()
#     wrapper = FileWrapper(open(settings.MEDIA_ROOT + product_image_url[6:], 'rb'))
#     content_type = mimetypes.guess_type(product_image_url)[0]
#     response = HttpResponse(wrapper, mimetype=content_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % product_image_url
#     return response


# def download_file(request):
#     # fill these variables with real values
#     fl_path = '/documents/'
#     filename = 'test.png'
#
#     fl = open(fl_path, 'r')
#     mime_type, _ = mimetypes.guess_type(fl_path)
#     response = HttpResponse(fl, content_type=mime_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     return response


def core_detail(request, pk):
    cores = Core.objects.get(id=pk)
    context = {'cores': cores, 'link': request.build_absolute_uri, 'site': get_current_site(request)}
    return render(request, 'core/core_details.html', context)


def core_detail_card(request, pk):
    cores = Core.objects.get(id=pk)
    context = {'cores': cores, 'link': request.build_absolute_uri, 'site': get_current_site(request)}
    return render(request, 'core/core_details_card.html', context)


def core_delete(request, pk):
    item = Core.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core')

    return render(request, 'core/core_delete.html')


def core_update(request, pk):
    item = Core.objects.get(id=pk)
    if request.method == 'POST':
        form = CoreForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core-core')
    else:
        form = CoreForm(instance=item)

    context = {
        'form': form,

    }
    return render(request, 'core/core_update.html', context)


# def core_history(request, pk):
#     core_history = coreHistory.objects.filter(core_id=pk)
#     # for v in core_history:
#     #     core_history.save()
#     if request.method == 'POST':
#         form = coreHistory(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             event = form.cleaned_data.get('event')
#             messages.success(request, f'{event} has been added')
#             return redirect('core-core')
#     else:
#         form = coreHistory()
#     context = {
#         'core_history': core_history,
#         # 'cores_count': cores_count,
#         'form': form
#         # 'orders_count': orders_count,
#         # 'products_count': products_count
#     }
#     # return HttpResponse('This is the staff page')
#     return render(request, 'core/cores.html', context)


def core_data(request):
    core_data = Core.objects.all()
    # core_history_count = core_history_all.count()
    context = {'core_data': core_data}
    return render(request, 'core/core_user_data.html', context)


def core_history_all(request):
    core_history_all = CoreHistory.objects.all()
    core_history_count = core_history_all.count()
    context = {'core_history_all': core_history_all, 'core_history_count': core_history_count}
    return render(request, 'core/core_history_all.html', context)


def core_history_detail(request, pk):
    core_history_all_id = CoreHistory.objects.get(id=pk)
    context = {
        'core_history_all_id': core_history_all_id

    }
    return render(request, 'core/core_history_all.html', context)


def core_history(request, pk):
    # core_history = CoreHistory.objects.filter(core_id=pk)
    # core_history = session.query(CoreHistory).join(Core).filter(core_id=pk)
    # core = Core.objects.all()
    # core_history = get_object_or_404(Core,id=pk)
    core_history = CoreHistory.objects.filter(core_id=pk).select_related('core')
    core_history_count = CoreHistory.objects.all().count()
    # core_history = CoreHistory.objects.raw('SELECT max(value) AS id FROM mytable GROUP BY id')
    # data = core_history
    # print(core_history.core_id)
    if request.method == 'POST':
        form1 = CoreHistoryForm(request.POST, request.FILES)

        if form1.is_valid():
            # instance = form1.save(commit=False)
            instance = form1.save(commit=False)
            instance.owner = request.user
            # instance.core = request.Core_id
            instance.save()
            # core_history.core_id = core_history.core.id
            # instance.core_id = request.core_id
            # instance.save()
            # form1.save()
            registration = form1.cleaned_data.get('event')
            messages.success(request, f'{instance.event} has been added')
            return redirect('core-core')
    else:
        form1 = CoreHistoryForm()

    context = {'core_history': core_history, 'form1': form1, 'core_history_count': core_history_count}
    return render(request, 'core/core_history.html', context)


def core_history_add(request, pk):
    # core = request.cores
    core = get_object_or_404(Core, pk=pk)
    # core_history = CoreHistory.objects.filter(core_id=pk).select_related('core')
    if request.method == "POST":
        form = CoreHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            corehistory = form.save(commit=False)
            corehistory.core = core
            corehistory.save()
            # event = form.cleaned_data.get('event')
            # event_desc = form.cleaned_data.get('event_desc')
            # file = form.cleaned_data.get('file')
            # p, created = CoreHistory.objects.get_or_create(event=event, event_desc=event_desc, file=file)
            # p.save()
            return redirect('core-core_history', pk=core.pk)
    else:
        form = CoreHistoryForm()
    context = {
        'form': form
    }
    return render(request, 'core/core_history_add.html', context)


def core_history_update(request, pk):
    item = CoreHistory.objects.get(id=pk)
    if request.method == 'POST':
        form = CoreHistoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core-core_history', pk=item.core_id)
    else:
        form = CoreHistoryForm(instance=item)

    context = {
        'form': form,

    }
    return render(request, 'core/core_history_update.html', context)


def core_history_delete(request, pk):
    item = CoreHistory.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core_history', pk=item.core_id)

    return render(request, 'core/core_history_delete.html')


def core_reminder_all_id(request, pk):
    core_reminders_all = CoreReminders.objects.get(id=pk)
    context = {
        'core_reminders_all': core_reminders_all

    }
    return render(request, 'core/core_reminder_all.html', context)


def core_reminder_all(request):
    core_reminder_all = CoreReminders.objects.all()
    core_reminder_all_count = core_reminder_all.count()
    context = {'core_reminder_all': core_reminder_all, 'core_reminder_all_count': core_reminder_all_count}
    return render(request, 'core/core_history_all.html', context)


def core_reminder_detail(request, pk):
    core_reminders_detail = CoreReminders.objects.get(id=pk)
    # core_reminders_count = core_reminders_detail.count()
    context = {'core_reminders_detail': core_reminders_detail}
    return render(request, 'core/core_reminder_all.html', context)


def core_reminder(request, pk):
    core_reminder = CoreReminders.objects.filter(core_id=pk).select_related('core')
    core_reminder_count = CoreReminders.objects.all().count()
    # core_history = CoreHistory.objects.raw('SELECT max(value) AS id FROM mytable GROUP BY id')
    # data = core_history
    # print(core_history.core_id)
    if request.method == 'POST':
        form = CoreReminderForm(request.POST, request.FILES)

        if form.is_valid():
            # instance = form1.save(commit=False)
            instance = form.save(commit=False)
            instance.owner = request.user
            # instance.core = request.Core_id
            instance.save()
            # core_history.core_id = core_history.core.id
            # instance.core_id = request.core_id
            # instance.save()
            # form1.save()
            registration = form.cleaned_data.get('activity')
            messages.success(request, f'{instance.activity} has been added')
            return redirect('core-core')
    else:
        form = CoreReminderForm()

    context = {'core_reminder': core_reminder, 'form': form, 'core_reminder_count': core_reminder_count}
    return render(request, 'core/core_reminder.html', context)


def core_reminder_add(request, pk):
    # core = request.cores
    core = get_object_or_404(Core, pk=pk)
    # core_history = CoreHistory.objects.filter(core_id=pk).select_related('core')
    if request.method == "POST":
        form = CoreReminderForm(request.POST, request.FILES)
        if form.is_valid():
            corereminder = form.save(commit=False)
            corereminder.core = core
            corereminder.save()
            # event = form.cleaned_data.get('event')
            # event_desc = form.cleaned_data.get('event_desc')
            # file = form.cleaned_data.get('file')
            # p, created = CoreHistory.objects.get_or_create(event=event, event_desc=event_desc, file=file)
            # p.save()
            return redirect('core-core_reminder', pk=core.pk)
    else:
        form = CoreReminderForm()
    context = {
        'form': form
    }
    return render(request, 'core/core_reminder_add.html', context)


def core_reminder_update(request, pk):
    item = CoreReminders.objects.get(id=pk)
    if request.method == 'POST':
        form = CoreReminderForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core-core_reminder', pk=item.core_id)
    else:
        form = CoreReminderForm(instance=item)

    context = {
        'form': form,

    }
    return render(request, 'core/core_reminder_update.html', context)


def core_reminder_delete(request, pk):
    item = CoreReminders.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core_reminder', pk=item.core_id)

    return render(request, 'core/core_reminder_delete.html')
