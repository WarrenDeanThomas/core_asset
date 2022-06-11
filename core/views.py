import qrcode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Sum

from .models import Core, CoreHistory, CoreReminders, Limits
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
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
import pandas as pd

from django.db.models import Sum
from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField



# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind = engine)
# session = Session()

# Create your views here.
@login_required
def index(request):
    core = Core.objects.all()
    core_count = core.count()
    core_count_user = Core.objects.filter(owner_id=request.user).count()
    history_count = CoreHistory.objects.all().count()
    reminders_count = CoreReminders.objects.all().count()
    users_count = User.objects.all().count()
    core_count_pets_data = Limits.objects.filter(owner_id=request.user)
    core_count_pets = core_count_pets_data[0].number_of_pets
    pet_total = core_count_user
    pet_max = core_count_pets
    exceeded_max = pet_max-pet_total
    # exceeded_max_pets = if(pet_max - exceeded_max) > 0, 1, 0

    # core_count_pets = Limits.objects.select_related('profile').values('number_of_pets').values
    # core_count_pets = Limits.objects.get('number_of_pets')[0]
    context = {
        'cores': core,
        'cores_count': core_count,
        'history_count': history_count,
        'reminders_count': reminders_count,
        'users_count': users_count,
        'core_count_user': core_count_user,
        'core_count_pets': core_count_pets,
        'pet_total': pet_total,
        'pet_max': pet_max,
        'exceeded_max': exceeded_max
        # 'exceeded_max_pets': exceeded_max_pets
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


@login_required
def core(request):
    cores = Core.objects.all()
    cores_count = cores.count()
    core_count_user = Core.objects.filter(owner_id=request.user).count()
    core_count_pets_data = Limits.objects.filter(owner_id=request.user)
    core_count_pets = core_count_pets_data[0].number_of_pets
    pet_total = core_count_user
    pet_max = core_count_pets
    exceeded_max = pet_max - pet_total
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
        'core_count_user': core_count_user,
        'core_count_pets': core_count_pets,
        'pet_total': pet_total,
        'pet_max': pet_max,
        'exceeded_max': exceeded_max,
        'form': form

        # 'owner': owner
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


@login_required
def core_detail(request, pk):
    cores = Core.objects.get(id=pk)
    card_url = f"{get_current_site(request)}/core_detail_card/{cores.id}"
    context = {'cores': cores, 'link': request.build_absolute_uri, 'site': get_current_site(request), "card_url": card_url}
    return render(request, 'core/core_details.html', context)


def core_detail_card(request, pk):
    cores = Core.objects.get(id=pk)
    card_url = f"{get_current_site(request)}/core_detail_card/{cores.id}"
    card_add_url = f"{get_current_site(request)}/core_history/{cores.id}/add/"
    context = {'cores': cores, 'link': request.build_absolute_uri, 'site': get_current_site(request),
               "card_url": card_url, 'card_add_url': card_add_url}
    return render(request, 'core/core_details_card.html', context)


@login_required
def core_delete(request, pk):
    item = Core.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core')

    return render(request, 'core/core_delete.html')


@login_required
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


@login_required
def core_data(request):
    core_data = Core.objects.all()
    # core_history_count = core_history_all.count()
    context = {'core_data': core_data}
    return render(request, 'core/core_user_data.html', context)


@login_required
def core_history_all(request):
    core_history_all = CoreHistory.objects.all()
    core_history_count = core_history_all.count()
    context = {'core_history_all': core_history_all, 'core_history_count': core_history_count}
    return render(request, 'core/core_history_all.html', context)


@login_required
def core_history_dashboard(request):
    #get all data
    core_history_all = CoreHistory.objects.all()
    #get data by user
    core_history_user = CoreHistory.objects.filter(core__owner=request.user)
    core_history_count = core_history_all.count()
    core_history_count_user = core_history_user.count()
    #filter by each category
    count_fuel = core_history_all.filter(category="Fuel").count()
    count_maintenance = core_history_all.filter(category="Maintenance").count()
    count_repair = core_history_all.filter(category="Repair").count()
    count_other = core_history_all.filter(category="Other").count()
    # filter by each category by user
    count_fuel_user = core_history_user.filter(category="Fuel").count()
    count_maintenance_user = core_history_user.filter(category="Maintenance").count()
    count_repair_user = core_history_user.filter(category="Repair").count()
    count_other_user = core_history_user.filter(category="Other").count()
    # get values for the dataset
    data = CoreHistory.objects.all().values()
    data_user = core_history_user.values()
    #create dataframes
    df = pd.DataFrame(data)
    df_user = pd.DataFrame(data_user)
    # add a month column to df
    df['month'] = pd.DatetimeIndex(df['date_of_event']).month
    df_user['month'] = pd.DatetimeIndex(df_user['date_of_event']).month

    # df_user['Month'] = pd.DatetimeIndex(df['date_of_event']).month
    # create lists for columns inDF
    dfCategory = df.category.tolist()
    dfCount = df.amount.tolist()
    # Do a group by category and sum the amount column
    dfsummary = df.groupby(['category'])['amount'].sum().reset_index()
    dfsummary_user = df_user.groupby(['category'])['amount'].sum().reset_index()
    #summary by sum date
    dfsummary_date = df.groupby(['month'])['amount'].sum().reset_index()
    dfsummary_user_date = df_user.groupby(['month'])['amount'].sum().reset_index()
    # summary by count date
    # dfsummary_date_count = df.groupby(['month'])['event'].count().reset_index()
    # dfsummary_user_date_count = df_user.groupby(['month'])['event'].count().reset_index()
    #summary by core - asset
    dfsummary_core = df.groupby(['core_id'])['amount'].sum().reset_index()
    dfsummary_user_core = df_user.groupby(['core_id'])['amount'].sum().reset_index()

    # create lists for columns inDF
    dfcat = dfsummary.category.tolist()
    dfsum = dfsummary.amount.tolist()
    dfcat_user = dfsummary_user.category.tolist()
    dfsum_user = dfsummary_user.amount.tolist()
    dfcat_date = dfsummary_date.month.tolist()
    dfsum_date = dfsummary_date.amount.tolist()
    # dfsum_date_event_count = dfsummary_date_count.event.tolist()
    # dfsum_date_count = dfsummary_date.amount.tolist()
    dfcat_user_date = dfsummary_user_date.month.tolist()
    dfsum_user_date = dfsummary_user_date.amount.tolist()
    # dfsum_user_date_event_count = dfsummary_user_date_count.event.tolist()
    # dfsum_user_date_count = dfsummary_user_date.id.tolist()
    dfcat_core = dfsummary_core.core_id.tolist()
    dfsum_core = dfsummary_core.amount.tolist()
    dfcat_user_core = dfsummary_user_core.core_id.tolist()
    dfsum_user_core = dfsummary_user_core.amount.tolist()

    #These are the totals from above views - we need them for the TOP NAV totals
    core = Core.objects.all()
    core_count = core.count()
    core_count_user = Core.objects.filter(owner_id=request.user).count()
    history_count = CoreHistory.objects.all().count()
    reminders_count = CoreReminders.objects.all().count()
    users_count = User.objects.all().count()
    core_count_pets_data = Limits.objects.filter(owner_id=request.user)
    core_count_pets = core_count_pets_data[0].number_of_pets
    pet_total = core_count_user
    pet_max = core_count_pets
    exceeded_max = pet_max-pet_total

    #create a list for the pie chart - this would be easier in a df but showing the manual way
    category_list = ['Maintenance', 'Repair', 'Fuel', 'Other']
    category_count = [count_maintenance, count_repair, count_fuel, count_other]

    # create a list for the pie chart - this would be easier in a df but showing the manual way
    category_list_user = ['Maintenance', 'Repair', 'Fuel', 'Other']
    category_count_user = [count_maintenance_user, count_repair_user, count_fuel_user, count_other_user]

    # returns {'price__sum': 1000} for example
    context = {'core_history_all': core_history_all, 'core_history_count': core_history_count,
               'category_list': category_list, 'category_count': category_count,
               'category_list_user': category_list_user, 'category_count_user': category_count_user,
               'dfCategory': dfCategory,
               'dfCount': dfCount, 'dfcat': dfcat, 'dfsum': dfsum, 'dfcat_user': dfcat_user, 'dfsum_user': dfsum_user,
               'dfcat_date': dfcat_date, 'dfsum_date': dfsum_date,
               'dfcat_user_date': dfcat_user_date, 'dfsum_user_date': dfsum_user_date, 'dfcat_core': dfcat_core,
               'dfsum_core': dfsum_core, 'dfcat_user_core': dfcat_user_core, 'dfsum_user_core': dfsum_user_core,
               # 'dfsum_date_count': dfsum_date_count, 'dfsum_user_date_count': dfsum_user_date_count,
               # 'dfsum_date_event_count': dfsum_date_event_count, 'dfsum_user_date_event_count': dfsum_user_date_event_count,
               'cores': core,
               'cores_count': core_count,
               'history_count': history_count,
               'reminders_count': reminders_count,
               'users_count': users_count,
               'core_count_user': core_count_user,
               'core_count_pets': core_count_pets,
               'pet_total': pet_total,
               'pet_max': pet_max,
               'exceeded_max': exceeded_max,
               'core_history_count_user': core_history_count_user,
               }
    return render(request, 'core/dashboard.html', context)


@login_required
def core_history_detail(request, pk):
    core_history_all_id = CoreHistory.objects.get(id=pk)
    context = {
        'core_history_all_id': core_history_all_id

    }
    return render(request, 'core/core_history_all.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
def core_history_delete(request, pk):
    item = CoreHistory.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core_history', pk=item.core_id)

    return render(request, 'core/core_history_delete.html')


@login_required
def core_reminder_all_id(request, pk):
    core_reminders_all = CoreReminders.objects.get(id=pk)
    context = {
        'core_reminders_all': core_reminders_all

    }
    return render(request, 'core/core_reminder_all.html', context)


@login_required
def core_reminder_all(request):
    core_reminder_all = CoreReminders.objects.all()
    core_reminder_all_count = core_reminder_all.count()

    context = {'core_reminder_all': core_reminder_all, 'core_reminder_all_count': core_reminder_all_count }
    return render(request, 'core/core_reminder_all.html', context)


@login_required
def core_reminder_week(request):
    current_date = date.today()
    future_date = current_date + timedelta(days=7)
    core_reminder_all = CoreReminders.objects.all()
    core_reminder_week = core_reminder_all.filter(
        date_of_activity__range=(current_date, future_date),
    )
    core_reminder_all_count = core_reminder_all.count()
    core_reminder_week_count = core_reminder_week.count()
    context = {'core_reminder_all': core_reminder_all, 'core_reminder_all_count': core_reminder_all_count,
               'core_reminder_week': core_reminder_week, 'core_reminder_week_count': core_reminder_week_count}
    return render(request, 'core/core_reminder_upcoming_events.html', context)








@login_required
def core_reminder_detail(request, pk):
    core_reminders_detail = CoreReminders.objects.get(id=pk)
    # core_reminders_count = core_reminders_detail.count()
    context = {'core_reminders_detail': core_reminders_detail}
    return render(request, 'core/core_reminder_all.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
def core_reminder_delete(request, pk):
    item = CoreReminders.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core-core_reminder', pk=item.core_id)

    return render(request, 'core/core_reminder_delete.html')


@login_required
def core_users(request):
    # User = get_user_model()
    # users = User.object.all()
    core_users = User.objects.all()
    all_users = User.objects.values()

    context = {'core_users': core_users, 'all_users': all_users}
    return render(request, 'core/core_user.html', context)


def send_email(request):
    all_users = get_user_model().objects.all()
    emails = [user.email for user in all_users]
    subject, from_email, to = 'hello', 'EMAIL_HOST_USER', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content,  from_email, emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # current_date = date.today()
    # future_date = current_date + timedelta(days=7)
    # core_reminder_all = CoreReminders.objects.all()
    # core_reminder_week = core_reminder_all.filter(
    #     date_of_activity__range=(current_date, future_date),
    # )
    # core_reminder_all_count = core_reminder_all.count()
    # core_reminder_week_count = core_reminder_week.count()
    # subject = "Test subject"
    # message = f'today is {current_date} and you have {core_reminder_week_count} reminders this week'
    # from_email = "EMAIL_HOST_USER"
    # if subject and message and from_email:
    #     try:
    #         send_mail(subject, message, from_email, ['warrendeanthomas@gmail.com'])
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return HttpResponseRedirect('core-index')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')

def send_email(request):
    current_date = date.today()
    future_date = current_date + timedelta(days=7)
    core_reminder_all = CoreReminders.objects.all()
    core_reminder_week = core_reminder_all.filter(
        date_of_activity__range=(current_date, future_date),
    )
    core_reminder_all_count = core_reminder_all.count()
    core_reminder_week_count = core_reminder_week.count()
    for core in core_reminder_week:

        # if user.is_active and user != request.user:
            message = EmailMultiAlternatives(
                subject="Reminder of your Pets upcoming events ",
                from_email="EMAIL_HOST_USER",
                to=[core.core.contact_email],
            )
            context = {'core_reminder_all': core_reminder_all, 'core_reminder_all_count': core_reminder_all_count,
                       'core_reminder_week': core_reminder_week, 'core_reminder_week_count': core_reminder_week_count}
            # html_template = get_template("core/core_reminder_upcoming_events.html").render(context)
            html_template = get_template("core/mail.html").render(context)
            message.attach_alternative(html_template, "text/html")
            message.send()
        # else:
        #     return render(request, 'core/index.html')

