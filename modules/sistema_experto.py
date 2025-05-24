# import os
# import sys
# import speech_recognition as sr
# import pyttsx3
# from experta import Fact, KnowledgeEngine, Rule, Field, AS
# # Asegura que se cargue la versión local de experta
# ruta_local = os.path.abspath("libs/experta")
# if ruta_local not in sys.path:
#     sys.path.insert(0, ruta_local)
#
#
#
# # Motor de voz
# voz = pyttsx3.init()
#
#
# def preguntar_por_voz(pregunta):
#     hablar(pregunta)  # Lee la pregunta en voz alta
#
#     r = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         print("🎤 Esperando respuesta (di 'sí' o 'no')...")
#         audio = r.listen(source)
#
#     try:
#         respuesta = r.recognize_google(audio, language="es-ES")
#         print(f"🔈 Tú dijiste: {respuesta}")
#
#         if "sí" in respuesta.lower():
#             return True
#         elif "no" in respuesta.lower():
#             return False
#         else:
#             print("❗ Respuesta no clara. Intenta responder solo 'sí' o 'no'.")
#             return preguntar_por_voz(pregunta)
#     except sr.UnknownValueError:
#         print("❗ No se entendió. Vamos a intentarlo otra vez.")
#         return preguntar_por_voz(pregunta)
#     except sr.RequestError as e:
#         print(f"❗ Error del servicio de reconocimiento de voz: {e}")
#         return False
#
# def hablar(texto):
#     print(texto)
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)
#
#     for voz in engine.getProperty('voices'):
#         if "spanish" in voz.name.lower():
#             engine.setProperty('voice', voz.id)
#             break
#
#     engine.say(texto)
#     engine.runAndWait()


from experta import *
from collections import Counter



class Sintomas(Fact): pass

traducciones = {
    "anemia" : {
        "fatiga extrema", "palidez notable", "dificultad para respirar"
    }
}

diagnosticos_base = {
    "amibiasis aguda avanzada" : {
        "necesidad de defecar sin conseguirlo", "diarrea"
    },
    "amibiasis aguda inicial" : {
        "dolor de cabeza", "perdida de apetito", "nauseas", "vomitos"
    },
    "amibiasis cronica" : {
        "episodios de estrenimiento", "episodios de diarrea explosiva",
        "episodios de dolor en la parte superior del abdomen"
    },
    "absceso hepatico amibiano" : {
        "fiebre alta", "dolor en la parte superior derecha del abdomen", "malestar general"
    },
    "absceso amibiano pulmonar" : {
        "dificultad para respirar", "dolor en el pecho", "tos" , "dolor en el pecho que empeora al respirar o toser"
    },
    "ascariasis pulmonar" : {
        "dificultad para respirar", "dolor en el pecho", "tos"
    },
    "ascariasis intestinal" : {
        "malestar abdominal cronico"
    },
    "ascariasis pancreatica" : {
        "dolor intenso en la parte superior del abdomen", "nauseas", "vomitos"
    },
    "giardiasis" : {
        "dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente"
    }
}

#por periodos = episodios de
#no se si cambiar anemia por sintomas mas carcateristicos de la anemia ustedes dicen
#cronica/cronico
#alta baja
#revisar noomenclatura
#en la parte superior del
"""
ESTAS SERIAN NUESTRAS REGLAS
    en un mismo renglon o set se considera condicion y
    en diferentes es como un o, por eso son reglas distintas
"""
diagnosticos_definidos = {
    #Generales (alergia, algo aparte de micro)

    #Virus

    #Bacterias

    #Parasitos
    "amibiasis aguda avanzada": [ #tal vez cambie este por lo del dolor
        diagnosticos_base["amibiasis aguda avanzada"] | {"dolor en la parte superior derecha del abdomen"},
        diagnosticos_base["amibiasis aguda avanzada"] | {"heces con sangre o moco"}
    ],

    "amibiasis aguda inicial": [
        diagnosticos_base["amibiasis aguda inicial"] | {"fiebre"},
        diagnosticos_base["amibiasis aguda inicial"]
    ],

    "amibiasis cronica": [
        diagnosticos_base["amibiasis cronica"] | traducciones["anemia"],
        diagnosticos_base["amibiasis cronica"] | {"dolor de cabeza"},
        diagnosticos_base["amibiasis cronica"] | {"mal sabor de boca"},
        diagnosticos_base["amibiasis cronica"] | {"dolor despues de comer"},
        diagnosticos_base["amibiasis cronica"]
    ],

    "absceso hepatico amibiano": [
        diagnosticos_base["absceso hepatico amibiano"] | {"sudoraciones vespertinas"},
        diagnosticos_base["absceso hepatico amibiano"] | {"dolor de cabeza"},
        diagnosticos_base["absceso hepatico amibiano"] | {"dolor en el hombro izquierdo"},
        diagnosticos_base["absceso hepatico amibiano"] | traducciones["anemia"],
        diagnosticos_base["absceso hepatico amibiano"] | {"perdida de peso"},
        diagnosticos_base["absceso hepatico amibiano"] | {"coloramiento amarillo"},
        diagnosticos_base["absceso hepatico amibiano"] | {"alcoholismo"},
        diagnosticos_base["absceso hepatico amibiano"] | {"desnutricion"},
        diagnosticos_base["absceso hepatico amibiano"] | {"inmunodeficiencia"},
        diagnosticos_base["absceso hepatico amibiano"]
    ],

    "absceso amibiano pulmonar": [
        diagnosticos_base["absceso amibiano pulmonar"] | {"tos seca"},
        diagnosticos_base["absceso amibiano pulmonar"] | {"tos con flema"},
        diagnosticos_base["absceso amibiano pulmonar"] | {"tos con flema achocolatada y sabor a higado"},
        diagnosticos_base["absceso amibiano pulmonar"] | {"fiebre"},
        diagnosticos_base["absceso amibiano pulmonar"] | {"malestar general"},
        diagnosticos_base["absceso amibiano pulmonar"] | {"sudoraciones nocturnas"}
    ],

    "ascariasis pulmonar" : [
        diagnosticos_base["ascariasis pulmonar"] | {"tos con sangre", "fiebre", "ruidos al respirar"},
        diagnosticos_base["ascariasis pulmonar"] | {"tos con sangre", "fiebre"},
    ],

    "ascariasis intestinal" : [
        diagnosticos_base["ascariasis intestinal"] | {"dolor abdominal", "falta de apetito", "nauseas", "diarrea"},
        diagnosticos_base["ascariasis intestinal"] | {"intolerancia a la lactosa que no existia antes"},
        diagnosticos_base["ascariasis intestinal"] | {"desnutricion"},
        diagnosticos_base["ascariasis intestinal"] | {"dolor abdominal", "vomitos", "estrenimiento"}, #si obstruyen
        diagnosticos_base["ascariasis intestinal"] | {"dolor abdominal", "vomitos con parasitos", "estrenimiento"}, #si obstruyen
    ],

    "ascariasis pancreatica" : [
         diagnosticos_base["ascariasis pancreatica"] | {"coloramiento amarillo"},
         diagnosticos_base["ascariasis pancreatica"] | {"sensibilidad al tacto en el abdomen"},
         diagnosticos_base["ascariasis pancreatica"] | {"dolor abdominal que irradia a la espalda"},
         diagnosticos_base["ascariasis pancreatica"] | {"dolor abdominal que irradia al hombro derecho"},
         diagnosticos_base["ascariasis pancreatica"] | {"hinchazon de pies o tobillos"},
         diagnosticos_base["ascariasis pancreatica"] | {"heces color arcilla"},
    ],

    "giardiasis" : [
        diagnosticos_base["giardiasis"] | {"malestar general"},
        diagnosticos_base["giardiasis"] | {"nauseas"},
        diagnosticos_base["giardiasis"] | {"heces con alimentos sin digerir"},
        diagnosticos_base["giardiasis"] | {"heces con mucha grasa, dificiles de limpiar"},
        diagnosticos_base["giardiasis"] | {"dolor en articulaciones"},
        diagnosticos_base["giardiasis"] | {"sarpullido"},
        diagnosticos_base["giardiasis"]
    ]
}

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.sintomas_usuario = {}
        self.diagnosticos_posibles = set(diagnosticos_definidos.keys())
        self.diagnostico_realizado = False
        self.sintomas = set()

    def set_sintomas(self):
        todos = set()
        for variantes in diagnosticos_definidos.values():
            for sintoma in variantes:
                todos.update(sintoma)
        self.sintomas = todos

    def siguiente_sintoma_a_preguntar(self):
        sintomas_base_faltantes = set()
        sintomas_variante_faltantes = []

        sintoma_ocurrencias = Counter()

        for diag in self.diagnosticos_posibles:
            base = diagnosticos_base.get(diag, set())
            for sintoma in base:
                if sintoma not in self.sintomas_usuario:
                    sintomas_base_faltantes.add(sintoma)
                    sintoma_ocurrencias[sintoma] += 1

            for variante in diagnosticos_definidos.get(diag, []):
                for sintoma in variante:
                    if sintoma not in self.sintomas_usuario:
                        sintomas_variante_faltantes.append(sintoma)
                        sintoma_ocurrencias[sintoma] += 1

        if sintomas_base_faltantes:
            # Ordenar por rareza (menos diagnósticos lo tienen → más discriminante)
            ordenados = sorted(sintomas_base_faltantes, key=lambda s: sintoma_ocurrencias[s])
            return ordenados
        else:
            ordenados = sorted(set(sintomas_variante_faltantes), key=lambda s: sintoma_ocurrencias[s])
            return ordenados

    def preguntar_sintoma(self, sintoma):
        respuesta = input(f"¿Tienes {sintoma.replace('_', ' ')}? (s/n): ").lower()
        self.sintomas_usuario[sintoma] = respuesta == "s"

    def diagnosticos_por_sintomas(sintomas_afirmados: set):
        posibles = set()

        for diag, variantes in diagnosticos_definidos.items():
            for variante in variantes:
                if variante.issubset(sintomas_afirmados):
                    posibles.add(diag)
                    break

        return posibles

    def filtrar_diagnostico_tollens(self):
        nuevos_posibles = set()

        for diag, variantes_sintomas in diagnosticos_definidos.items():
            base = diagnosticos_base[diag]
            if any(s in self.sintomas_usuario and self.sintomas_usuario[s] is False for s in base):
                continue

            sintomas_negados = {s for s, v in self.sintomas_usuario.items() if v is False}

            variante_valida = False
            for variante in variantes_sintomas:
                if variante.isdisjoint(sintomas_negados):
                    variante_valida = True
                    break

            if not variante_valida:
                continue

            nuevos_posibles.add(diag)

        print(nuevos_posibles)
        self.diagnosticos_posibles = nuevos_posibles

    def filtrar_diagnosticos_ponens(self, immediate = False):
        nuevos_posibles = set()

        if not immediate:
            sintomas_reportados = self.sintomas_usuario
        else:
            sintomas_reportados = immediate

        for diag, variantes_sintomas in diagnosticos_definidos.items():
            base = diagnosticos_base[diag]
            if any(s in self.sintomas_usuario and self.sintomas_usuario[s] is False for s in base):
                continue

            sintomas_extra_afirmados = {s for s, v in self.sintomas_usuario.items() if v is True and s not in base}

            # 3. Verificar variantes válidas
            og_sintomas_extra_afirmados = sintomas_extra_afirmados
            for variante in variantes_sintomas:
                variante_valida = {s for s in variante if s not in base}
                if variante_valida.issubset(og_sintomas_extra_afirmados):
                    sintomas_extra_afirmados -= variante

            if len(sintomas_extra_afirmados) > 0:
                continue

            nuevos_posibles.add(diag)

        print(nuevos_posibles)
        self.diagnosticos_posibles = nuevos_posibles

    @Rule(AS.fact << Sintomas())
    def evaluar_diagnostico(self, fact):
        #self.filtrar_diagnostico_ponens() #para hard filtering
        self.filtrar_diagnostico_tollens() #como trabaja porlog

        if len(self.diagnosticos_posibles) == 0:
            print("No se encontró un diagnóstico claro.")
            self.diagnostico_realizado = True
        elif not self.siguiente_sintoma_a_preguntar():
            valid = False
            aux = {i for i in self.diagnosticos_posibles}
            for diag in aux:
                sintomas_extra = {s for s, v in self.sintomas_usuario.items() if v is True and s not in diagnosticos_base[diag]}
                if len(sintomas_extra) == 0:
                    for variante in diagnosticos_definidos[diag]:
                        variante_valida = {s for s in variante if s not in diagnosticos_base[diag]}
                        if len(variante_valida) == 0:
                            valid = True
                            break
                if len(sintomas_extra) == 0 and not valid:
                    self.diagnosticos_posibles.remove(diag)

            if len(self.diagnosticos_posibles) == 0:
                print("No se encontró un diagnóstico claro.")
            elif len(self.diagnosticos_posibles) == 1:
                diag = list(self.diagnosticos_posibles)[0]
                print(f"Diagnóstico probable: {diag.upper()}")
            else:
                print(f"Posibles diagnósticos: {', '.join(self.diagnosticos_posibles)}")
            self.diagnostico_realizado = True

def ejecutar_diagnostico():
    motor = DiagnosticoMedico()
    motor.set_sintomas()
    print(motor.sintomas)
    while not motor.diagnostico_realizado:
        sintomas_a_preguntar = motor.siguiente_sintoma_a_preguntar()

        if not sintomas_a_preguntar:
            break

        siguiente = sintomas_a_preguntar[0]
        motor.preguntar_sintoma(siguiente)

        motor.reset()
        motor.declare(Sintomas(**motor.sintomas_usuario))
        motor.run()


if __name__ == "__main__":
    ejecutar_diagnostico()