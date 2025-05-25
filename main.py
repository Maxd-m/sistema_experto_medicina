import sys
import os
from modules.voz_manager import VozManager
from modules.whatsapp_manager import WhatsAppManager
from firebase import DiagnosticoDB
from modules.sistema_experto import ejecutar_diagnostico


class MenuPrincipal:
    def __init__(self):
        self.voz = VozManager()
        self.whatsapp = WhatsAppManager()
        self.ejecutando = True
        self.db = DiagnosticoDB("key.json")
        self.diagnosticos_base = None
        self.diagnosticos_definidos = None
        self.posibles_diagnosticos = None

    def mostrar_bienvenida(self):
        """Es el mensaje de bienvenida"""
        print("\n" + "=" * 60)
        print("🏥 SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO")
        print("📞 Interfaz de Voz Simulada")
        print("=" * 60)

        mensaje_bienvenida = """
        Bienvenido al sistema de diagnóstico médico.
        Este sistema le ayudará con dos opciones principales.
        Por favor, escuche atentamente las opciones del menú.
        """

        self.voz.hablar(mensaje_bienvenida)

    def mostrar_menu(self):
        """Muestra las opciones del menú por voz"""
        mensaje_menu = """
        Menú principal. Tiene dos opciones:

        Opción uno: Agendar una cita médica.

        Opción dos: Iniciar diagnóstico médico con nuestro sistema experto.

        Por favor, diga "opcion uno" para agendar cita, o "opcion 
        " para diagnóstico.
        """

        self.voz.hablar(mensaje_menu)

        # Mostrar menú visual también
        print("\n📋 MENÚ PRINCIPAL:")
        print("1️⃣  Agendar cita médica")
        print("2️⃣  Sistema experto de diagnóstico")
        print("\n🎤 Diga su opción...")

    def procesar_opcion_1(self):
        """Maneja la opción de agendar la cita"""
        print("\n" + "-" * 40)
        print("📅 AGENDAR CITA MÉDICA")
        print("-" * 40)

        self.voz.hablar("Ha seleccionado agendar cita médica.")

        # Mostrar información de la clínica
        self.whatsapp.mostrar_info_cita()

        # Solicitar número de teléfono
        numero = self.whatsapp.solicitar_numero_telefono(self.voz)

        if numero:
            self.voz.hablar("Perfecto. Procederé a agendar su cita y enviar la confirmación por WhatsApp.")

            # Intentar agendar la cita
            if self.whatsapp.agendar_cita(numero):
                self.voz.hablar("""
                Su cita ha sido agendada exitosamente. 
                En breve recibirá la confirmación en su WhatsApp con todos los detalles.
                Gracias por elegir nuestros servicios.
                """)
                self.db.guardar('pacientes', numero)
            else:
                self.voz.hablar("""
                Lo siento, hubo un problema al agendar su cita. 
                Por favor intente más tarde o contacte directamente a la clínica.
                """)
        else:
            self.voz.hablar("No se pudo procesar su solicitud de cita. Regresando al menú principal.")

    def procesar_opcion_2(self):
        """Maneja la opción del sistema experto"""
        print("\n" + "-" * 40)
        print("🔬 SISTEMA EXPERTO DE DIAGNÓSTICO")
        print("-" * 40)

        self.voz.hablar("""
        Ha seleccionado el sistema experto de diagnóstico médico.
        Este sistema le hará una serie de preguntas sobre sus síntomas
        para ayudar a identificar posibles condiciones médicas.
        """)

        self.voz.hablar("""
        Recuerde que este sistema es solo una herramienta de apoyo
        y no reemplaza la consulta con un médico profesional.
        """)

        self.voz.hablar("Comenzando con las preguntas del diagnóstico.")

        try:
            # Ejecutar el sistema experto con integración de voz
            self.ejecutar_sistema_experto_con_voz()

        except Exception as e:
            print(f"❌ Error en el sistema experto: {e}")
            self.voz.hablar("Lo siento, hubo un error en el sistema de diagnóstico. Regresando al menú principal.")

    def ejecutar_sistema_experto_con_voz(self):
        # Importar aquí para evitar problemas de dependencias circulares
        from modules.sistema_experto import DiagnosticoMedico, Sintomas

        motor = DiagnosticoMedico(self.diagnosticos_base, self.diagnosticos_definidos)
        motor.set_sintomas()

        # Integrar VozManager con el sistema experto
        motor.voz_manager = self.voz

        print("🔬 Iniciando diagnóstico médico...")
        self.voz.hablar("Voy a hacerle algunas preguntas sobre sus síntomas. Responda con sí o no.")

        while not motor.diagnostico_realizado:
            sintomas_a_preguntar = motor.siguiente_sintoma_a_preguntar()

            if not sintomas_a_preguntar:
                break

            siguiente = sintomas_a_preguntar[0]

            # Usar el sistema de voz para preguntar
            pregunta = f"¿Tiene {siguiente.replace('_', ' ')}?"
            respuesta = self.voz.escuchar_si_no(pregunta)

            # Registrar respuesta
            motor.sintomas_usuario[siguiente] = respuesta

            # Procesar diagnóstico
            motor.reset()
            motor.declare(Sintomas(**motor.sintomas_usuario))
            motor.run()

        self.voz.hablar("Diagnóstico completado. Gracias por usar nuestro sistema.")

    def manejar_opcion_invalida(self):
        self.voz.hablar("""
        Lo siento, no entendí su opción. 
        Por favor diga "uno" para agendar cita, o "dos" para diagnóstico médico.
        """)

    def confirmar_salida(self):
        """Simular el reinicio"""
        self.voz.hablar("¿Desea realizar otra consulta?")
        respuesta = self.voz.escuchar_si_no("¿Quiere volver al menú principal?")
        return respuesta

    def ejecutar(self):
        try:
            # Initialization
            self.db.guardar('pacientes', '442223034')
            self.diagnosticos_base = self.db.leer_base()
            self.diagnosticos_definidos = self.db.leer_definidos()

            self.mostrar_bienvenida()

            while self.ejecutando:
                self.mostrar_menu()

                # Escuchar opción del usuario
                opcion = self.voz.escuchar_opcion_menu()

                if opcion == 1:
                    self.procesar_opcion_1()
                elif opcion == 2:
                    self.procesar_opcion_2()
                elif opcion is None:
                    self.manejar_opcion_invalida()
                    continue
                else:
                    self.manejar_opcion_invalida()
                    continue

                # Preguntar si quiere continuar
                if not self.confirmar_salida():
                    self.ejecutando = False

            # Despedida
            self.voz.despedirse()

        except KeyboardInterrupt:
            print("\n\n⚠️  Sistema interrumpido por el usuario")
            self.voz.hablar("Sistema interrumpido. Hasta luego.")

        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            self.voz.hablar("Lo siento, ocurrió un error crítico. El sistema se cerrará.")

        finally:
            print("\n👋 Gracias por usar el Sistema de Diagnóstico Médico")
            print("🏥 Clínica San Rafael - Sistema desarrollado para fines educativos")


def main():
    menu = MenuPrincipal()
    menu.ejecutar()


if __name__ == "__main__":
    main()