import pywhatkit as kit
from datetime import datetime, timedelta
import time


class WhatsAppManager:
    def __init__(self):
        # Configuración del "consultorio médico"
        self.nombre_doctor = "Dr. Jose Elias Cuevas Torres"
        self.nombre_clinica = "Clínica San Elias"
        self.direccion = "Av. Luis Cortazar 123, El Colorado"
        self.telefono_clinica = "+52 461 123 4567"

    def agendar_cita(self, numero_destino):
        try:
            # Generar datos de la cita
            fecha_cita, hora_cita = self.generar_fecha_hora_cita()

            # Crear mensaje de confirmación
            mensaje = self.crear_mensaje_cita(fecha_cita, hora_cita)

            # Calcular cuándo enviar (actual + 1 minuto para procesr)
            ahora = datetime.now()
            enviar_en = ahora + timedelta(minutes=1)

            print(f"📅 Agendando cita para {fecha_cita} a las {hora_cita}")
            print(f"📱 Enviando confirmación a {numero_destino}")
            print(f"⏰ El mensaje se enviará a las {enviar_en.strftime('%H:%M:%S')}")

            # Enviar mensaje
            kit.sendwhatmsg(
                phone_no=numero_destino,
                message=mensaje,
                time_hour=enviar_en.hour,
                time_min=enviar_en.minute,
                wait_time=15,  # Segundos para cargar WhatsApp Web
                tab_close=True  # Cerrar pestaña automáticamente
            )

            print("✅ ¡Cita agendada y confirmación enviada exitosamente!")
            return True

        except Exception as e:
            print(f"❌ Error al agendar cita: {e}")
            return False

    def generar_fecha_hora_cita(self):
        # Día siguiente
        ahora = datetime.now()
        fecha_cita = ahora + timedelta(days=1)

        # Si cae en fin de semana, mover al lunes
        while fecha_cita.weekday() >= 5:  # 5=sábado, 6=domingo
            fecha_cita += timedelta(days=1)

        fecha_str = fecha_cita.strftime("%d/%m/%Y")
        hora_str = "10:00 AM"

        return fecha_str, hora_str

    def crear_mensaje_cita(self, fecha, hora):
        # Mensaje de confirmacion
        mensaje = f"""
🏥 *{self.nombre_clinica}*

✅ *CITA CONFIRMADA*

👨‍⚕️ *Doctor:* {self.nombre_doctor}
📅 *Fecha:* {fecha}
🕐 *Hora:* {hora}
📍 *Dirección:* {self.direccion}

📋 *Recomendaciones:*
• Llegar 15 minutos antes
• Traer identificación oficial
• Traer estudios médicos previos (si los tiene)
• Usar cubrebocas

📞 *Contacto:* {self.telefono_clinica}

_Mensaje generado automáticamente por el Sistema de Diagnóstico Médico_
        """.strip()

        return mensaje

    def validar_numero(self, numero):
        # Válida que el número de teléfono tenga el formato correcto
        numero_limpio = ''.join(filter(str.isdigit, numero))

        # Validar longitud para México (10 dígitos + código país)
        if len(numero_limpio) == 10:
            # Agregar código de país de México
            return f"+52{numero_limpio}"
        elif len(numero_limpio) == 12 and numero_limpio.startswith("52"):
            # Ya tiene código de país
            return f"+{numero_limpio}"
        elif len(numero_limpio) == 13 and numero_limpio.startswith("521"):
            # Formato con 521 (móvil México)
            return f"+{numero_limpio}"
        else:
            return None

    def solicitar_numero_telefono(self, voz_manager):
        voz_manager.hablar("Para agendar su cita, necesito su número de teléfono.")
        voz_manager.hablar("Puede dictarme su número por voz o escribirlo.")

        for intento in range(3):
            try:
                # Dar opción de voz o texto
                voz_manager.hablar("¿Prefiere dictar su número por voz?")
                usar_voz = voz_manager.escuchar_si_no("¿Quiere decir su número por voz?")

                numero = None

                if usar_voz:
                    voz_manager.hablar("Perfecto. Diga su número de teléfono celular de 10 dígitos.")
                    voz_manager.hablar(
                        "Puede decir los números uno por uno, por ejemplo: cuatro seis uno, dos tres cuatro, cinco seis siete ocho.")

                    numero = voz_manager.escuchar_numero_telefono()

                    if numero:
                        voz_manager.repetir_numero_reconocido(numero)
                    else:
                        voz_manager.hablar("No pude reconocer su número. Intentemos por escrito.")
                        numero = None


                if not numero:
                    voz_manager.hablar("Por favor escriba su número de teléfono de 10 dígitos.")
                    print("📱 Ingrese su número de teléfono (ej: 4611234567):")
                    numero = input("Número: ").strip()

                # Validar el número obtenido
                numero_valido = self.validar_numero(numero)
                if numero_valido:
                    voz_manager.hablar(f"Su número es {self.formatear_numero_para_voz(numero_valido)}. ¿Es correcto?")

                    confirmacion = voz_manager.escuchar_si_no("¿El número es correcto?")
                    if confirmacion:
                        return numero_valido
                    else:
                        voz_manager.hablar("Entendido. Vamos a intentar de nuevo.")
                else:
                    voz_manager.hablar("El número no parece válido. Debe tener 10 dígitos. Intente de nuevo.")
                    print("❌ Formato incorrecto. Use 10 dígitos sin espacios ni guiones.")

            except Exception as e:
                print(f"❌ Error: {e}")
                voz_manager.hablar("Hubo un error. Intente de nuevo.")

        voz_manager.hablar("No pude obtener un número válido después de varios intentos. Regresando al menú principal.")
        return None

    def formatear_numero_para_voz(self, numero_completo):
        # Extraer solo los dígitos del número (sin +52)
        solo_numero = numero_completo.replace("+52", "")

        if len(solo_numero) == 10:
            # Formato: 000 000 00 00
            grupos = [
                solo_numero[:3],
                solo_numero[3:6],
                solo_numero[6:8],
                solo_numero[8:10]
            ]
            return " ".join(grupos)
        else:
            # Si no tiene 10 dígitos, separar cada dígito
            return " ".join(solo_numero)

    def mostrar_info_cita(self):
        print("\n" + "=" * 50)
        print("📋 INFORMACIÓN SOBRE CITAS MÉDICAS")
        print("=" * 50)
        print(f"🏥 Clínica: {self.nombre_clinica}")
        print(f"👨‍⚕️ Doctor: {self.nombre_doctor}")
        print(f"📍 Dirección: {self.direccion}")
        print(f"📞 Teléfono: {self.telefono_clinica}")
        print("\n💡 Nota: Este es un sistema de demostración.")
        print("   Las citas son simuladas para fines educativos.")
        print("=" * 50)