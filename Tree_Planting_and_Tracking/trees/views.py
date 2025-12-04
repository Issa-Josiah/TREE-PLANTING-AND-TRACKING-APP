from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Tree
from .forms import TreeForm


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

    return render(request, 'tree_app/add_tree.html', {'form': form})


# viewing my trees and the details
@login_required
def my_trees(request):
    trees = Tree.objects.filter(owner=request.user)
    context = {'tree_app': trees}
    return render(request, 'tree_app/my_trees.html', context )

def tree_list(request):
    trees = Tree.objects.all()
    context = {'trees': trees}
    return render(request, 'tree_app/tree_list.html', context)

def tree_detail(request, id):
    tree = get_object_or_404(Tree, id=id)
    return render(request, 'tree_app/tree_detail.html', {'tree': tree})

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

    return render(request, 'tree_app/edit_tree.html', {'form': form, 'tree': tree})

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

    return render(request, 'tree_app/delete_tree.html', {'tree': tree})

# price tag for the admin


@staff_member_required  # Only admin/staff can access
def admin_edit_tree(request, id):
    tree = get_object_or_404(Tree, id=id)

    if request.method == "POST":
        form = TreeAdminForm(request.POST, instance=tree)
        if form.is_valid():
            form.save()
            messages.success(request, "Tree price/payment updated successfully.")
            return redirect('tree_detail', id=tree.id)
    else:
        form = TreeAdminForm(instance=tree)

    return render(request, 'tree_app/admin_edit_tree.html', {'form': form, 'tree': tree})

# admin dashboard

@staff_member_required
def admina_dashboard(request):
    users = User.objects.all()
    trees = Tree.objects.all()
    return render(request, 'tree_app/admin_dashboard.html', {'users': users, 'trees': trees})
