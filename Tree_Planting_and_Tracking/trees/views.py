from urllib import request

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from .models import Tree
from .forms import TreeForm
from .forms import TreeAdminForm
from sponsors.models import Sponsor
from event.models import Event
from sponsors.models import Payment
from .models import Contact



def get_badge(tree_count):
    if tree_count >= 50:
        return "🥇 Gold"
    elif tree_count >= 30:
        return "🥈 Silver"
    elif tree_count >= 10:
        return "🥉 Bronze"
    elif tree_count >=2:
        return "🌲🌲 forest"
    elif tree_count ==1:
        return "🌳 starter"
    else:
        return "🌼bud"  # No badge


def leaderboard(request):
    leaderboard_data = (
        User.objects.annotate(tree_count=Count('tree'))
        .order_by('-tree_count')
    )

    # Add badge attribute dynamically
    for user in leaderboard_data:
        user.badge = get_badge(user.tree_count)
    sponsors = Sponsor.objects.all()
    context = {
        'leaderboard': leaderboard_data,
        'sponsors' : sponsors,
    }
    return render(request, 'tree_app/leaderboard.html', context)

# normal page
def dashboard(request):
    trees = Tree.objects.all()  # show all trees
    total_trees = trees.count()


    # User-specific tree count
    user_total = 0
    if request.user.is_authenticated:
        user_total = Tree.objects.filter(owner=request.user).count() if request.user.is_authenticated else 0

    # Upcoming events (ordered by date)
    events = Event.objects.order_by('date')[:3]

    # Sponsors
    sponsors = Sponsor.objects.all()

    context = {
        'trees': trees,
        'total_trees': total_trees,
        'user_total': user_total,
        'events': events,
        'sponsors': sponsors,
    }

    if request.user.is_authenticated:
        user_trees = trees.filter(owner=request.user)
        context['user_trees'] = user_trees
        context['user_total'] = user_trees.count()

    return render(request, 'tree_app/dashboard.html', context)
# adding tree

@login_required
def add_tree(request):
    if request.method == "POST":
        form = TreeForm(request.POST, request.FILES)
        if form.is_valid():
            tree = form.save(commit=False)
            tree.owner = request.user
            tree.save()
            return redirect('my_trees')
    else:
        form = TreeForm()
    context =  {'form': form}
    return render(request, 'tree_app/add_tree.html', context)


# viewing my trees and the details
@login_required
def my_trees(request):
    user_trees = Tree.objects.filter(owner=request.user)
    context = {'my_tree': user_trees}
    return render(request, 'tree_app/my_trees.html', context )

def tree_list(request):
    trees = Tree.objects.all()
    context = {'trees': trees}
    return render(request, 'tree_app/tree_list.html', context)

def tree_detail(request, id):
    tree = get_object_or_404(Tree, id=id)
    context ={'tree': tree}
    return render(request, 'tree_app/tree_detail.html', context)

# editing the tree
@login_required
def edit_tree(request, id):
    tree = get_object_or_404(Tree, id=id)

    # Only owner can edit
    if request.user != tree.owner:
        return HttpResponseForbidden("You are not allowed to edit this tree.")

    if request.method == "POST":
        form = TreeForm(request.POST, request.FILES, instance=tree)
        if form.is_valid():
            form.save()
            return redirect('tree_detail', id=tree.id)
    else:
        form = TreeForm(instance=tree)
    context =  {'form': form,
                'tree': tree}
    return render(request, 'tree_app/edit_tree.html',context)

# deleting tree


@login_required
def delete_tree(request, id):
    tree = get_object_or_404(Tree, id=id)

    # Only owner can delete
    if request.user != tree.owner:
        return HttpResponseForbidden("You are not allowed to delete this tree.")

    if request.method == "POST":
        tree.delete()
        messages.success(request, "Tree deleted successfully.")
        return redirect('my_trees')
    context = {'tree': tree}
    return render(request, 'tree_app/tree_delete.html',context)

# price tag for the admin


@staff_member_required  # Only admin/staff can access
def admin_edit_tree(request, id):
    tree = get_object_or_404(Tree, id=id)

    if request.method == "POST":
        form = TreeAdminForm(request.POST, request.FILES, instance=tree)
        if form.is_valid():
            form.save()
            messages.success(request, "Tree updated successfully.")
            return redirect('admina_dashboard')
    else:
        form = TreeAdminForm(instance=tree)

    context = {'form': form, 'tree': tree}
    return render(request, 'tree_app/edit_tree.html', context)

# delete_tree
@staff_member_required
def admin_delete_tree(request, id):
    tree = get_object_or_404(Tree, id=id)

    if request.method == "POST":
        tree.delete()
        messages.success(request, "Tree deleted successfully.")
        return redirect('admina_dashboard')

    context = {'tree': tree}
    return render(request, 'tree_app/tree_delete.html', context)


def about(request):
    return render(request, 'tree_app/about.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message_content
        )
        # Send email
        send_mail(
            subject=f"Contact Us Message from {name}",
            message=message_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        # Add success message
        messages.success(request, "✅ Your message has been sent successfully. Thank you!")
        return redirect('contact')  # Redirect after POST

    return render(request, 'tree_app/contact_us.html')

# admin dashboard

@staff_member_required
def admina_dashboard(request):
    users = User.objects.all()
    trees = Tree.objects.all()
    events = Event.objects.all().order_by('date')
    payments = Payment.objects.all().order_by('-date')
    contacts = Contact.objects.all().order_by('-created_at')

    context = {'users': users,
               'trees': trees,
               'events': events,
               'payments': payments,
               'contacts': contacts,  }
    return render(request, 'tree_app/admin_dashboard.html', context)



