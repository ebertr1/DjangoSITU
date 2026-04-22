from django import forms
from .models import Pasajero
from .models import Tarjeta
class PasajeroFormulario(forms.ModelForm):
	class Meta:
		model = Pasajero
		fields=["cedula","nombre","apellido", "email","imagen"] 
		#fields = '__all__'
from .models import Tarjeta

from django import forms
from .models import Tarjeta

class TarjetaFormulario(forms.ModelForm):

    class Meta:
        model = Tarjeta
        fields = ["monto", "idPasajero"]  # 🔥 quitamos codigo