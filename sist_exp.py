import os
import sys
import speech_recognition as sr
import pyttsx3
from experta import Fact, KnowledgeEngine, Rule, Field, AS
# Asegura que se cargue la versión local de experta
ruta_local = os.path.abspath("libs/experta")
if ruta_local not in sys.path:
    sys.path.insert(0, ruta_local)



# Motor de voz
voz = pyttsx3.init()


def preguntar_por_voz(pregunta):
    hablar(pregunta)  # Lee la pregunta en voz alta

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Esperando respuesta (di 'sí' o 'no')...")
        audio = r.listen(source)

    try:
        respuesta = r.recognize_google(audio, language="es-ES")
        print(f"🔈 Tú dijiste: {respuesta}")

        if "sí" in respuesta.lower():
            return True
        elif "no" in respuesta.lower():
            return False
        else:
            print("❗ Respuesta no clara. Intenta responder solo 'sí' o 'no'.")
            return preguntar_por_voz(pregunta)
    except sr.UnknownValueError:
        print("❗ No se entendió. Vamos a intentarlo otra vez.")
        return preguntar_por_voz(pregunta)
    except sr.RequestError as e:
        print(f"❗ Error del servicio de reconocimiento de voz: {e}")
        return False

def hablar(texto):
    print(texto)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    for voz in engine.getProperty('voices'):
        if "spanish" in voz.name.lower():
            engine.setProperty('voice', voz.id)
            break

    engine.say(texto)
    engine.runAndWait()



class Sintomas(Fact):
    """Clase que representa los síntomas reportados por el paciente"""
    pass

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_realizado = False
        self.evaluacion_final = False

    @Rule(Sintomas(fiebre=True, tos=True, dolor_garganta=True, congestion_nasal=True), salience=5)
    def diagnostico_gripe(self):
        hablar("Diagnóstico: Posible GRIPE. Se recomienda reposo e hidratación.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, tos=True, dificultad_respirar=True, perdida_olfato=True), salience=10)
    def diagnostico_covid(self):
        hablar("Diagnóstico: Posible COVID-19. Consulte a un médico y hágase una prueba.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, dolor_cabeza=True, dolor_muscular=True, sarpullido=False), salience=8)
    def diagnostico_dengue(self):
        hablar("Diagnóstico: Posible DENGUE. Consulte a un médico de inmediato.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, tos=True, dolor_pecho=True, dificultad_respirar=True), salience=9)
    def diagnostico_neumonia(self):
        hablar("Diagnóstico: Posible NEUMONÍA. Se recomienda una evaluación médica urgente.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(dolor_cabeza=True, sensibilidad_luz=True, nauseas=True), salience=6)
    def diagnostico_migraña(self):
        hablar("Diagnóstico: Posible MIGRAÑA. Evite la luz fuerte y descanse.")
        self.diagnostico_realizado = True

    @Rule(AS.fact << Sintomas(), salience=1)
    def diagnostico_desconocido(self, fact):
        if not self.diagnostico_realizado and self.evaluacion_final:
            hablar("No se encontró un diagnóstico claro. Consulte con un médico.")
            print(f"📌 Hechos insertados: {fact}")

def ejecutar_diagnostico():
    motor = DiagnosticoMedico()
    sintomas_usuario = {}

    lista_sintomas = [
        ("fiebre", "¿Tienes fiebre?"),
        ("tos", "¿Tienes tos?"),
        ("dolor_garganta", "¿Te duele la garganta?"),
        ("congestion_nasal", "¿Tienes congestión nasal?"),
        ("dificultad_respirar", "¿Tienes dificultad para respirar?"),
        ("perdida_olfato", "¿Has perdido el olfato?"),
        ("dolor_cabeza", "¿Tienes dolor de cabeza?"),
        ("dolor_muscular", "¿Te duelen los músculos?"),
        ("sarpullido", "¿Tienes sarpullido?"),
        ("dolor_pecho", "¿Sientes dolor en el pecho?"),
        ("sensibilidad_luz", "¿Te molesta la luz?"),
        ("nauseas", "¿Tienes náuseas?")
    ]

    for clave, pregunta in lista_sintomas:
        sintomas_usuario[clave] = preguntar_por_voz(pregunta)

        motor.reset()
        motor.evaluacion_final = False
        motor.declare(Sintomas(**sintomas_usuario))
        motor.run()

        if motor.diagnostico_realizado:
            return  # Salir si ya se hizo un diagnóstico

    # Evaluación final si no se encontró diagnóstico
    motor.reset()
    motor.evaluacion_final = True
    motor.declare(Sintomas(**sintomas_usuario))
    motor.run()

if __name__ == "__main__":
    ejecutar_diagnostico()
