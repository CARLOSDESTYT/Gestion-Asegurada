from django.core.management.base import BaseCommand
from clientes.models import Poliza
from datetime import date, timedelta
from pywa import WhatsApp
from pywa.types import Template

class Command(BaseCommand):
    help = 'Envía recordatorios por WhatsApp usando pywa'

    def handle(self, *args, **kwargs):
        # Configuración de pywa api
        wa = WhatsApp(
            phone_id="TU_PHONE_ID",
            token="TU_ACCESS_TOKEN"
        )

        hoy = date.today()
        objetivo = hoy + timedelta(days=30)
        
        # filtro pólizas que vencen en 30 días
        polizas = Poliza.objects.filter(estatus='Activa')
        
        for p in polizas:
            if p.proxima_renovacion == objetivo:
                try:
                    # plantilla 'recordatorio_vencimiento'
                    # ajustar variables de la plantila q apruebe meta
                    wa.send_template(
                        to=p.cliente.telefono,
                        name="recordatorio_vencimiento",
                        language="es",
                        components=[
                            Template.Body(parameters=[
                                Template.Text(p.cliente.nombre),
                                Template.Text(p.tipo_seguro)
                            ])
                        ]
                    )
                    self.stdout.write(self.style.SUCCESS(f'WhatsApp enviado a {p.cliente.nombre}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error con {p.cliente.nombre}: {e}'))