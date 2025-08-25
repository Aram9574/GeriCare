import json
import os
from typing import Dict, List, Any
from datetime import datetime

class KnowledgeBase:
    """
    Base de conocimientos con guías de práctica clínica geriátricas españolas
    """
    
    def __init__(self):
        self.clinical_guidelines = self._load_clinical_guidelines()
        self.medication_database = self._load_medication_database()
        self.fall_prevention_protocols = self._load_fall_prevention_protocols()
        self.emergency_protocols = self._load_emergency_protocols()
    
    def _load_clinical_guidelines(self) -> Dict:
        """
        Carga las guías clínicas geriátricas españolas
        """
        return {
            "evaluacion_geriatrica_integral": {
                "descripcion": "Evaluación multidimensional del paciente geriátrico",
                "dominios": {
                    "funcional": {
                        "escalas": ["Barthel", "Lawton", "Katz"],
                        "parametros": ["AVD básicas", "AVD instrumentales", "movilidad"]
                    },
                    "cognitivo": {
                        "escalas": ["MMSE", "MoCA", "Clock Test"],
                        "parametros": ["memoria", "orientación", "función ejecutiva"]
                    },
                    "afectivo": {
                        "escalas": ["GDS-15", "HAM-D"],
                        "parametros": ["depresión", "ansiedad", "apatía"]
                    },
                    "social": {
                        "evaluacion": ["soporte familiar", "recursos sociales", "vivienda"],
                        "riesgos": ["aislamiento", "maltrato", "sobrecarga cuidador"]
                    },
                    "nutricional": {
                        "escalas": ["MNA", "MUST"],
                        "parametros": ["peso", "IMC", "ingesta", "disfagia"]
                    }
                }
            },
            
            "prevencion_caidas": {
                "factores_riesgo": {
                    "intrinsecos": [
                        "edad avanzada (>80 años)",
                        "caídas previas",
                        "alteraciones del equilibrio",
                        "debilidad muscular",
                        "alteraciones visuales",
                        "deterioro cognitivo",
                        "depresión",
                        "polifarmacia",
                        "hipotensión ortostática"
                    ],
                    "extrinsecos": [
                        "obstáculos ambientales",
                        "iluminación inadecuada",
                        "calzado inadecuado",
                        "superficies resbaladizas",
                        "medicamentos sedantes"
                    ]
                },
                "escalas_evaluacion": {
                    "morse": {
                        "parametros": ["historial caídas", "diagnóstico secundario", "ayuda ambulación", "terapia IV", "marcha", "estado mental"],
                        "puntuacion": {
                            "0-24": "bajo riesgo",
                            "25-50": "riesgo moderado", 
                            "≥51": "alto riesgo"
                        }
                    },
                    "downton": {
                        "parametros": ["caídas previas", "medicamentos", "deficits sensoriales", "estado mental", "deambulación"],
                        "puntuacion": {
                            "0-2": "bajo riesgo",
                            "≥3": "alto riesgo"
                        }
                    }
                },
                "intervenciones": {
                    "ejercicio": ["entrenamiento equilibrio", "fortalecimiento muscular", "tai chi"],
                    "revision_medicamentos": ["reducir polifarmacia", "evitar sedantes", "ajustar hipotensores"],
                    "modificacion_ambiental": ["eliminar obstáculos", "mejorar iluminación", "barras apoyo"],
                    "calzado_adecuado": ["suela antideslizante", "buen ajuste", "tacón bajo"]
                }
            },
            
            "manejo_polifarmacia": {
                "criterios_beers": {
                    "medicamentos_evitar": [
                        "benzodiacepinas (>4 semanas)",
                        "antidepresivos tricíclicos",
                        "antihistamínicos primera generación",
                        "relajantes musculares",
                        "antipsicóticos (sin indicación específica)"
                    ]
                },
                "criterios_stopp_start": {
                    "stopp": "criterios para suspender medicación potencialmente inadecuada",
                    "start": "criterios para iniciar medicación potencialmente beneficiosa"
                },
                "revision_sistematica": {
                    "frecuencia": "cada 3-6 meses",
                    "aspectos": ["indicación", "efectividad", "seguridad", "adherencia", "costo"]
                }
            },
            
            "deterioro_cognitivo": {
                "evaluacion": {
                    "cribado": ["MMSE", "MoCA", "Test del reloj"],
                    "estadificacion": ["CDR", "GDS", "FAST"]
                },
                "manejo_no_farmacologico": {
                    "estimulacion_cognitiva": ["terapia ocupacional", "reminiscencia", "musicoterapia"],
                    "actividad_fisica": ["ejercicio aeróbico", "coordinación", "equilibrio"],
                    "cuidados_ambientales": ["rutinas estructuradas", "ambiente familiar", "reducir estímulos"]
                },
                "tratamiento_farmacologico": {
                    "inhibidores_acetilcolinesterasa": ["donepezilo", "rivastigmina", "galantamina"],
                    "antagonistas_nmda": ["memantina"],
                    "precauciones": ["monitorización efectos adversos", "evaluación periódica beneficio-riesgo"]
                }
            },
            
            "cuidados_paliativos": {
                "principios": [
                    "alivio del sufrimiento",
                    "respeto por la autonomía",
                    "comunicación honesta",
                    "apoyo a la familia",
                    "cuidado integral"
                ],
                "control_sintomas": {
                    "dolor": ["evaluación regular", "tratamiento multimodal", "escalera analgésica OMS"],
                    "disnea": ["oxígeno si hipoxia", "morfina", "ventilador", "posición"],
                    "nauseas_vomitos": ["antieméticos", "identificar causa"],
                    "estreñimiento": ["laxantes profilácticos con opioides"],
                    "delirium": ["identificar causas", "medidas no farmacológicas", "haloperidol si necesario"]
                }
            }
        }
    
    def _load_medication_database(self) -> Dict:
        """
        Base de datos de medicamentos con consideraciones geriátricas
        """
        return {
            "antihipertensivos": {
                "iecas": {
                    "ejemplos": ["enalapril", "lisinopril", "ramipril"],
                    "consideraciones_geriatricas": [
                        "monitorizar función renal",
                        "riesgo hipotensión ortostática",
                        "ajustar dosis según aclaramiento creatinina"
                    ],
                    "interacciones_relevantes": ["diuréticos", "AINEs", "suplementos potasio"]
                },
                "diureticos": {
                    "ejemplos": ["furosemida", "hidroclorotiazida", "indapamida"],
                    "consideraciones_geriatricas": [
                        "riesgo deshidratación",
                        "alteraciones electrolíticas",
                        "aumenta riesgo caídas"
                    ],
                    "monitorización": ["peso diario", "ionograma", "función renal"]
                }
            },
            
            "psicotropos": {
                "benzodiacepinas": {
                    "ejemplos": ["lorazepam", "diazepam", "alprazolam"],
                    "riesgos_geriatricos": [
                        "aumento riesgo caídas",
                        "deterioro cognitivo",
                        "dependencia",
                        "síndrome abstinencia"
                    ],
                    "alternativas": ["trazodona para insomnio", "técnicas relajación"]
                },
                "antidepresivos": {
                    "preferidos": ["sertralina", "citalopram", "mirtazapina"],
                    "evitar": ["amitriptilina", "imipramina", "paroxetina"],
                    "consideraciones": ["inicio dosis baja", "incremento gradual", "monitorizar efectos anticolinérgicos"]
                }
            },
            
            "analgesicos": {
                "paracetamol": {
                    "dosis_maxima": "3g/día en >75 años",
                    "precauciones": ["hepatopatía", "desnutrición"]
                },
                "aines": {
                    "riesgos": ["nefrotoxicidad", "cardiotoxicidad", "gastropatía"],
                    "uso": "menor tiempo posible, menor dosis efectiva"
                },
                "opioides": {
                    "consideraciones": ["estreñimiento", "confusión", "depresión respiratoria"],
                    "inicio": "25-50% dosis adulto joven"
                }
            }
        }
    
    def _load_fall_prevention_protocols(self) -> Dict:
        """
        Protocolos de prevención de caídas
        """
        return {
            "evaluacion_inicial": {
                "anamnesis": [
                    "historial de caídas previas",
                    "circunstancias de caídas",
                    "medicamentos actuales",
                    "síntomas asociados"
                ],
                "exploracion_fisica": [
                    "agudeza visual",
                    "equilibrio (Romberg)",
                    "marcha (Tinetti)",
                    "fuerza muscular",
                    "hipotensión ortostática"
                ]
            },
            
            "medidas_preventivas": {
                "ambientales": [
                    "iluminación adecuada (>300 lux)",
                    "eliminar alfombras sueltas",
                    "barras de apoyo en baño",
                    "altura cama apropiada",
                    "calzado antideslizante"
                ],
                "ejercicio": [
                    "entrenamiento equilibrio 3x/semana",
                    "fortalecimiento miembros inferiores",
                    "ejercicios propioceptivos",
                    "tai chi o yoga"
                ],
                "revision_medicamentos": [
                    "reducir sedantes",
                    "ajustar antihipertensivos",
                    "revisar polifarmacia",
                    "optimizar analgesia"
                ]
            },
            
            "protocolo_post_caida": {
                "evaluacion_inmediata": [
                    "descartar lesiones",
                    "signos vitales",
                    "estado neurológico",
                    "dolor o limitación movimiento"
                ],
                "investigacion_causas": [
                    "circunstancias caída",
                    "síntomas previos",
                    "factores precipitantes",
                    "medicación reciente"
                ],
                "seguimiento": [
                    "reforzar medidas preventivas",
                    "fisioterapia si indicado",
                    "apoyo psicológico",
                    "revisión plan cuidados"
                ]
            }
        }
    
    def _load_emergency_protocols(self) -> Dict:
        """
        Protocolos de emergencias geriátricas
        """
        return {
            "signos_alarma": {
                "vitales": {
                    "temperatura": ">38.5°C o <36°C",
                    "presion_arterial": "<90/60 o >180/110 mmHg",
                    "frecuencia_cardiaca": "<50 o >120 lpm",
                    "saturacion_o2": "<90%",
                    "frecuencia_respiratoria": "<12 o >25 rpm"
                },
                "neurologicos": [
                    "alteración súbita del nivel de consciencia",
                    "confusión aguda (delirium)",
                    "déficit neurológico focal",
                    "convulsiones",
                    "cefalea intensa súbita"
                ],
                "respiratorios": [
                    "disnea severa",
                    "cianosis",
                    "uso músculos accesorios",
                    "ortopnea"
                ],
                "cardiovasculares": [
                    "dolor torácico",
                    "síncope",
                    "edemas agudos",
                    "palpitaciones con inestabilidad"
                ]
            },
            
            "actuacion_inmediata": {
                "abc": ["vía aérea", "respiración", "circulación"],
                "signos_vitales": "monitorización continua",
                "posicionamiento": "según patología (fowler, trendelenburg)",
                "oxigenoterapia": "si saturación <90%",
                "acceso_vascular": "si inestabilidad hemodinámica"
            },
            
            "cuando_llamar_112": [
                "parada cardiorrespiratoria",
                "alteración súbita consciencia",
                "dolor torácico con inestabilidad",
                "dificultad respiratoria severa",
                "hemorragia abundante",
                "traumatismo grave",
                "convulsiones prolongadas"
            ],
            
            "medicamentos_emergencia": {
                "bradicardia": ["atropina 0.5mg IV"],
                "broncoespasmo": ["salbutamol inhalado", "corticoides IV"],
                "hipotension": ["suero fisiológico", "vasopresores si necesario"],
                "convulsiones": ["diacepam 5-10mg IV lento"],
                "dolor_toracico": ["AAS 100mg", "nitroglicerina sublingual"]
            }
        }
    
    def get_clinical_guideline(self, topic: str) -> Dict:
        """
        Obtiene una guía clínica específica
        """
        return self.clinical_guidelines.get(topic, {})
    
    def get_medication_info(self, medication_class: str) -> Dict:
        """
        Obtiene información sobre una clase de medicamentos
        """
        return self.medication_database.get(medication_class, {})
    
    def get_fall_prevention_protocol(self) -> Dict:
        """
        Obtiene el protocolo completo de prevención de caídas
        """
        return self.fall_prevention_protocols
    
    def get_emergency_protocol(self, emergency_type: str = None) -> Dict:
        """
        Obtiene protocolos de emergencia
        """
        if emergency_type:
            return self.emergency_protocols.get(emergency_type, {})
        return self.emergency_protocols
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """
        Busca información en la base de conocimientos
        """
        results = []
        query_lower = query.lower()
        
        # Buscar en guías clínicas
        for guideline_key, guideline_data in self.clinical_guidelines.items():
            if query_lower in guideline_key.lower() or any(query_lower in str(v).lower() for v in str(guideline_data).lower().split()):
                results.append({
                    "type": "clinical_guideline",
                    "key": guideline_key,
                    "data": guideline_data,
                    "relevance": self._calculate_relevance(query_lower, str(guideline_data).lower())
                })
        
        # Buscar en medicamentos
        for med_class, med_data in self.medication_database.items():
            if query_lower in med_class.lower() or any(query_lower in str(v).lower() for v in str(med_data).lower().split()):
                results.append({
                    "type": "medication",
                    "key": med_class,
                    "data": med_data,
                    "relevance": self._calculate_relevance(query_lower, str(med_data).lower())
                })
        
        # Ordenar por relevancia
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:5]  # Top 5 resultados
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """
        Calcula la relevancia de un texto para una consulta
        """
        query_words = query.split()
        matches = sum(1 for word in query_words if word in text)
        return matches / len(query_words) if query_words else 0
    
    def get_assessment_recommendations(self, patient_conditions: List[str]) -> Dict:
        """
        Obtiene recomendaciones de evaluación basadas en las condiciones del paciente
        """
        recommendations = {
            "escalas_recomendadas": [],
            "frecuencia_evaluacion": {},
            "parametros_especiales": []
        }
        
        condition_mapping = {
            "diabetes": {
                "escalas": ["control glucémico", "pie diabético"],
                "frecuencia": "mensual",
                "parametros": ["HbA1c", "glucemia capilar", "examen pies"]
            },
            "hypertension": {
                "escalas": ["presión arterial", "riesgo cardiovascular"],
                "frecuencia": "semanal",
                "parametros": ["PA acostado/sentado", "hipotensión ortostática"]
            },
            "demencia": {
                "escalas": ["MMSE", "CDR", "GDS"],
                "frecuencia": "trimestral",
                "parametros": ["función cognitiva", "ABVD", "síntomas psicológicos"]
            },
            "depression": {
                "escalas": ["GDS-15", "Hamilton"],
                "frecuencia": "mensual",
                "parametros": ["estado ánimo", "ideación suicida", "función social"]
            }
        }
        
        for condition in patient_conditions:
            if condition in condition_mapping:
                mapping = condition_mapping[condition]
                recommendations["escalas_recomendadas"].extend(mapping["escalas"])
                recommendations["frecuencia_evaluacion"][condition] = mapping["frecuencia"]
                recommendations["parametros_especiales"].extend(mapping["parametros"])
        
        # Eliminar duplicados
        recommendations["escalas_recomendadas"] = list(set(recommendations["escalas_recomendadas"]))
        recommendations["parametros_especiales"] = list(set(recommendations["parametros_especiales"]))
        
        return recommendations