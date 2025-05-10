from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    typeAcc = models.CharField(max_length=50,blank=True, null=True)
    Currency = models.CharField(max_length=50,blank=True, null=True)
    scretqestion = models.CharField(max_length=50,blank=True, null=True)
    scretanswer = models.CharField(max_length=50,blank=True, null=True)
    token = models.CharField(max_length=50,blank=True, null=True)
    AccountNUm = models.BigIntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    Bdate = models.DateField(blank=True, null=True)
    Phone = models.CharField(max_length=50,blank=True, null=True)
    swiftcode = models.CharField( max_length=50,blank=True)

    otp = models.IntegerField(blank=True, null=True)
    verified = models.BooleanField()
    Tancode = models.BigIntegerField( max_length=50,blank=True, null=True)
    Pin = models.CharField( max_length=50,blank=True, null=True)
    deposite = models.ManyToManyField("deposite",blank=True,)
    userBtcpay = models.ManyToManyField("Btcpayin",blank=True,)
    depositeckecked = models.ManyToManyField("Depositchecking",blank=True,)
    approved = models.BooleanField(default= False, )
    disabled  = models.BooleanField(default= False)

    withdraw = models.ManyToManyField("withdraw",blank=True,)
    uuid = models.CharField( max_length=50,blank=True)
    password = models.CharField( max_length=50,blank=True, null=True)
    seftcode = models.CharField( max_length=50,blank=True, null=True)
    def __str__(self):
        return f"{self.user.username } -------and -----{self.balance}"

class Accwithdra(models.Model):
    date = models.DateTimeField( auto_now_add=True)
    user = models.ForeignKey(Client, on_delete=models.CASCADE,blank=True,null=True)
    uuid = models.CharField( max_length=50)
    accountnumber = models.CharField( max_length=50,blank=True)
    bankname = models.CharField( max_length=50,blank=True)
    name = models.CharField( max_length=50,blank=True)
    disc = models.CharField( max_length=50,blank=True)
    def __str__(self):
        return self.uuid

class deposite(models.Model):
    date = models.DateTimeField( auto_now_add=False)
    uuid = models.CharField( max_length=50)
    amount = models.IntegerField()
    img = models.FileField( upload_to='deposit/',  blank=True)
    approved = models.BooleanField()
    BankCountry = models.CharField( max_length=50,blank=True)
    BankAddress = models.CharField( max_length=50,blank=True)
    holdername = models.CharField( max_length=50,blank=True)
    swiftcode = models.CharField( max_length=50,blank=True)
    accountnumber = models.CharField( max_length=50,blank=True)
    Currency = models.CharField( max_length=50,blank=True)
    statedecr = models.CharField( max_length=50,blank=True)
    bankname = models.CharField( max_length=50,blank=True)
    disc = models.CharField( max_length=50,blank=True)
    def __str__(self):
        return self.uuid

class withdraw(models.Model):
    date = models.DateTimeField( auto_now_add=False)
    uuid = models.CharField( max_length=50)
    amount = models.IntegerField()
    Accto = models.ForeignKey('Accwithdra', on_delete=models.CASCADE,blank=True,null=True)

    approved = models.BooleanField()


    def __str__(self):
        return self.uuid
class Depositchecking (models.Model):
    date = models.DateTimeField( )
    amount = models.IntegerField(blank=True, null=True)
    front = models.TextField( blank=True)
    back = models.TextField( blank=True)
    approved = models.BooleanField(blank=True, null=True)



    def __str__(self):
        return str(self.date )
class APIfetch(models.Model):
    date = models.DateTimeField( auto_now_add=True)
    name = models.CharField( max_length=50,blank=True)
    nameS = models.CharField( max_length=50,blank=True)



    def __str__(self):
        return self.name
class Btc(models.Model):
    date = models.DateTimeField( )
    name = models.CharField( max_length=50,blank=True)
    address = models.CharField( max_length=50,blank=True)
    img = models.FileField(  upload_to='btc', blank=True)
    active=models.BooleanField()
class Btcpayin(models.Model):
    btcname = models.ForeignKey(Btc, on_delete=models.CASCADE)
    uuid = models.CharField( max_length=50)
    amount = models.CharField(blank=True, null=True, max_length=50)
    date = models.DateTimeField( auto_now_add=True)
    prof = models.TextField(  blank=True)
    approved=models.BooleanField(blank=True, null=True)




    def __str__(self):
        return self.uuid





class Kycdb(models.Model):
    cardUser = models.ForeignKey('Client', on_delete=models.CASCADE,blank=True, null=True)
    date = models.DateTimeField( auto_now_add=True)
    uuid = models.CharField( max_length=50,blank=True )
    ZipCode = models.CharField( max_length=50,blank=True )
    Nationality = models.CharField( max_length=50,blank=True )
    City = models.CharField( max_length=50,blank=True )
    Idname = models.CharField( max_length=50,blank=True)
    AddressLine1 = models.CharField( max_length=50,blank=True,null=True)
    AddressLine2 = models.CharField( max_length=50,blank=True,null=True)
    front = models.TextField( blank=True , null=True  )
    back = models.TextField( blank=True  , null=True )
    def uuidgen ():
        if self.uuid == "":
           self.uuid = genUdis()
           self.uuid.save()


    active = models.BooleanField()


    def __str__(self):
        return self.uuid










class Site(models.Model):
    uuid = models.CharField( max_length=50,blank=True )
    date = models.DateTimeField( auto_now_add=True)
    name = models.CharField( max_length=50,blank=True )
    location  = models.CharField( max_length=50,blank=True )
    email = models.CharField( max_length=50,blank=True)
    desc = models.CharField( max_length=50,blank=True,null=True)
    addressLine2 = models.CharField( max_length=50,blank=True,null=True)
    logo = models.TextField( blank=True  , null=True )

    def __str__(self):
        return self.name









