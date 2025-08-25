import openai
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Any
from datetime import datetime

load_dotenv()

class GPTService:
    def __init__(self):
        """Inicializa el servicio de ChatGPT con la API key"""
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.model = "gpt-4"  # o "gpt-3.5-turbo" si prefieres
        
    def analyze_patient_condition(self, patient, assessment_data: Dict) -> str:
        """
        Analiza la condición del paciente usando IA y las guías clínicas españolas
        """
        try:
            # Construir el prompt con información del paciente y las guías clínicas
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(patient, assessment_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error al conectar con el servicio de IA: {str(e)}"
    
    def _build_system_prompt(self) -> str:
        """Construye el prompt del sistema con conocimientos geriátricos"""
        return """Eres un asistente médico especializado en geriatría que ayuda a cuidadores en residencias de ancianos en España. 

Tu conocimiento se basa en:
- Guías de práctica clínica geriátricas españolas
- Protocolos de cuidados en residencias
- Evaluación de riesgos específicos en ancianos
- Manejo de polifarmacia en geriatría
- Prevención de caídas
- Cuidados paliativos geriátricos
- Normativas sanitarias españolas

PRINCIPIOS FUNDAMENTALES:
1. Evalúa SIEMPRE el riesgo de caídas usando escalas validadas
2. Considera las interacciones medicamentosas
3. Evalúa el estado cognitivo y funcional
4. Detecta signos de deterioro o urgencias médicas
5. Proporciona recomendaciones específicas para cuidadores
6. Sugiere cuándo contactar al médico

RESPONDE SIEMPRE en formato estructurado:
## 🔍 ANÁLISIS CLÍNICO
[Evaluación de signos vitales y estado general]

## ⚠️ ALERTAS Y RIESGOS
[Factores de riesgo identificados - caídas, medicamentos, etc.]

## 📋 RECOMENDACIONES
[Acciones específicas para cuidadores]

## 🚨 URGENCIA MÉDICA
[Si requiere atención médica inmediata]

## 📊 SEGUIMIENTO
[Qué monitorizar y con qué frecuencia]

Sé específico, claro y siempre prioriza la seguridad del paciente."""

    def _build_user_prompt(self, patient, assessment_data: Dict) -> str:
        """Construye el prompt del usuario con datos del paciente"""
        
        # Información básica del paciente
        patient_info = f"""
PACIENTE: {patient.name}
Edad: {patient.age} años
Género: {patient.gender}
Habitación: {patient.room}
Riesgo de caídas conocido: {patient.fall_risk}
Nivel cognitivo: {patient.cognitive_level}

CONDICIONES MÉDICAS:
"""
        
        # Agregar condiciones médicas
        for condition, status in patient.conditions.items():
            if status:
                patient_info += f"- {condition.replace('_', ' ').title()}\n"
        
        if patient.allergies:
            patient_info += f"\nALERGIAS: {patient.allergies}"
        
        if patient.medical_history:
            patient_info += f"\nHISTORIAL: {patient.medical_history}"
        
        # Datos de la evaluación actual
        vital_signs = assessment_data['vital_signs']
        general_status = assessment_data['general_status']
        
        evaluation_info = f"""

EVALUACIÓN ACTUAL ({assessment_data['date']}):

SIGNOS VITALES:
- Presión arterial: {vital_signs['blood_pressure']} mmHg
- Frecuencia cardíaca: {vital_signs['heart_rate']} lpm
- Temperatura: {vital_signs['temperature']}°C
- Saturación O2: {vital_signs['oxygen_saturation']}%

ESTADO GENERAL:
- Dolor (0-10): {general_status['pain_level']}
- Movilidad: {general_status['mobility']}
- Apetito: {general_status['appetite']}
- Sueño: {general_status['sleep']}
- Estado de ánimo: {general_status['mood']}
"""
        
        # Síntomas observados
        if assessment_data['symptoms']:
            evaluation_info += f"\nSÍNTOMAS OBSERVADOS:\n"
            for symptom in assessment_data['symptoms']:
                evaluation_info += f"- {symptom}\n"
        
        # Observaciones adicionales
        if assessment_data['observations']:
            evaluation_info += f"\nOBSERVACIONES:\n{assessment_data['observations']}"
        
        return patient_info + evaluation_info + "\n\nPor favor, proporciona un análisis completo y recomendaciones específicas."

    def check_medication_interactions(self, medications: List[str]) -> str:
        """
        Verifica posibles interacciones entre medicamentos
        """
        try:
            prompt = f"""Analiza las siguientes medicaciones para un paciente geriátrico y identifica:
1. Posibles interacciones medicamentosas
2. Efectos adversos específicos en ancianos
3. Recomendaciones de monitorización
4. Sugerencias de optimización terapéutica

Medicamentos: {', '.join(medications)}

Responde basándote en guías farmacológicas geriátricas españolas."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un farmacólogo clínico especializado en geriatría."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error al analizar medicamentos: {str(e)}"

    def generate_care_plan(self, patient, assessment_history: List[Dict]) -> str:
        """
        Genera un plan de cuidados personalizado basado en el historial
        """
        try:
            history_summary = self._summarize_assessment_history(assessment_history)
            
            prompt = f"""Basándote en el siguiente paciente y su historial de evaluaciones, genera un plan de cuidados integral:

PACIENTE: {patient.name}, {patient.age} años
CONDICIONES: {patient.conditions}
NIVEL COGNITIVO: {patient.cognitive_level}
RIESGO DE CAÍDAS: {patient.fall_risk}

HISTORIAL DE EVALUACIONES:
{history_summary}

Genera un plan que incluya:
1. Objetivos específicos de cuidado
2. Intervenciones de enfermería
3. Medidas de prevención
4. Programa de actividades
5. Indicadores de seguimiento
6. Alertas específicas para cuidadores"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres una enfermera geriátrica especializada en planes de cuidado."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error al generar plan de cuidados: {str(e)}"

    def assess_fall_risk(self, patient, mobility_data: Dict) -> Dict:
        """
        Evalúa el riesgo de caídas usando criterios geriátricos
        """
        try:
            prompt = f"""Evalúa el riesgo de caídas para este paciente geriátrico usando escalas validadas (Morse, Downton, etc.):

PACIENTE:
- Edad: {patient.age} años
- Historial de caídas: {patient.fall_risk}
- Condiciones médicas: {patient.conditions}
- Medicamentos que pueden afectar: [list si están disponibles]

DATOS DE MOVILIDAD ACTUAL:
{json.dumps(mobility_data, indent=2)}

Proporciona:
1. Puntuación de riesgo (Bajo/Medio/Alto)
2. Factores específicos identificados
3. Medidas preventivas específicas
4. Frecuencia de evaluación recomendada"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un fisioterapeuta geriátrico especializado en prevención de caídas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            # Extraer nivel de riesgo de la respuesta para actualizar el paciente
            content = response.choices[0].message.content
            
            # Lógica simple para extraer nivel de riesgo
            risk_level = "Medio"  # Por defecto
            if "Alto" in content or "ALTO" in content:
                risk_level = "Alto"
            elif "Bajo" in content or "BAJO" in content:
                risk_level = "Bajo"
            
            return {
                "risk_level": risk_level,
                "analysis": content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "risk_level": "Indeterminado",
                "analysis": f"❌ Error al evaluar riesgo de caídas: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _summarize_assessment_history(self, history: List[Dict]) -> str:
        """
        Resume el historial de evaluaciones para contexto
        """
        if not history:
            return "Sin historial previo disponible."
        
        summary = "Resumen de evaluaciones previas:\n"
        for assessment in history[-5:]:  # Últimas 5 evaluaciones
            date = assessment.get('date', 'Fecha no disponible')
            summary += f"- {date}: "
            
            # Resumir puntos clave
            vital_signs = assessment.get('vital_signs', {})
            if vital_signs:
                summary += f"PA: {vital_signs.get('blood_pressure', 'N/A')}, "
                summary += f"FC: {vital_signs.get('heart_rate', 'N/A')}, "
                summary += f"Temp: {vital_signs.get('temperature', 'N/A')}°C"
            
            symptoms = assessment.get('symptoms', [])
            if symptoms:
                summary += f" | Síntomas: {', '.join(symptoms[:3])}"
            
            summary += "\n"
        
        return summary

    def emergency_assessment(self, patient, current_symptoms: List[str]) -> Dict:
        """
        Evaluación rápida para situaciones de emergencia
        """
        try:
            emergency_symptoms = [
                "dolor_pecho", "dificultad_respiratoria", "confusion_severa",
                "caida_reciente", "perdida_consciencia", "sangrado",
                "temperatura_alta", "dolor_abdominal_severo"
            ]
            
            # Verificar si hay síntomas de emergencia
            is_emergency = any(symptom in emergency_symptoms for symptom in current_symptoms)
            
            prompt = f"""EVALUACIÓN DE EMERGENCIA GERIÁTRICA:

Paciente: {patient.name}, {patient.age} años
Síntomas actuales: {', '.join(current_symptoms)}
Condiciones previas: {patient.conditions}

Determina:
1. ¿Es una emergencia médica? (SÍ/NO)
2. Nivel de urgencia (1-5, siendo 5 crítico)
3. Acciones inmediatas requeridas
4. ¿Requiere llamar a emergencias (112)?
5. Cuidados mientras llega ayuda

RESPONDE DE FORMA CONCISA Y CLARA."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un médico de emergencias especializado en geriatría. Prioriza la seguridad del paciente."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Muy conservador para emergencias
                max_tokens=500
            )
            
            return {
                "is_emergency": is_emergency,
                "assessment": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "requires_112": "112" in response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "is_emergency": True,  # Por seguridad, asumir emergencia si hay error
                "assessment": f"❌ Error en evaluación. Por seguridad, considere contactar servicios médicos.",
                "timestamp": datetime.now().isoformat(),
                "requires_112": len(current_symptoms) > 2  # Heurística simple
            }