from django.shortcuts import render
from .forms import PasajeroFormulario
from .models import Pasajero
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Tarjeta, Viaje, SimularAccesoPago, Bus
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Tarjeta
from .models import Tarjeta
from .forms import TarjetaFormulario

def home_view(request):
    return render(request,"index.html",{})
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Tarjeta
from django.shortcuts import redirect

def tarjeta(request):
    if request.method == "POST":
        form = TarjetaFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarjeta")  # 🔥 IMPORTANTE

    form = TarjetaFormulario()
    tarjetas = Tarjeta.objects.all()  # 🔥 SIEMPRE RECARGA DATOS

    return render(request, "tarjeta.html", {
        "form": form,
        "tarjetas": tarjetas
    })
def recargar_saldo(request, id):
    tarjeta = get_object_or_404(Tarjeta, id=id)

    if request.method == "POST":
        monto_recarga = float(request.POST.get("monto"))

        saldo_actual = float(tarjeta.monto)
        tarjeta.monto = str(saldo_actual + monto_recarga)
        tarjeta.save()

        messages.success(request, "Saldo recargado correctamente ✅")
        return redirect("tarjeta")

    return render(request, "recargar.html", {"tarjeta": tarjeta})
def pasajeros(request):
    pasajeros = Pasajero.objects.all()
    form = PasajeroFormulario()

    if request.method == 'POST':
        form = PasajeroFormulario(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pasajeros')

    return render(request, "pasajeros.html", {
        "pasajeros": pasajeros,
        "form": form
    })
def pasajerosEdit(request, id):
    pasajeros = get_object_or_404(Pasajero, id = id)
    data = {
        'form' : PasajeroFormulario(instance=pasajeros)
    }
    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, instance=pasajeros, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")

    return render(request,'pasajerosEdit.html',data)
from django.contrib import messages
from .models import Tarjeta, Viaje, SimularAccesoPago, Bus

def simular_pago(request):
    tarjetas = Tarjeta.objects.all()
    buses = Bus.objects.all()

    if request.method == "POST":
        tarjeta_id = request.POST.get("tarjeta")
        bus_id = request.POST.get("bus")
        costo = float(request.POST.get("costo"))

        tarjeta = Tarjeta.objects.get(id=tarjeta_id)
        bus = Bus.objects.get(id=bus_id)

        saldo = float(tarjeta.monto)

        # Validación de saldo
        if saldo < costo:
            messages.error(request, "Saldo insuficiente ❌")
        else:
            # descontar saldo
            tarjeta.monto = str(saldo - costo)
            tarjeta.save()

            # crear viaje
            viaje = Viaje.objects.create(
                pasajero=tarjeta.idPasajero,
                bus=bus,
                costo=costo,
                cantidad=1,
                efectivo=False
            )

            # registrar acceso
            SimularAccesoPago.objects.create(
                numero=bus.numero,
                viaje=viaje,
                tarjeta=tarjeta
            )

            messages.success(request, "Pago realizado correctamente ✅")

    return render(request, "simular_pago.html", {
        "tarjetas": tarjetas,
        "buses": buses
    })