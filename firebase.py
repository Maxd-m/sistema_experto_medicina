import firebase_admin
from firebase_admin import credentials, db

class DiagnosticoDB:
    def __init__(self, path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://sistema-experto-plf-default-rtdb.firebaseio.com/'
            })

    def leer(self, rama: str):
        ref = db.reference(rama)
        data = ref.get()
        return data if data else False

    def leer_base(self):
        ref = db.reference('diagnosticos_base')
        data = ref.get()
        if not data:
            return False
        processed_data = {}
        for diagnosis_name, symptoms_list in data.items():
            processed_data[diagnosis_name] = set(symptoms_list)

        return processed_data

    def leer_definidos(self):
        ref = db.reference('diagnosticos_definidos')
        data = ref.get()
        if not data:
            return False
        processed_data = {}
        for diagnosis_name, symptom_variations_list in data.items():
            converted_variations = []
            for symptoms_inner_list in symptom_variations_list:
                converted_variations.append(set(symptoms_inner_list))
            processed_data[diagnosis_name] = converted_variations
        return processed_data

    def guardar(self, rama: str, data):
        ref = db.reference(rama)
        ref.push(data)

    def adicionar_base(self, rama: str, nombre_diag: str, sintomas):
        ref = db.reference(f"{rama}/{nombre_diag}")
        if isinstance(sintomas, set):
            sintomas_to_store = list(sintomas)
        else:
            sintomas_to_store = sintomas
        ref.set(sintomas_to_store)

    def agregar_diagnostico_completo(self, nombre_diag, sintomas_variante):
        ref_base = db.reference(f"diagnosticos_base/{nombre_diag}")
        base = ref_base.get()

        if base is None:
            raise ValueError(f"No se encontró la base para el diagnóstico '{nombre_diag}'.")

        set_base = set(base)
        if sintomas_variante == {}:
            sintomas_variante = set()
        variante_completa = set_base | sintomas_variante
        variante_lista = list(variante_completa)

        ref_def = db.reference(f"diagnosticos_definidos/{nombre_diag}")
        variantes = ref_def.get()

        if variantes is None:
            variantes = []

        if variante_lista not in variantes:
            variantes.append(variante_lista)
            ref_def.set(variantes)
        else:
            print("La variante ya existe.")

    def dev_base(self, diagnosticos_base):
        for base in diagnosticos_base:
            self.adicionar_base('diagnosticos_base', base, diagnosticos_base[base])

    def dev_definidos(self, diagnosticos_definidos):
        for definido in diagnosticos_definidos:
            for variante in diagnosticos_definidos[definido]:
                self.agregar_diagnostico_completo(definido, variante)

if __name__ == "__main__":
    dev = input('Estas seguro que estas de dev bro?')
    diagnosticodb = DiagnosticoDB()

    """
    Para leer lo de firebase si lo ocupan
    """
    # print(diagnosticodb.leer('pacientes'))
    #print(diagnosticodb.leer_base())
    #print(diagnosticodb.leer_definidos())

    """
    SOLO PONGAN LOS NUEVOS BASE QUITEN LO DEMAS, OJO PRIMERO PONGAN LOS BASE LUEGO LOS OTROS
    """
    #diagnosticos_base = {
    #     "amebiasis aguda avanzada": {
    #         "dolor abdominal", "diarrea", "heces anormales"
    #     },
    #     "amebiasis aguda inicial": {
    #         "dolor de cabeza", "pérdida de apetito", "nauseas", "vómitos"
    #     },
    #     "amebiasis crónica": {
    #         "estreñimiento", "diarrea", "dolor abdominal"
    #     },
    #     "absceso hepático amebiano": {
    #         "fiebre", "dolor abdominal", "malestar general"
    #     },
    #     "absceso amebiano pulmonar": {
    #         "dificultad para respirar", "dolor en el pecho", "tos"
    #     },
    #     "ascariasis pulmonar": {
    #         "dificultad para respirar", "dolor en el pecho", "tos", "fiebre"
    #     },
    #     "ascariasis intestinal": {
    #         "dolor abdominal", "vómitos", "nauseas"
    #     },
    #     "ascariasis pancreática": {
    #         "dolor abdominal", "nauseas", "vómitos"
    #     },
    #     "giardiasis": {
    #         "dolor abdominal", "diarrea", "heces anormales"
    #     },

    #      # virus
    #      "varicela": {
    #          "erupción cutánea con picazón", "fiebre", "cansancio"
    #      },
    #
    #      "influenza": {
    #          "fiebre o escalofríos", "dolores musculares", "fatiga", "tos"
    #      },
    #
    #      "sarampion": {
    #          "fiebre", "tos", "secreción nasal", "ojos rojos", "erupción cutánea"
    #      },
    #
    #      "norovirus": {
    #          "diarrea", "vómitos", "náuseas", "dolor de estómago"
    #      }
    #
    #  }
    # diagnosticodb.dev_base(diagnosticos_base)

    """
    Pongan {} si con el base era suficiente
    """
    #diagnosticos_definidos = {
    #     # Generales (alergia, algo aparte de micro)
    #
    #     # Virus
    #
    #     # Bacterias
    #
    #     # Parasitos
    #     "amebiasis aguda avanzada": [
    #         {"dolor en la parte superior derecha del abdomen"},
    #         {"heces con sangre o moco"},
    #         {"necesidad de defecar sin conseguirlo"},
    #     ],
    #
    #     "amebiasis aguda inicial": [
    #         {"fiebre"},
    #         {}
    #     ],
    #
    #     "amebiasis crónica": [
    #         {"diarrea explosiva", "dolor en la parte superior del abdomen",
    #                                                   "fatiga extrema", "palidez notable"},
    #         {"diarrea explosiva", "dolor en la parte superior del abdomen",
    #                                                   "dolor de cabeza"},
    #         {"diarrea explosiva", "dolor en la parte superior del abdomen",
    #                                                   "mal sabor de boca"},
    #         {"diarrea explosiva", "dolor en la parte superior del abdomen",
    #                                                   "dolor abdominal después de comer"},
    #         {"diarrea explosiva", "dolor en la parte superior del abdomen"}
    #     ],
    #
    #     "absceso hepático amebiano": [
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "sudoraciones vespertinas"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "dolor de cabeza"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "dolor en el hombro izquierdo"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "fatiga extrema", "palidez notable"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "pérdida de peso"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "coloramiento amarillo"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "alcoholismo"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "desnutrición"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen",
    #                                                           "inmunodeficiencia"},
    #         {"fiebre alta",
    #                                                           "dolor en la parte superior derecha del abdomen"}
    #     ],
    #
    #     "absceso amebiano pulmonar": [
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "tos seca"},
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "tos con flema"},
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "tos achocolatada y sabor a hígado"},
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "fiebre"},
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "malestar general"},
    #         {"dolor en el pecho que empeora al respirar o toser",
    #                                                           "sudoraciones nocturnas"}
    #     ],
    #
    #     "ascariasis pulmonar": [
    #         {"tos con sangre", "ruidos al respirar"},
    #         {"tos con sangre"},
    #     ],
    #
    #     "ascariasis intestinal": [
    #         {"dolor abdominal crónico", "falta de apetito", "diarrea"},
    #         {"intolerancia a la lactosa que no existía antes"},
    #         {"desnutrición"},
    #         {"dolor abdominal crónico", "vómitos con parásitos",
    #                                                       "estreñimiento"},  # si obstruyen
    #     ],
    #
    #     "ascariasis pancreática": [
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "coloramiento amarillo"},
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "sensibilidad al tacto en el abdomen"},
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "dolor abdominal que irradia a la espalda"},
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "dolor abdominal que irradia al hombro derecho"},
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "hinchazón de pies o tobillos"},
    #         {"dolor intenso en la parte superior del abdomen",
    #                                                        "heces color arcilla"},
    #     ],
    #
    #     "giardiasis": [
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente", "malestar general"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente", "nauseas"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente",
    #                                            "heces con alimentos sin digerir"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente",
    #                                            "heces con mucha grasa, difíciles de limpiar"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente",
    #                                            "dolor en articulaciones"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente", "sarpullido"},
    #         {"dolor en la parte superior central del abdomen",
    #                                            "diarrea pastosa, con muchos gases y maloliente"}
    #     ]

    #     # Virus
    #     "varicela": [
    #         {"pérdida de apetito", "dolor de cabeza"},
    #         {"ampollas llenas de líquido", "formación de costras"},
    #         {"erupción en el pecho, espalda y cara"},
    #         {"ampollas en la boca"},
    #         {"ampollas en los párpados"},
    #         {"ampollas en el área genital"},
    #         {"protuberancias, ampollas y costras simultáneamente"},
    #         {"malestar general", "dolor de cabeza"}
    #     ],
    #
    #     "influenza": [
    #         {"fiebre alta", "dolores musculares intensos"},
    #         {"fiebre alta", "sudoración excesiva"},
    #         {"tos seca", "dolor de garganta"},
    #         {"tos persistente", "secreción o congestión nasal"},
    #         {"fatiga extrema", "dolor de cabeza intenso"},
    #         {"dolores musculares intensos", "dolor en articulaciones"},
    #         {"dolor de garganta severo", "dificultad para tragar"},
    #         {"congestión nasal severa", "presión en los senos nasales"},
    #         {"dolor de cabeza pulsátil", "sensibilidad a la luz"},
    #         {"fatiga debilitante", "malestar general"}
    #     ],
    #
    #     "sarampion": [
    #         {"fiebre alta (más de 40°C)", "tos seca"},
    #         {"fiebre alta", "manchas de Koplik en la boca"},
    #         {"erupción cutánea en la cara", "fiebre alta"},
    #         {"erupción extendida desde la cara hacia el cuerpo", "fiebre alta"},
    #         {"ojos llorosos e inflamados", "dolor de garganta"},
    #         {"tos persistente", "malestar general"},
    #         {"erupción con pequeños bultos rojos", "fiebre superior a 40°C"},
    #         {"erupción con manchas que se fusionan", "congestión nasal severa"},
    #         {"manchas blancas con centro azulado en el interior de la boca",
    #                                           "secreción nasal abundante"},
    #         {"erupción que se extiende desde la cabeza hacia todo el cuerpo",
    #                                           "descamación de la piel"}
    #     ],
    #
    #     "norovirus": [
    #         {"diarrea líquida o blanda", "aparición repentina de síntomas"},
    #         {"vómitos frecuentes", "fiebre leve"},
    #         {"dolor o calambres estomacales intensos", "dolor de cabeza"},
    #         {"náuseas intensas", "dolores musculares"},
    #         {"diarrea acuosa", "disminución de la micción"},
    #         {"vómitos repetidos", "boca y garganta seca"},
    #         {"dolor abdominal agudo", "sensación de malestar general"},
    #         {"diarrea persistente", "mareos al ponerse de pie"},
    #         {"vómitos que duran de 1 a 3 días", "somnolencia inusual"},
    #         {"náuseas matutinas", "febrícula"}
    #     ]
    #
    # }
    # diagnosticodb.dev_definidos(diagnosticos_definidos)