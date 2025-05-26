from experta import *
from collections import Counter

class Sintomas(Fact): pass

diagnosticos_base = {
    "amebiasis aguda avanzada" : {
        "dolor abdominal", "diarrea", "heces anormales"
    },
    "amebiasis aguda inicial" : {
        "dolor de cabeza", "pérdida de apetito", "nauseas", "vómitos"
    },
    "amebiasis crónica" : {
        "estreñimiento", "diarrea", "dolor abdominal"
    },
    "absceso hepático amebiano" : {
        "fiebre", "dolor abdominal", "malestar general"
    },
    "absceso amebiano pulmonar" : {
        "dificultad para respirar", "dolor en el pecho", "tos"
    },
    "ascariasis pulmonar" : {
        "dificultad para respirar", "dolor en el pecho", "tos", "fiebre"
    },
    "ascariasis intestinal" : {
        "dolor abdominal", "vómitos", "nauseas"
    },
    "ascariasis pancreática" : {
        "dolor abdominal", "nauseas", "vómitos"
    },
    "giardiasis" : {
        "dolor abdominal", "diarrea", "heces anormales"
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
    "amebiasis aguda avanzada": [
        diagnosticos_base["amebiasis aguda avanzada"] | {"dolor en la parte superior derecha del abdomen"},
        diagnosticos_base["amebiasis aguda avanzada"] | {"heces con sangre o moco"},
	    diagnosticos_base["amebiasis aguda avanzada"] | {"necesidad de defecar sin conseguirlo"},
    ],

    "amebiasis aguda inicial": [
        diagnosticos_base["amebiasis aguda inicial"] | {"fiebre"},
        diagnosticos_base["amebiasis aguda inicial"]
    ],

    "amebiasis crónica": [
        diagnosticos_base["amebiasis crónica"] | {"diarrea explosiva", "dolor en la parte superior del abdomen", "fatiga extrema", "palidez notable"},
        diagnosticos_base["amebiasis crónica"] | {"diarrea explosiva", "dolor en la parte superior del abdomen", "dolor de cabeza"},
        diagnosticos_base["amebiasis crónica"] | {"diarrea explosiva", "dolor en la parte superior del abdomen", "mal sabor de boca"},
        diagnosticos_base["amebiasis crónica"] | {"diarrea explosiva", "dolor en la parte superior del abdomen", "dolor abdominal después de comer"},
        diagnosticos_base["amebiasis crónica"] | {"diarrea explosiva", "dolor en la parte superior del abdomen"}
    ],

    "absceso hepático amebiano": [
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "sudoraciones vespertinas"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "dolor de cabeza"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "dolor en el hombro izquierdo"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "fatiga extrema", "palidez notable"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "pérdida de peso"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "coloramiento amarillo"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "alcoholismo"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "desnutrición"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen", "inmunodeficiencia"},
        diagnosticos_base["absceso hepático amebiano"] | {"fiebre alta", "dolor en la parte superior derecha del abdomen"}
    ],

    "absceso amebiano pulmonar": [
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "tos seca"},
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "tos con flema"},
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "tos achocolatada y sabor a hígado"},
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "fiebre"},
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "malestar general"},
        diagnosticos_base["absceso amebiano pulmonar"] | {"dolor en el pecho que empeora al respirar o toser", "sudoraciones nocturnas"}
    ],

    "ascariasis pulmonar" : [
        diagnosticos_base["ascariasis pulmonar"] | {"tos con sangre", "ruidos al respirar"},
        diagnosticos_base["ascariasis pulmonar"] | {"tos con sangre"},
    ],

    "ascariasis intestinal" : [
        diagnosticos_base["ascariasis intestinal"] | {"dolor abdominal crónico", "falta de apetito", "diarrea"},
        diagnosticos_base["ascariasis intestinal"] | {"intolerancia a la lactosa que no existía antes"},
        diagnosticos_base["ascariasis intestinal"] | {"desnutrición"},
        diagnosticos_base["ascariasis intestinal"] | {"dolor abdominal crónico", "vómitos con parásitos", "estreñimiento"}, #si obstruyen
    ],

    "ascariasis pancreática" : [
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "coloramiento amarillo"},
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "sensibilidad al tacto en el abdomen"},
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "dolor abdominal que irradia a la espalda"},
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "dolor abdominal que irradia al hombro derecho"},
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "hinchazón de pies o tobillos"},
         diagnosticos_base["ascariasis pancreática"] | {"dolor intenso en la parte superior del abdomen", "heces color arcilla"},
    ],

    "giardiasis" : [
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "malestar general"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "nauseas"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "heces con alimentos sin digerir"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "heces con mucha grasa, difíciles de limpiar"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "dolor en articulaciones"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente", "sarpullido"},
        diagnosticos_base["giardiasis"] | {"dolor en la parte superior central del abdomen", "diarrea pastosa, con muchos gases y maloliente"}
    ]
}

class DiagnosticoMedico(KnowledgeEngine):
    def get_sintomas_base(self):
        sintomas = set()
        for conjunto in diagnosticos_base.values():
            sintomas.update(conjunto)
        return sintomas

    def sintomas_variante_faltantes_dado_base(self):
        sintomas_base_afirmados = {s for s, v in self.sintomas_usuario.items() if v}
        sintomas_preguntados = set(self.sintomas_usuario.keys())
        sintomas_faltantes = set()

        for diag in self.diagnosticos_posibles:
            variantes = diagnosticos_definidos.get(diag, [])
            base = diagnosticos_base.get(diag, set())

            if not base.issubset(sintomas_base_afirmados):
                continue  # solo seguimos si la base ya está afirmada

            for variante in variantes:
                print(variante)
                sintomas_variante = variante - base
                sintomas_no_preguntados = sintomas_variante - sintomas_preguntados
                sintomas_faltantes.update(sintomas_no_preguntados)
        return sintomas_faltantes

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

    def diagnosticos_por_sintomas(self):
        sintomas_afirmados = {s for s, v in self.sintomas_usuario.items() if v}

        resultados = set()
        for diagnostico, variantes in self.base_conocimiento.items():
            for variante in variantes:
                if variante.issubset(sintomas_afirmados):
                    resultados.add(diagnostico)
                    break  # Si una variante coincide, no necesitas revisar más

        return resultados

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

    @Rule(Sintomas())
    def evaluar_diagnostico(self):
        if not self.siguiente_sintoma_a_preguntar():
            sintomas_afirmados = {s for s, v in self.sintomas_usuario.items() if v}
            validos = set()

            for diag in self.diagnosticos_posibles:
                for variante in diagnosticos_definidos[diag]:
                    if variante.issubset(sintomas_afirmados):
                        validos.add(diag)
                        break

            if not validos:
                print("No se encontró un diagnóstico claro.")
            elif len(validos) == 1:
                print(f"Diagnóstico probable: {list(validos)[0].upper()}")
            else:
                print("Posibles diagnósticos:")
                for diag in validos:
                    print(f"- {diag}")

            self.diagnosticos_posibles = list(validos)
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