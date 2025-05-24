import speech_recognition as sr
import pyttsx3
import time


class VozManager:
    def __init__(self):
        # Configurar motor de síntesis de voz
        self.engine = pyttsx3.init()
        self.configurar_voz()

        # Configurar reconocedor de voz
        self.recognizer = sr.Recognizer()
        self.configurar_reconocedor()

    def configurar_voz(self):
        # Configura el motor de síntesis de voz
        # Configurar velocidad
        self.engine.setProperty('rate', 200)

        # Configurar volumen (0.0 a 1.0)
        self.engine.setProperty('volume', 1)

        # Intentar configurar voz en español
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def configurar_reconocedor(self):
        # Configura el reconocedor de voz para mejor precisión
        # Ajustar sensibilidad al ruido ambiente
        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.2
        self.recognizer.non_speaking_duration = 0.3

    def calibrar_microfono(self, duracion=2):
        """Calibración mejorada del micrófono"""
        print("🎤 Calibrando micrófono...")
        print("   Mantente en silencio por unos segundos...")

        try:
            with sr.Microphone() as source:
                # Calibración más larga para mejor ajuste
                self.recognizer.adjust_for_ambient_noise(source, duration=duracion)

                # Mostrar el nivel de ruido detectado
                print(f"   Nivel de ruido ambiente: {self.recognizer.energy_threshold:.0f}")

                # Reducir aún más el umbral después de la calibración
                self.recognizer.energy_threshold = max(100, self.recognizer.energy_threshold * 0.7)
                print(f"   Umbral ajustado a: {self.recognizer.energy_threshold:.0f}")

        except Exception as e:
            print(f"❗ Error en calibración: {e}")
            # Usar valores seguros si falla la calibración
            self.recognizer.energy_threshold = 150

    def hablar(self, texto):
        #Convierte texto a voz
        print(f"🔊 Sistema: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()

    def escuchar_opcion_menu(self, max_intentos=3):
        self.calibrar_microfono(duracion=2)

        for intento in range(max_intentos):
            try:
                with sr.Microphone() as source:
                    if intento == 0:
                        print("🎤 Calibrando micrófono...")
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)

                    print(f"🎤 Esperando tu respuesta... (Intento {intento + 1}/{max_intentos})")
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=5)

                # Reconocer audio
                respuesta = self.recognizer.recognize_google(
                    audio,
                    language="es-ES"
                ).lower().strip()

                print(f"🔈 Escuché: '{respuesta}'")

                # Procesar respuesta para opciones del menú
                resultado = self.procesar_opcion_menu(respuesta)
                if resultado is not None:
                    return resultado

            except sr.WaitTimeoutError:
                print("⏰ Tiempo agotado. Intenta de nuevo.")
                if intento < max_intentos - 1:
                    self.hablar("No escuché nada. Inténtalo de nuevo.")

            except sr.UnknownValueError:
                print("❗ No se entendió. Intenta hablar más claro.")
                if intento < max_intentos - 1:
                    self.hablar("No te entendí. Por favor repite tu opción.")

            except sr.RequestError as e:
                print(f"❗ Error del servicio: {e}")
                return None

            except Exception as e:
                print(f"❗ Error inesperado: {e}")
                return None

        self.hablar("No pude entender tu respuesta después de varios intentos.")
        return None

    def procesar_opcion_menu(self, respuesta):
        respuesta = respuesta.replace(" ", "").lower()

        # Opciones para "1" o "uno"
        opciones_uno = [
            "uno", "1", "primera", "opción1", "opcion1",
            "unouno", "primero", "cita", "agendar"
        ]

        # Opciones para "2" o "dos"
        opciones_dos = [
            "dos", "2", "segunda", "opción2", "opcion2",
            "dosdos", "segundo", "diagnóstico", "diagnostico",
            "sistema", "preguntas"
        ]

        # Verificar coincidencias
        for opcion in opciones_uno:
            if opcion in respuesta:
                return 1

        for opcion in opciones_dos:
            if opcion in respuesta:
                return 2

        return None

    def escuchar_si_no(self, pregunta, max_intentos=5):
        self.hablar(pregunta)

        for intento in range(max_intentos):
            try:
                with sr.Microphone() as source:
                    if intento == 0:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.8)

                    print(f"🎤 Esperando respuesta (sí/no)... (Intento {intento + 1}/{max_intentos})")
                    audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=5)

                respuesta = self.recognizer.recognize_google(
                    audio,
                    language="es-ES"
                ).lower().strip()

                print(f"🔈 Escuché: '{respuesta}'")

                # Procesar respuesta sí/no
                resultado = self.procesar_si_no(respuesta)
                if resultado is not None:
                    return resultado
                else:
                    self.hablar("Por favor responde solo sí o no.")

            except sr.WaitTimeoutError:
                print("⏰ Tiempo agotado.")
                if intento < max_intentos - 1:
                    self.hablar("No escuché respuesta. ¿Sí o no?")

            except sr.UnknownValueError:
                print("❗ No se entendió.")
                if intento < max_intentos - 1:
                    self.hablar("No te entendí. Responde sí o no.")

            except Exception as e:
                print(f"❗ Error: {e}")
                return None

        self.hablar("No pude entender tu respuesta. Asumiré que es no.")
        return False

    def procesar_si_no(self, respuesta):
        #Procesa respuestas de sí/no
        respuesta = respuesta.replace(" ", "").lower()

        # Respuestas afirmativas
        afirmativas = [
            "sí", "si", "sii", "síí", "yes", "yep",
            "claro", "correcto", "exacto", "afirmativo"
        ]

        # Respuestas negativas
        negativas = [
            "no", "nop", "nope", "negativo", "para nada",
            "nunca", "jamás", "jamas"
        ]

        for afirmativa in afirmativas:
            if afirmativa in respuesta:
                return True

        for negativa in negativas:
            if negativa in respuesta:
                return False

        return None  # No se pudo determinar

    def despedirse(self):
        #Mensaje de despedida
        self.hablar("Hasta luego. Que tengas un buen día.")
        time.sleep(1)

    def escuchar_numero_telefono(self, max_intentos=5):

        for intento in range(max_intentos):
            try:
                with sr.Microphone() as source:
                    if intento == 0:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)

                    print(f"🎤 Diga su número de teléfono... (Intento {intento + 1}/{max_intentos})")
                    print("   💡 Diga los dígitos claramente, puede usar pausas")
                    print("   📱 Ejemplo: 'cuatro seis uno dos tres cuatro cinco seis siete ocho'")

                    # Tiempo más largo para números
                    audio = self.recognizer.listen(
                        source,
                        timeout=10,  # Más tiempo para empezar
                        phrase_time_limit=15  # Tiempo suficiente para 10 dígitos
                    )

                # Reconocer audio
                respuesta = self.recognizer.recognize_google(
                    audio,
                    language="es-ES"
                ).lower().strip()

                print(f"🔈 Escuché: '{respuesta}'")

                # Procesar y extraer número
                numero = self.extraer_numero_de_texto(respuesta)
                if numero:
                    return numero
                else:
                    self.hablar("No pude extraer un número válido. Intente de nuevo diciendo los dígitos claramente.")

            except sr.WaitTimeoutError:
                print("⏰ Tiempo agotado.")
                if intento < max_intentos - 1:
                    self.hablar("No escuché nada. Diga su número de teléfono con calma.")

            except sr.UnknownValueError:
                print("❗ No se entendió.")
                if intento < max_intentos - 1:
                    self.hablar("No te entendí. Diga los números más despacio y claro.")

            except Exception as e:
                print(f"❗ Error: {e}")
                return None

        self.hablar("No pude obtener su número de teléfono por voz.")
        return None

    def extraer_numero_de_texto(self, texto):
        # Diccionario para convertir palabras a números
        numeros_dict = {
            'cero': '0', 'uno': '1', 'dos': '2', 'tres': '3', 'cuatro': '4',
            'cinco': '5', 'seis': '6', 'siete': '7', 'ocho': '8', 'nueve': '9',
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }

        # Limpiar el texto
        texto = texto.lower().replace(',', ' ').replace('.', ' ').replace('-', ' ')
        palabras = texto.split()

        numero_extraido = ""

        for palabra in palabras:
            # Si ya es un dígito
            if palabra.isdigit():
                numero_extraido += palabra
            # Si es una palabra que representa un número
            elif palabra in numeros_dict:
                numero_extraido += numeros_dict[palabra]
            # Intentar extraer dígitos de palabras mixtas
            else:
                for char in palabra:
                    if char.isdigit():
                        numero_extraido += char

        # Validar longitud (debe ser 10 dígitos para México)
        if len(numero_extraido) == 10 and numero_extraido.isdigit():
            return numero_extraido
        elif len(numero_extraido) > 10:
            # si tiene más de 10, tomar los últimos 10
            return numero_extraido[-10:]
        else:
            return None

    def repetir_numero_reconocido(self, numero):
        if numero:
            # Separar cada dígito para pronunciarlo claramente
            digitos_separados = " ".join(numero)
            self.hablar(f"El número que escuché es: {digitos_separados}")

            # También decirlo como un número completo
            #self.hablar(f"Es decir: {numero}")
        else:
            self.hablar("No pude reconocer un número válido.")