from django.forms import ModelForm, forms
from .models import Game
from .models import WishList

class GameForm(ModelForm):      #Create a class/form object. Inherit information via ModelForm django mehtod.
    class Meta:                 #Define its meta information:
        model = Game            #Connect this ModelForm the the model object defined in mainapp/models.py
        fields = '__all__'      #'__all__' is a dunder shortcut to grab all the fields within the Product model, define in products/models.pyclass AccountForm(ModelForm):    #inherit information from ModelForm

class WishListForm(ModelForm):
    class Meta:                 # Define its meta information:
        model = WishList        # Connect this ModelForm the model object defined in mainapp/models.py
        fields = '__all__'      # '__all__' is a dunder shortcut to grab all the fields within the Product model, define in products/models.pyclass AccountForm(ModelForm):    #inherit information from ModelForm
