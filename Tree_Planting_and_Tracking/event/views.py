from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from calendar import month_name


#  the list of the event
def event_list(request):
    events = Event.objects.all().order_by('date')
    month_str = request.GET.get('month')
    month = int(month_str) if month_str else None
    selected_month = int(month) if month else 1
    events = Event.objects.all().order_by('date')
    if selected_month:
        events = events.filter(date__month=selected_month)
    months = [(i, month_name[i]) for i in range(1, 13)]
    selected_month_name = month_name[month] if month else 'month chosen .Kindly select event to see event'
    context = {'events': events,
               'selected_month': int(month) if month else None,
               'months': months,
               'selected_month_name': selected_month_name,}

    return render(request, 'event/event_list.html', context)

# adding of the event
@staff_member_required
def add_event(request):

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event added successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
        context = {'form': form}
    return render(request, 'event/add_event.html', context)

# editing of the event
@staff_member_required
def edit_event(request, id):

    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES,  instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
        context = {'form': form,
                   'event': event}
    return render(request, 'event/edit_event.html', context)


# deleting of the event
@staff_member_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('event_list')
    context =  {'event': event}
    return render(request, 'event/delete_event.html', context)



# payment of the event
@login_required
def event_payment(request, id):
    event = get_object_or_404(Event, id=id)
    context =  {'event': event}
    return render(request, 'event/event_payment.html',context)