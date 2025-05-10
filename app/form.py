from django import forms


from .models import *

class deposites(forms.ModelForm):
    class Meta:
        model = deposite
        fields = ['img']
class kycimgc(forms.ModelForm):
    class Meta:
        model = Kycdb
        fields = ['front','back']

class depositeForm(forms.ModelForm):
    class Meta:
        model = deposite
        fields = ['uuid','date', 'amount', 'approved' ,'accountnumber','statedecr','bankname','disc',
        
        ]
class updatebtcForm(forms.ModelForm):
    class Meta:
        model = Btc
        fields = [
            'date', 
            'name', 
            'address', 
            'active', 
        
        ]


    
