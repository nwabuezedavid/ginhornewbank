from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *


from django.template.loader import get_template

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import *
from django.conf import settings
from rest_framework.decorators import api_view
from django.core.mail import send_mail,  EmailMultiAlternatives
from django.conf import settings
from datetime import datetime , timedelta,timezone
from django.views.decorators.csrf import csrf_exempt
from .genUid import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  django.utils.html import strip_tags
# Create your views here.
from django.template.loader import get_template, render_to_string




def denied(request, pk):
    if  Client.objects.filter(uuid=pk, disabled=False).exists():
        print('skdkd')

        disabledaccount(request)
    if  Client.objects.filter(uuid=pk, approved=False).exists():
        print('skdkd,sndnn')

        return redirect('Activate')
    else:
        pass


 
def email_sending(request,tempname,context,subjects,to):
    tos = render_to_string(tempname,context=context )
    tags =strip_tags(tos)
    mas = EmailMultiAlternatives(
        subject = subjects,
        body=tags,
        from_email = settings.EMAIL_HOST_USER,
        to=[to.lower()]
    )
    mas.attach_alternative(tos, 'text/html')
    mas.send()
    print(mas)

def email_sendingSINGLE(request,subjects,message,to):
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to]
    send_mail(subjects, message, from_email, recipient_list, fail_silently=False)
     
from rest_framework.response import Response 
from rest_framework.decorators import api_view

@api_view(['GET' ])
def sheckdisable(request, pk):
    try: 
        user = Client.objects.get(uuid = pk)
        if user.disabled==True and  user.approved==True:
            print('bloled')
            
            return Response({'data': 'now'})
            
        print('loading')
    except:

        return Response({'erre': 'error'})
    return Response({'erre': 'error'})
def adminauthdisable(request, pk):
    e = Client.objects.get(uuid=pk)
    ex = Client.objects.get(user=request.user)
    if  e.disabled == False :
        e.disabled=True
        e.save()
        messages.error(request,'Account disabled')
    elif e.disabled==True:
        e.disabled=False
        e.save()
        messages.error(request,'Account activated')
    
    return  redirect('admin', pk=ex.uuid)
def adminauthverified(request, pk):
    e = Client.objects.get(uuid=pk)
    ex = Client.objects.get(user=request.user)

    if  e.approved == False :
        e.approved=True
        e.save()
        messages.error(request,'Account verified')
    elif e.approved==True:
        e.approved=False
        e.save()
        messages.error(request,'Account unverified')
    return  redirect('admin', pk=ex.uuid)

def disabledaccount(request):
    
    i = Site.objects.get(uuid=1)

    logout(request)
    c = {
    'i':Site.objects.get(uuid=1),
    }


    return render(request,'html/blocked.html',c)
def home(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }

    return render(request,'html/home.html',c)
def contact(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'html/service.html',c)
def LOan(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'html/loan.html',c)
def transfers(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'html/transfer.html',c)
def about(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'html/about.html',c)
def mailxs(request):
    i = Site.objects.get(uuid=1)
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        message = request.POST['message']
        c = {
                        
                        'w':i
            }
        email_sending(request,'mail/blockedmail.html',c,f"Account Blocked ",email.lower())
        return redirect('mails')
    return render(request,'mail/mail.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Site, Client
from .utils import email_sending, referCode, acc  # assuming these are your helper functions

def loginuser(request):
    try:
        i = Site.objects.get(uuid=1)
        c = {'i': i}

        if request.method == "POST":
            hidden = request.POST.get('hidden')

            # ---- LOGIN SECTION ----
            if hidden == "false":
                passwordx = request.POST.get('pwds', '').strip()
                usernamex = request.POST.get('username', '').strip()
                emailx = request.POST.get('email', '').strip()

                email = emailx.replace(" ", "")
                username = usernamex.replace(" ", "_")
                password = passwordx.replace(" ", "")

                if User.objects.filter(username__icontains=username, email__icontains=email).exists():
                    alluser = User.objects.filter(username__icontains=username, email__icontains=email).first()

                    # Disabled account
                    if Client.objects.filter(user=alluser, disabled=True).exists():
                        c = {'a': alluser, 'w': i}
                        email_sending(request, 'mail/blockedmail.html', c, "Account Blocked", alluser.email)
                        return redirect('disabledaccount')

                    # Not approved yet
                    if Client.objects.filter(user=alluser, approved=False).exists():
                        alluserc = Client.objects.get(user=alluser)
                        login(request, alluserc.user)
                        return redirect('Activate')

                    # Valid login
                    if password and username and Client.objects.filter(
                        user=alluser, disabled=False, approved=True, password=password
                    ).exists():

                        if User.objects.filter(is_superuser=False, username=username, email=email).exists():
                            mainuser = Client.objects.get(user=alluser)
                            authenticate(username=username, password=password)
                            login(request, alluser)

                            if mainuser.Pin:
                                return redirect('dashboard', pk=mainuser.uuid)
                            else:
                                return redirect('pin', pk=mainuser.uuid)
                        elif alluser.is_superuser:
                            mainuser = Client.objects.get(user=alluser)
                            authenticate(username=username, password=password)
                            login(request, alluser)
                            return redirect('admin', pk=mainuser.uuid)
                        else:
                            messages.info(request, 'Invalid details')
                    else:
                        messages.info(request, 'Invalid details')

            # ---- SIGNUP SECTION ----
            elif hidden == "True":
                usernamex = request.POST.get('username', '').strip()
                emailx = request.POST.get('email', '').strip()
                pass1x = request.POST.get('password2', '').strip()
                pass2x = request.POST.get('password', '').strip()
                acctype = request.POST.get('acctype', '')
                Currency = request.POST.get('Currency', '')

                email = emailx.replace(" ", "")
                username = usernamex.replace(" ", "_")
                pass1 = pass1x.replace(" ", "")
                pass2 = pass2x.replace(" ", "")

                if User.objects.filter(username__icontains=username, email__icontains=email).exists():
                    messages.error(request, 'User already exists')
                    return redirect('loginuser')
                else:
                    if pass1 == pass2:
                        alluser = User.objects.create(username=username, email=email)
                        mainuser = Client.objects.create(
                            approved=False,
                            Currency=Currency,
                            typeAcc=acctype,
                            password=pass1,
                            uuid=referCode(11),
                            Tancode=referCode(5),
                            AccountNUm=acc(),
                            user=alluser,
                            balance=0,
                            verified=False
                        )
                        login(request, alluser)
                        return redirect('Activate')
                    else:
                        messages.error(request, 'Passwords do not match!')
                        return redirect('loginuser')

        return render(request, 'html/login.html', c)

    except Exception as e:
        # This captures any unexpected errors
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('loginuser')

def resetpass(request):
    i = Site.objects.get(uuid=1)
    c = {
     'i':Site.objects.get(uuid=1)
    }
    return render(request,'html/fchangedpassword.html',c)
def Activate(request):
    i = Site.objects.get(uuid=1)
    mainuser = Client.objects.get(user=request.user)
    message = f'http://{request.get_host()}/linktoactivate/{mainuser.Tancode}/'
    c={
        'a':mainuser,
        'm':message,
        'v':i
    }
    
    email_sending(request,'mail/email.html',c,f"{i.name} Activation of Email ",mainuser.user.email.lower())
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'dashboard/activate.html',c)
def Activated(request):
    i = Site.objects.get(uuid=1)
    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'dashboard/Activated.html',c)
def linktoactivate(request, pk):
    i = Site.objects.get(uuid=1)
    
    c = {
    'i':Site.objects.get(uuid=1),
    }
    if Client.objects.filter(Tancode=pk).exists():
        c = Client.objects.get(Tancode=pk)
        c.approved = True
        c.tancode = genUdis(6)
        c.save()
        return redirect('Activated')
    else:
       return  HttpResponse('sorry expired')
    return  HttpResponse('something went wrong')
    

    
def forgotten(request):
    i = Site.objects.get(uuid=1) 
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username,email=email).exists():
            user = User.objects.get(username=username,email=email)
            use = Client.objects.get(user=user)
            email_sendingSINGLE(request,'PASSWORD RESET',f" Dear {user.username} your password is {use.password}",email) 
            messages.error(request,'Dear Customer Your password have been send to your email')
        else: 
            messages.error(request,'sorry Your detail is incorrect try again?')
            


    c = {
    'i':Site.objects.get(uuid=1),
    }
    return render(request,'html/forgottenpassword.html',c)

def logoutUser(request):
    logout(request )

    return redirect('loginuser')



#  dashboard
@login_required(login_url="loginuser")
def dashboard(request, pk):
    userc = Client.objects.get(uuid = pk)
    i = Site.objects.get(uuid=1)
    if  Client.objects.filter(uuid =pk, disabled=True).exists():
        c = {
           'a':request.user,
           'w':i
        }
        email_sending(request,'mail/blockedmail.html',c,f" Account Blocked#  ",userc.user.email)

        return redirect('disabledaccount')
    if  Client.objects.filter(uuid =pk, approved=False).exists():
        message = f'http://{request.get_host()}/linktoactivate/{userc.Tancode}/'


        c={
            'a':request.user,
            'm':message,
            'v':i
        }
        print('send')
        email_sending(request,'mail/email.html',c,f"{i.name} Activation of Email ",userc.user.email.lower())

        return redirect('Activate')

    ini =0
    inic =0
    d = userc.deposite.all().order_by('id')[:2]
    cv = userc.deposite.all().order_by('id')[:2]
    dc = userc.deposite.filter(statedecr='Credit')
    cc = userc.deposite.filter(statedecr='Debit')
    for dc in dc:
        ini += dc.amount
    for cc in cc:
        inic  += cc.amount
    pcash= ini
    dcash= inic
    print()

    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'dcash':dcash,
        'd':d,
        'd2':cv,

    }

    return render(request,'dashboard/dashboard.html',consc)
@login_required(login_url="loginuser")
def funding(request, pk):
    denied(request, pk)
    userc = Client.objects.get(uuid = pk)
    if request.method =="POST":
        account = request.POST['account']



    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'key':settings.PAYSTACK__PUB
    }

    return render(request,'dashboard/FUND.html',consc)
@login_required(login_url="loginuser")
def widthdrawalF(request, pk):
    denied(request, pk)
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    withto = Accwithdra.objects.filter(user=userc)
    if request.method =="POST":
        account = request.POST['account'] 
        amount = request.POST['amount']
        dis = request.POST['dis']
        vc = Accwithdra.objects.get(uuid = account)
        if account != "" and int(amount) >= 1000 < userc.balance :
            w = withdraw.objects.create(
            uuid=referCode(10),
            amount=amount,
            Accto=vc,
            date=datetime.today(),
            approved=False
            )
            userc.withdraw.add(w)
            messages.error(request,"Withdrawal Account sucessfully created")

        else:
             messages.error(request,"sorry check your balance or the amount you want to withdraw")
    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'key':settings.PAYSTACK__PUB,
        'withto':withto,
    }

    return render(request,'dashboard/paybill.html',consc)
@login_required(login_url="loginuser")

def AddwidthdrawalF(request, pk):
    denied(request, pk)
    userc = Client.objects.get(uuid = pk)

    if request.method =="POST":
        aname = request.POST['aname']
        Anumber = request.POST['Anumber']
        Bname = request.POST['Bname']
        if aname and Anumber:
            withto = Accwithdra.objects.create(
            user=userc,
            uuid = referCode(10),
            accountnumber = Anumber,
            bankname = Bname,
            name = aname
            )
            withto.save()
            messages.error(request,"Withdrawal Account sucessfully created")

        else:
             messages.error(request,"sorry input can not be empty")

    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'key':settings.PAYSTACK__PUB
    }

    return render(request,'dashboard/addpaybill.html',consc)

@login_required(login_url="loginuser")
def fundingf(request, pk):
    denied(request, pk)
    userc = Client.objects.get(uuid = pk)
    fund = True
    if request.method == "POST":
        amount = request.POST['amount']
        iss = request.POST['is']
        if amount:
            userc.balance = int(amount)
            d = deposite.objects.create(uuid=genUdis(12), date=datetime.today(), amount=amount,approved=True,statedecr='Credit')
            d.save()
            userc.save()
            userc.deposite.add(d)
            return redirect('successful2', pk =d.uuid)
    coc ={
        'fund':fund
    }
    return render(request,'dashboard/api.html',coc)
@login_required(login_url="loginuser")
def innertransfer(request, pk):
    userc = Client.objects.get(uuid = pk)
    i = Site.objects.get(uuid=1)
    if  Client.objects.filter(user =userc.user, disabled=True).exists():
        c = {
            'a':userc,
            'w':i
        }
        email_sending(request,'mail/blockedmail.html',c,f"Account Blocked ",userc.user.email)

        return redirect('disabledaccount')
    if request.method =="POST" and userc.disabled == False:
        amount = request.POST['amount']
        if int(userc.balance) >= int(amount) > 0:
            d =deposite.objects.create(uuid =referCode(10),date=datetime.today(),amount=amount,approved=False)
            return redirect ('finialtransfer', pk =d.uuid)
        else:
            messages.error(request,'Low Balance Fund Account To continue')
            return redirect ('innertransfer', pk =userc.uuid)
    pcash= userc.balance/100



    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/innerbanktransfer.html',consc)



@login_required(login_url="loginuser")
def finialtransfer(request, pk):
    i = Site.objects.get(uuid=1)
    userc = Client.objects.get(user=request.user)
    if  Client.objects.filter(uuid =pk, disabled=True).exists():
        c = {
           'a':request.user,
           'w':i
        }
        email_sending(request,'mail/blockedmail.html',c,f" Account Blocked#  ",userc.user.email.lower())

        return redirect('disabledaccount')
    d =deposite.objects.get(uuid =pk)
    if request.method == 'POST' and userc.disabled == False and   int(userc.balance) >= int(d.amount) > 0:
        bankname  = request.POST['bankname']
        accnumber  = request.POST['accnumber']
        holdernnm  = request.POST['holdernnm']
        country  = request.POST['country']
        currency  = request.POST['cur']
        swift  = request.POST['swift']
        disc  = request.POST['disc']
        BankAddress  = request.POST['BankAddress']
        d.holdername = holdernnm
        d.accountnumber = accnumber
        d.bankname = bankname
        d.BankCountry = country
        d.swiftcode = swift
        d.BankAddress = BankAddress
        d.Currency = currency
        d.statedecr = "Debit"
        if disc:
            d.disc= disc
            d.save() 
        userc.balance -= d.amount 
        userc.save()
        c = {
                'a':d,
                'w':userc,
                "i" : Site.objects.get(uuid=1)
            }
        email_sending(request,'mail/alertmail.html',c,f"DEBIT ALERT# {d.amount} ",request.user.email.lower())
        userc.deposite.add(d)
        d.save()


        return redirect('successful',pk= d.uuid)

    pcash= userc.balance/100
    
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'd':d,
    }

    return render(request,'dashboard/innerfinal.html',consc)
@login_required(login_url="loginuser")
def pending(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/pending.html',consc)
@login_required(login_url="loginuser")
def profile(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)
    print(userc.scretqestion)
    if request.method =="POST":
        pin = request.POST['pin']
        sq = request.POST['secretequese']
        sa = request.POST['secretequeseasd']
        firstname = request.POST['firstname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        if pin  and  firstname and phone != None and sa != None and sq !=None :
            if userc.Pin == pin:
                userc.user.username= username
                userc.user.first_name= firstname
                userc.user.email=email
                print(userc.user.first_name)
                userc.scretqestion=sq
                userc.scretanswer=sa
                userc.Phone=phone
                userc.save()
                userc.user.save()
                messages.error(request,'Updated Successfully')
            else:
                messages.error(request,'Sorry the pin is incorrect ')
        else:
            messages.error(request,'input can not be empty')

        # sa = request.POST['secretequese']


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/profile.html',consc)
def security(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    if request.method =="POST":
        pin = request.POST['pin']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        passc = request.POST['passc']
        if passc == userc.password :
            if pass1 == pass2:
                userc.password = pass1
                userc.Pin = pin or userc.Pin
                userc.save()
                messages.error(request,'sucessfully updated')
            else:
                messages.error(request,'password mismatched')
        else:
            messages.error(request,'your current password is incorrect')
    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/security.html',consc)
def loanpend(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/pending.html',consc)
def pinuser(request, pk):
    if  Client.objects.filter(uuid =pk, disabled=True).exists():
        c = {
           'a':request.user,
           'w':i
        }
        email_sending(request,'mail/blockedmail.html',c,f" Account Blocked#  ",userc.user.email.lower())

        return redirect('disabledaccount')
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    if request.method == "POST":
        pin = request.POST['pin']
        if pin :
            userc.Pin = pin
            userc.save()
            return redirect('dashboard', pk=userc.uuid)
        else:
            messages.error(request,'Sorry the pin is empty / is less or more that 4 ')


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/pin.html',consc)
def loanform(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/loanForm.html',consc)
def widthdrawalcheck(request, pk):
    userc = Client.objects.get(user=request.user)
    d =withdraw.objects.get(uuid =pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':d,
        'pcash':pcash
    }

    return render(request,'dashboard/successful22.html',consc)
def widthdrawalhistory(request, pk):
    userc = Client.objects.get(user=request.user)
    d =userc.withdraw.all()
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':d,
        'pcash':pcash
    }

    return render(request,'dashboard/historypaybill.html',consc)
def successful2(request, pk):
    userc = Client.objects.get(user=request.user)
    d =deposite.objects.get(uuid =pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':d,
        'pcash':pcash
    }

    return render(request,'dashboard/successful2.html',consc)
def btchistory(request, pk):
    userc = Client.objects.get(user=request.user)

    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    btc = userc.userBtcpay.all().order_by('id')
    if request.method =="POST":
        search = request.POST['p']
        if search:
            print(f"{search}")

            if userc.userBtcpay.filter(uuid__startswith = search).exists():
                btc= userc.userBtcpay.filter( uuid__startswith = search)
            else:

                messages.info(request, 'Empty....')
    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':btc,
        'pcash':pcash
    }

    return render(request,'dashboard/btchis.html',consc)
def successful(request, pk):
    userc = Client.objects.get(user=request.user)
    d =deposite.objects.get(uuid =pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)


    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':d,
        'pcash':pcash
    }

    return render(request,'dashboard/successful.html',consc)

def Accountsum(request, pk):
    userc = Client.objects.get(uuid=pk)
    d = userc.deposite.all().order_by('-date')
    btc = userc.userBtcpay.all().order_by('id')
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    if  Client.objects.filter(uuid =pk, disabled=True).exists():
        c = {
           'a':request.user,
           'w':i
        }
        email_sending(request,'mail/blockedmail.html',c,f" Account Blocked#  ",userc.user.email.lower())

        return redirect('disabledaccount')
    if request.method =="POST":
        search = request.POST['p']
        if search:
            print(f"GXB/{search[3:]}")
            lookup= ( Q( statedecr=search or '' ) | Q(disc__startswith=search or '' ) | Q(uuid__startswith = search[4:] or ''))
            if userc.deposite.filter(lookup).exists():
                d= userc.deposite.filter(Q( statedecr=search or '' ) | Q(disc__startswith = search or '' )| Q(uuid__startswith = search[4:] or '' ))
            else:

                messages.info(request, 'Empty....')



    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'd':d,
        'b':btc,
        'pcash':pcash
    }

    return render(request,'dashboard/pending.html',consc)
def Checkdepositx(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    if request.method == "POST":
        amount = request.POST['amount']
        front = request.POST['front']
        back = request.POST['back']
        date = request.POST['date']
        dc = Depositchecking.objects.create(amount=amount  ,approved=False, front=front  , back=back  , date=date
        )
        userc.depositeckecked.add(dc)
        dc.save()
        userc.save()
        messages.info(request, 'Request under Review.. ')

    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/depositecheck.html',consc)
def samebank(request, pk):
    userc = Client.objects.get(uuid = pk)
    allp = Client.objects.all()
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    if request.method == "POST":
        account  = request.POST['account']
        pin  = request.POST['pin']
        amount  = request.POST['amount']
        if pin and amount and amount:
            if userc.Pin == pin:
                if int(amount) <= userc.balance >= 1000 :

                    if Client.objects.filter(AccountNUm=account).exists():
                        allp = Client.objects.get(AccountNUm=account)
                        d = deposite.objects.create(date=datetime.today(),uuid=genUdis(8),amount=amount,approved=True,holdername=allp.user.username,accountnumber=account,statedecr="Debit",bankname=i.name,disc='Domestic Transfer')
                        dc = deposite.objects.create(date=datetime.today(),uuid=genUdis(6),amount=amount,approved=True,holdername=request.user.username,accountnumber=account,statedecr="Credit",bankname=i.name,disc='Domestic Transfer')
                        allp.balance += int(amount)
                        allp.deposite.add(dc)
                        userc.deposite.add(d)
                        userc.balance -= int(amount)
                        allp.save()
                        userc.save()
                        return redirect('successful', pk = d.uuid)
                    else:
                        messages.info(request, 'sorry the Account Number is inValid  ')

                else:
                    messages.info(request, 'sorry insufficient Balance  ')
            else:
                messages.info(request, 'sorry Incorrect Pin try again  ')
        else:
            messages.info(request, 'sorry the input form can not be empty ')






    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash
    }

    return render(request,'dashboard/sameBnk.html',consc)
def Btcpay(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    btc= Btc.objects.all()
    if request.method =="POST":
        wallet = request.POST['wallet']
        prof = request.POST['convertc']
        amount = request.POST['amount']
        if prof:
            btcx= Btc.objects.filter(address= wallet).first()
            btcxx= Btcpayin.objects.create(
                btcname= btcx,
                uuid= f"{btcx.name}/{genUdis(8)}",
                prof= prof,
                approved= False,
                amount= amount,
            )
            btcxx.save()
            userc.userBtcpay.add(btcxx)
            return redirect('btchistory', pk=userc.uuid)



    # Btcpayin.objects.all()
    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'btc':btc,
    }

    return render(request,'dashboard/btcPayment.html',consc)
def kycD(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)

    forms = kycimgc()
    vc = False
    if Kycdb.objects.filter(cardUser=userc).exists():
        cx=Kycdb.objects.get(cardUser=userc)

        if cx.active == True:
            vc='True'
        elif cx.front:
            vc='Truec'

    k =None
    if not Kycdb.objects.filter(cardUser=userc) :
        k = None
    elif Kycdb.objects.filter(cardUser=userc):
        k=Kycdb.objects.get(cardUser=userc)
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        city = request.POST.get('city')
        Nationality = request.POST.get('Nationality')
        Bdate = request.POST.get('Bdate')
        ZipCode = request.POST.get('zipcode')
        email = request.POST.get('email')
        interPimg = request.POST.get('ini')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        Phone = request.POST.get('Phone')
        back = request.POST.get('back')
        front = request.POST.get('front')


        c=Kycdb.objects.filter(cardUser=userc)
        if c:
            for c in c:
                c.delete()
        kycx = Kycdb.objects.create(uuid=genUdis(6),cardUser= userc, back=back,    front=front,ZipCode=ZipCode,Nationality=Nationality,City =city,Idname=interPimg,AddressLine1=add1,AddressLine2=add2, active=False)

        userc.user.first_name=firstname
        userc.user.last_name=lastname
        userc.Bdate=Bdate
        userc.user.email=email
        userc.Phone=Phone
        userc.save()
        messages.info(request, 'Send successfully ')



    consc = {
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'pcash':pcash,
        'form':forms,
        'k':k,
        'vc':vc,
    }

    return render(request,'dashboard/kycDEetail.html',consc)
def Kyc(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)



    subject = 'kYC '
    redi = f'/kycD/{userc.uuid}/'
    btn = 'Upload KYC '
    p = 'specially designed for your online transaction .'
    i = 'bi-file-person'
    p2 ='make sure that the file you upload are clear and up to data to avold issues'
    cons = {
        'p2':p2,
        'i':Site.objects.get(uuid=1),
        'p':p,
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'subject':subject,
        'btn':btn,
        'btn':btn,
        'redi':redi,
        'pcash':pcash
    }
    return render(request,'dashboard/virtualcard.html',cons)
def loancover(request, pk):
    userc = Client.objects.get(uuid = pk)
    pcash= userc.balance/100
    i = Site.objects.get(uuid=1)



    subject = 'Request for a loan'
    btn = 'Request For A New Virtual Card'
    btn = 'Request For A New Virtual Card'
    p = 'specially designed for your online transaction .'
    i = 'bi-person'
    p2 ='Lorem Ipsum Dolor Sit Amet Consectetur Adipisicing Elit. Minima Alias Deserunt Ullam! Architecto Unde Incidunt Iste, Similique Tenetur Nihil Maiores Quidem Consequuntur Porro, Commodi Tempora! Temporibus, Praesentium. Quidem, Ut Nobis?'
    cons = {
        'p2':p2,
        'i':Site.objects.get(uuid=1),
        'p':p,
        'user':userc,
        'i':Site.objects.get(uuid=1),
        'subject':subject,
        'btn':btn,
        'pcash':pcash
    }
    return render(request,'dashboard/virtualcard.html',cons)


def deleteuserc(request, pk):
    de = Client.objects.get(uuid = pk)
    de.delete()
    userc = Client.objects.get(user = request.user)
    messages.info(request, 'Deleted successfully ')
    return redirect('admin', pk=userc.uuid)



@login_required(login_url="loginuser")
def adminauth(request,pk):
    userc = Client.objects.get( user=request.user)
    alluser=None
    if request.user.is_superuser == True:
        userc = Client.objects.get(uuid = pk)
        alluser= Client.objects.all().exclude(user=userc.user )

    else:
        return redirect('loginuser')

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'userad':alluser,
    }
    return render(request,'adminC/html/admin_dashboard.html',consc)

def adminauthedit(request,pk):
    userc = Client.objects.get( user=request.user)
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = deposite.objects.get(uuid = pk)
    cx = depositeForm(instance=usercd)
    if request.method == 'POST':
        cx = depositeForm(request.POST,instance=usercd)

        if request.POST:

            if cx.is_valid():
                cx.save()
            messages.info(request, 'Updated successfully ')
            return redirect('adminauthedit', pk=pk)




    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'd':usercd,
    'date':cx,
    }


    return render(request,'adminC/html/edittrans.html', consc)
def personalsecurity(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = Client.objects.get(uuid = pk)
    userc = Client.objects.get( user=request.user)
    security(request, pk)

    consc = {
    'i':usercd,
    'user':userc,
    'i':Site.objects.get(uuid=1),
    }

    return render(request,'adminC/html/personalsecurity.html',consc)
def adminautheditpersonal(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = Client.objects.get(uuid = pk)
    userc = Client.objects.get( user=request.user)
    profile(request, pk)
    consc = {
    'i':usercd,
    'user':userc,
    'i':Site.objects.get(uuid=1),
    }

    return render(request,'adminC/html/personal.html',consc)
def allptrandeleteall(request, pk):

    m = deposite.objects.all().order_by('id')
    if m:
        m.delete()
        messages.info(request, 'Deleted successfully ')
    return redirect('alltran' ,pk = pk)
def allptrandelete(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    userc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('alltran' ,pk = cc)
def allptranapproved(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    userc.approved = True
    s = Client.objects.filter(deposite__uuid = pk)
    for i in s:
        if userc.statedecr == 'Debit':
             
            i.save()
        else:
            i.balance += userc.amount
            i.save()

        userc.save()
        messages.info(request, 'Approved successfully ')

    return redirect('alltran' ,pk = cc)
def alldisptranapproved(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    userc.approved = False
    s = Client.objects.filter(deposite__uuid = pk)

    for i in s:

        if userc.statedecr == 'Debit':
            i.balance += userc.amount
            i.save()
        else:
            
            i.save()
    userc.save()
    messages.info(request, 'Declined successfully ')
    return redirect('alltran' ,pk = cc)
def ptrandeleteall(request, pk):
    sc = Client.objects.get(uuid = pk)
    m = sc.deposite.all()
    for s in m:
        m.delete()
        messages.info(request, 'Deleted successfully ')
        return redirect('ptran' ,pk = pk)
def ptrandelete(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    userc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('ptran' ,pk = cc)
def deleteaccom(request, pk, cc):
    userc = Accwithdra.objects.get(uuid = pk)
    userc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('allaccountwithdrawAL' ,pk = cc)
def ptranapproved(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    s = Client.objects.filter(deposite__uuid = pk)
    for i in s:
        if userc.statedecr == 'Debit':
            
            userc.approved = True

            i.save()
            c = {
                'a':userc,
                'w':i,
                "i" : Site.objects.get(uuid=1)
            }
            email_sending(request,'mail/alertmail.html',c,f"DEBIT ALERT# {d.amount} ",i.user.email.lower())
        else:
            userc.approved = True
 
            
            i.save()
            c = {
                'a':userc,
                'w':i,
                "i" : Site.objects.get(uuid=1)
            }
            email_sending(request,'mail/alertmail.html',c,f"CREDIT ALERT# {d.amount} ",i.user.email)

    userc.save()
    messages.info(request, 'Approved successfully ')

    return redirect('ptran' ,pk = cc)
def disptranapproved(request, pk, cc):
    userc = deposite.objects.get(uuid = pk)
    userc.approved = False
    s = Client.objects.filter(deposite__uuid = pk)

    for i in s:

        if userc.statedecr == 'Debit':
            
            i.save()
            c = {
                'a':d,
                'w':userc,
                "i" : Site.objects.get(uuid=1)
            }
            email_sending(request,'mail/alertmail.html',c,f"CREDIT ALERT# {d.amount} ",i.user.email)
        else:
            i.balance -= userc.amount
            i.save()
            c = {
                'a':d,
                'w':userc,
                "i" : Site.objects.get(uuid=1)
                }
            email_sending(request,'mail/alertmail.html',c,f"DEBIT ALERT# {d.amount} ",i.user.email)
    userc.save()
    messages.info(request, 'Declined successfully ')
    return redirect('ptran' ,pk = cc)

def alltran(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = Client.objects.get(uuid = pk)
    usertran = deposite.objects.all().order_by('id')
    userc = Client.objects.get( user=request.user)

    consc = {
    'i':usercd,
    'user':userc,
    'ix':Site.objects.get(uuid=1),
    't':usertran
    }

    return render(request,'adminC/html/alltrans.html',consc)
def ptran(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = Client.objects.get(uuid = pk)
    usertran = usercd.deposite.all()
    userc = Client.objects.get( user=request.user)

    consc = {
    'i':usercd,
    'user':userc,
    'ix':Site.objects.get(uuid=1),
    't':usertran
    }

    return render(request,'adminC/html/personaltranscation.html',consc)
def allaccountwithdrawAL(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    usercd = Client.objects.get(uuid = pk)
    usertran = usercd.deposite.all()
    usertran = Accwithdra.objects.filter( user =usercd)
    userc = Client.objects.get( user=request.user)

    consc = {
    'i':usercd,
    'user':userc,
    'ix':Site.objects.get(uuid=1),
    't':usertran
    }

    return render(request,'adminC/html/with.html',consc)
    
import random    

def funuser(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    banks = ["Bank of America", "JPMorgan Chase", "Wells Fargo", "Citibank", "Goldman Sachs"] 
    random_bank = random.choice(banks)    
    userc = Client.objects.get(uuid = pk)
    alls = Client.objects.all()
    if request.method =='POST':
        amount=request.POST['amount']
        useid=request.POST['Account']
        date=request.POST['date']
        dis=request.POST['dis']
        Type=request.POST['Type']
        bv = Client.objects.get(uuid=useid)
        if Type !="" and Type=='Credit':
            bv.balance += int(amount)

            x = deposite.objects.create(
                uuid=referCode(12),
                amount=int(amount),
                date= date or datetime.today() ,
                approved =True,
                holdername = bv.user.username,
                accountnumber=bv.AccountNUm,
                statedecr = Type,
                disc = dis,
                bankname = random_bank,
            )
            bv.deposite.add(x)
            bv.save()
            messages.info(request, f' successfully  credited {amount} to {bv.user.username } account ')
        elif Type !="" and Type=='Dedit' and bv.balance >= int(amount):
            x = deposite.objects.create(
                uuid=referCode(12),
                amount=int(amount),
                date=datetime.today(),
                disc = dis,
                approved =True,
                holdername = bv.user.username,
                accountnumber=bv.AccountNUm,
                statedecr = Type,
                bankname = 'GX-Bank',
            )
            bv.balance -= int(amount)
            bv.deposite.add(x)
            bv.save()
            messages.info(request, f' successfully Debited {amount} to {bv.user.username } account ')


        return redirect('funuser', pk=pk)

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':alls,
    }

    return render(request,'adminC/html/FUNDuser.html',consc)
def senduser(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc2 = Btcpayin.objects.get(id = pk)
    userc = Client.objects.get(user=request.user)
    allsd = Client.objects.all()
    cv = None
    print(str(userc2.uuid))
    for ic in allsd :
        if ic.userBtcpay.filter(id = pk).exists():
            cv = ic

        # for vc in vc:

        #     print('dfjfkfk',vc.uuid)
        # print(ic.userBtcpay.filter(id = 1))


    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1), 
    'c':userc2,
    'z':cv,
    }

    return render(request,'adminC/html/unisbtc.html',consc)

@login_required(login_url="loginuser")
def senduserbtcview(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    allkyc = Btcpayin.objects.all()

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc,
    }

    return render(request,'adminC/html/btc1.html',consc)
@login_required(login_url="loginuser")
def senduserkcyview(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(uuid = pk)
    allkyc = Kycdb.objects.all()

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc,
    }

    return render(request,'adminC/html/kyc1.html',consc)
@login_required(login_url="loginuser")
def checkdepositeadmin(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(uuid = pk)
    allkyc = Depositchecking.objects.all().order_by('id')

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc,
    }

    return render(request,'adminC/html/check1.html',consc)

def allbtcdelete(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Btcpayin.objects.all()
    if usercc:
        usercc.delete()
        messages.info(request, 'Deleted successfully ')
    return redirect('senduserbtcview', userc.uuid)

def allkycdelete(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Kycdb.objects.all()
    if usercc:
        usercc.delete()
        messages.info(request, 'Deleted successfully ')
def allcheckdelete(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Depositchecking.objects.all()
    if usercc:
        usercc.delete()
        messages.info(request, 'Deleted successfully ')
    return redirect('checkdepositeadmin', userc.uuid)
def deletebtc(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Btcpayin.objects.get(id = pk)
    usercc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('senduserbtcview', userc.id)
def deletecheck(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Depositchecking.objects.get(id = pk)
    usercc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('checkdepositeadmin', userc.uuid)
def approvedcheck(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')

    userc = Client.objects.get(user = request.user)
    allsd = Client.objects.all()
    usercc = Depositchecking.objects.get(id = pk)
    if usercc.approved != True:
        usercc.approved = True
        for c in allsd:
            if c.depositeckecked.filter(id = pk).exists():
                c.depositeckecked.get(id = pk)
                c.balance+= int(usercc.amount)
                c.save()

        usercc.save()
        messages.info(request, 'approved successfully ')
    else:
        messages.info(request, 'Already been approved successfully ')
    return redirect('checkdepositeadmin', userc.uuid)
def approvedbtc(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')

    userc = Client.objects.get(user = request.user)
    allsd = Client.objects.all()
    usercc = Btcpayin.objects.get(id = pk)
    if usercc.approved != True:
        usercc.approved = True
        for c in allsd:
            if c.userBtcpay.filter(id = pk).exists():
                c.userBtcpay.get(id = pk)
                c.balance+= int(usercc.amount)
                c.save()
        usercc.save()
        messages.info(request, 'approved successfully ')
    else:
        messages.info(request, 'Already been approved successfully ')
    return redirect('senduserbtcview', usercc.id)

def deletekyc(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Kycdb.objects.get(uuid = pk)

    usercc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('senduserkcyview', userc.uuid)
def deletekyc(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Kycdb.objects.get(uuid = pk)

    usercc.delete()
    messages.info(request, 'Deleted successfully ')
    return redirect('senduserkcyview', userc.uuid)
def approvedkyc(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Kycdb.objects.get(uuid = pk)
    usercc.approved = True
    usercc.save()
    messages.info(request, 'approved successfully ')
    return redirect('senduserkcy', usercc.uuid)

def sendusercheck(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Depositchecking.objects.get(id = pk)
    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'v':usercc,
    }

    return render(request,'adminC/html/checkdopsite.html',consc)
def senduserkcy(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    usercc = Kycdb.objects.get(uuid = pk)
    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'v':usercc,
    }

    return render(request,'adminC/html/kyc.html',consc)
def createwalletcrypto(request, pk):
    userc = Client.objects.get(user = request.user)
    allkyc = Btc.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        wallet  = request.POST['wallet']
        if name and wallet:
            s = Btc.objects.create(
                name=name,
                address=wallet,
                active=True,
                date=datetime.today()
            )
            messages.info(request, f'{s.name} wallet  sucessfully created ')
    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc,
    }
    return render(request,'adminC/html/createwallet.html', consc)
def createwalletedite(request, pk):
    userc = Client.objects.get(user = request.user)
    als = Btc.objects.get(id=pk)
    up = updatebtcForm(instance=als)
    if request.method == "POST":
        up = updatebtcForm(request.POST,instance=als)
        if up.is_valid():
            up.save()


            messages.info(request, f'{als.name} wallet  sucessfully Updated ')

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':als,
    'up':up,
    }
    return render(request,'adminC/html/createwalletedite.html', consc)
def BtchistoryV(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)
    allkyc = Btc.objects.all().order_by('id')

    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc,
    }

    return render(request,'adminC/html/btc1his.html',consc)
def EditeSite(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')
    userc = Client.objects.get(user = request.user)

    allkyc2=None
    if Site.objects.filter(uuid=1).exists():
        allkyc2 = Site.objects.get(uuid = 1)
        if request.method =='POST':
            name = request.POST['name']
            loaction = request.POST['location']
            email = request.POST['email']
            logo = request.POST['logo']
            adder = request.POST['adder']
            desc = request.POST['desc']
            if desc and logo:
                allkyc2.uuid=1
                allkyc2.name=name
                allkyc2.location=loaction
                allkyc2.email = email
                allkyc2.desc=desc
                allkyc2.addressLine2=adder
                allkyc2.logo = logo
                allkyc2.save()
    else:
        if request.method =='POST':
            name = request.POST['name']
            loaction = request.POST['location']
            email = request.POST['email']
            logo = request.POST['logo']
            adder = request.POST['adder']
            desc = request.POST['desc']
        if request.POST:
            allkyc = Site.objects.create(
                uuid=1,
                name=name,
                location=loaction,
                email = email,
                desc=desc,
                addressLine2=adder,
                logo = logo,
            )
            allkyc.save()
            messages.info(request,   'sucessfully Updated ')

            return redirect('EditeSite', pk=pk)


    consc = {
    'user':userc,
    'i':Site.objects.get(uuid=1),
    'o':allkyc2,
    }

    return render(request,'adminC/html/aboutsite.html',consc)



def approvedx(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')

    als = Btc.objects.get(id=pk)
    userc = Client.objects.get(user = request.user)
    als.active = True
    als.save()
    messages.info(request, f'{als.name} wallet  sucessfully Updated ')
    return redirect('BtchistoryV',pk = userc.uuid)
def deltex(request,pk):
    if not request.user.is_superuser:
        return redirect('loginuser')

    userc = Client.objects.get(user = request.user)

    als = Btc.objects.get(id=pk)
    als.delete()
    messages.info(request, f'{als.name} wallet  sucessfully Deleted ')
    return redirect('BtchistoryV',pk = userc.uuid)
