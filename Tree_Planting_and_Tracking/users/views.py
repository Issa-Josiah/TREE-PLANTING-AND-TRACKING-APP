from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.admin.views.decorators import staff_member_required
from sponsors.models import Payment
from trees.models import Tree
from django.contrib.auth.decorators import login_required

@staff_member_required
def admin_add_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)  # use custom form
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully.")
            return redirect('admina_dashboard')
    else:
        form = UserRegisterForm()  # use custom form

    context = {'form': form}  # always define context
    return render(request, 'accounts/admin_add_user.html', context)





def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/register.html')

def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admina_dashboard')
    context =  {'user': user}
    return render(request, 'accounts/admin_delete_user.html',context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
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
    trees = Tree.objects.all()
    user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else ""

    if request.method == "POST":

        payment_type = request.POST.get("paymentType")
        tree_id = request.POST.get("tree")
        quantity = request.POST.get("quantity")
        name = request.POST.get("name")
        phone_number = request.POST.get("phoneNumber")
        amount = request.POST.get("amount")

        # Validate amount
        try:
            amount = int(float(amount))
        except:
            return HttpResponse("Invalid amount")

        tree = None
        if payment_type == "buy":
            tree = get_object_or_404(Tree, id=tree_id)
            quantity = int(quantity)
            if amount != tree.price * quantity:
                return HttpResponse("Amount mismatch detected!")

        # M-Pesa integration
        cl = MpesaClient()
        response = cl.stk_push(
            phone_number,
            amount,
            account_reference="TreeTops",
            transaction_desc="Tree Payment",
            callback_url="https://api.darajambili.com/express-payment"
        )

        user = request.user if request.user.is_authenticated else None

        # Save payment
        Payment.objects.create(
            user=user,
            payment_type=payment_type,
            tree=tree if tree else None,
            quantity=quantity if tree else 1,
            amount=amount,
            phone_number=phone_number,
            name=name
        )
        context = {"response": response,
                   "name": name,
                   "amount": amount,
                   "phone_number": phone_number}

        return render(request, "accounts/waiting_response.html", context)
    context =  {"trees": trees}
    return render(request, "accounts/prompt_stk_push.html", context)

@staff_member_required
def payments_list(request):
    payments = Payment.objects.all().order_by('-date')
    context =  {"payments": payments}
    return render(request, "accounts/payments_details.html", context)