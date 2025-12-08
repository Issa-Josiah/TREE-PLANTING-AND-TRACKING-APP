from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SponsorForm

@staff_member_required  # Only admins can access
def add_sponsor(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SponsorForm()
    return render(request, 'sponsor/add_sponsor.html', {'form': form})
