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
        """Carga las guías clínicas geriátricas españolas"""
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
                        "deterioro cognitivo",
                        "polifarmacia"
                    ],
                    "extrinsecos": [
                        "obstáculos ambientales",
                        "iluminación inadecuada",
                        "calzado inadecuado",
                        "medicamentos sedantes"
                    ]
                }
            }
        }
    
    def _load_medication_database(self) -> Dict:
        """Base de datos de medicamentos con consideraciones geriátricas"""
        return {
            "antihipertensivos": {
                "iecas": {
                    "ejemplos": ["enalapril", "lisinopril", "ramipril"],
                    "consideraciones_geriatricas": [
                        "monitorizar función renal",
                        "riesgo hipotensión ortostática"
                    ]
                }
            },
            "psicotropos": {
                "benzodiacepinas": {
                    "ejemplos": ["lorazepam", "diazepam"],
                    "riesgos_geriatricos": [
                        "aumento riesgo caídas",
                        "deterioro cognitivo"
                    ]
                }
            }
        }
    
    def _load_fall_prevention_protocols(self) -> Dict:
        """Protocolos de prevención de caídas"""
        return {
            "evaluacion_inicial": {
                "anamnesis": [
                    "historial de caídas previas",
                    "medicamentos actuales",
                    "síntomas asociados"
                ],
                "exploracion_fisica": [
                    "agudeza visual",
                    "equilibrio (Romberg)",
                    "fuerza muscular"
                ]
            }
        }
    
    def _load_emergency_protocols(self) -> Dict:
        """Protocolos de emergencias geriátricas"""
        return {
            "signos_alarma": {
                "vitales": {
                    "temperatura": ">38.5°C o <36°C",
                    "presion_arterial": "<90/60 o >180/110 mmHg",
                    "frecuencia_cardiaca": "<50 o >120 lpm",
                    "saturacion_o2": "<90%"
                }
            },
            "cuando_llamar_112": [
                "parada cardiorrespiratoria",
                "alteración súbita consciencia",
                "dolor torácico con inestabilidad",
                "dificultad respiratoria severa"
            ]
        }
    
    def get_clinical_guideline(self, topic: str) -> Dict:
        """Obtiene una guía clínica específica"""
        return self.clinical_guidelines.get(topic, {})
    
    def get_medication_info(self, medication_class: str) -> Dict:
        """Obtiene información sobre una clase de medicamentos"""
        return self.medication_database.get(medication_class, {})
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Busca información en la base de conocimientos"""
        results = []
        query_lower = query.lower()
        
        # Búsqueda simple en guías clínicas
        for guideline_key, guideline_data in self.clinical_guidelines.items():
            if query_lower in guideline_key.lower():
                results.append({
                    "type": "clinical_guideline",
                    "key": guideline_key,
                    "data": guideline_data
                })
        
        return results[:5]  # Top 5 resultados