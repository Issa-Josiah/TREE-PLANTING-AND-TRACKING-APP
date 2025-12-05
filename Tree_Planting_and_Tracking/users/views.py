from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient





def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tree_list')
        else:
            messages.error(request, "Invalid login")

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

# mpesa intgretion

def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = 'phoneNumber'
    amount = 'amount'
    account_reference = 'TreeTops'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def mpesaPayement(request):
    if request.method == "POST":
        phone_number = request.POST.get('phoneNumber', '').strip()
        amount = request.POST.get('amount', '').strip()

        # ensure the input is good
        try:
            amount = int(float(amount))
        except ValueError:
            return HttpResponse("Amount must be a valid number")

        cl = MpesaClient()
        # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
        account_reference = 'TreeTops'
        transaction_desc = 'service purchase'
        callback_url = 'https://api.darajambili.com/express-payment'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        context = {
            'phone_number': phone_number,
            'amount': amount,
            'response': response,  # could contain checkoutRequestID etc
        }
        return render(request, 'accounts/waiting_response.html', context)
    context = {}
    return render(request, 'accounts/prompt_stk_push.html', context)
