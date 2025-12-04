from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tree
from .forms import TreeForm

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

@login_required
def my_trees(request):
    trees = Tree.objects.filter(owner=request.user)
    context = {'tree_app': trees}
    return render(request, 'tree_app/my_trees.html', context )

def tree_list(request):
    trees = Tree.objects.all()
    context = {'trees': trees}
    return render(request, 'tree_app/tree_list.html', context)
