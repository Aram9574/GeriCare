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
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"API Key encontrada: {api_key[:10]}...")
            try:
                # Versión simplificada sin parámetros problemáticos
                self.client = openai.OpenAI(
                    api_key=api_key
                )
                self.model = "gpt-3.5-turbo"  # Modelo más estable y económico
                print("✅ Cliente OpenAI inicializado correctamente")
            except Exception as e:
                print(f"❌ Error inicializando OpenAI: {e}")
                self.client = None
                self.model = None
        else:
            print("❌ NO se encontró API Key en las variables de entorno")
            self.client = None
            self.model = None
        
    def analyze_patient_condition(self, patient, assessment_data: Dict) -> str:
        """
        Analiza la condición del paciente usando IA y las guías clínicas españolas
        """
        if not self.client:
            print("⚠️ No hay cliente OpenAI disponible, usando análisis básico")
            return self._generate_basic_analysis(patient, assessment_data)
        
        try:
            print("🤖 Iniciando análisis con IA...")
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
            
            analysis_result = response.choices[0].message.content
            print("✅ Análisis IA completado correctamente")
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error en análisis IA: {e}")
            print("🔄 Usando análisis básico como respaldo")
            return self._generate_basic_analysis(patient, assessment_data)
    
    def _generate_basic_analysis(self, patient, assessment_data: Dict) -> str:
        """Genera análisis básico sin IA cuando no hay API key"""
        print("📋 Generando análisis básico...")
        
        vitals = assessment_data.get('vital_signs', {})
        general = assessment_data.get('general_status', {})
        symptoms = assessment_data.get('symptoms', [])
        
        analysis = "## 🔍 ANÁLISIS CLÍNICO BÁSICO\n\n"
        
        # Análisis de signos vitales
        bp_sys = vitals.get('systolic_bp', 120)
        bp_dia = vitals.get('diastolic_bp', 80)
        hr = vitals.get('heart_rate', 70)
        temp = vitals.get('temperature', 36.5)
        spo2 = vitals.get('oxygen_saturation', 98)
        pain = vitals.get('pain_level', 0)
        
        analysis += "**Signos Vitales Evaluados:**\n"
        analysis += f"- Presión arterial: {bp_sys}/{bp_dia} mmHg "
        if bp_sys > 180 or bp_dia > 110:
            analysis += "(🚨 CRISIS HIPERTENSIVA - Contactar médico INMEDIATAMENTE)\n"
        elif bp_sys > 160 or bp_dia > 100:
            analysis += "(⚠️ HIPERTENSIÓN SEVERA - Contactar médico)\n"
        elif bp_sys > 140 or bp_dia > 90:
            analysis += "(⚠️ Hipertensión - Monitorizar)\n"
        elif bp_sys < 90 or bp_dia < 60:
            analysis += "(⚠️ HIPOTENSIÓN - Monitorizar signos de mareo)\n"
        else:
            analysis += "(✅ Normal)\n"
            
        analysis += f"- Frecuencia cardíaca: {hr} lpm "
        if hr > 120:
            analysis += "(🚨 TAQUICARDIA SEVERA - Evaluar urgente)\n"
        elif hr > 100:
            analysis += "(⚠️ Taquicardia - Buscar causas)\n"
        elif hr < 50:
            analysis += "(⚠️ BRADICARDIA - Revisar medicación)\n"
        elif hr < 60:
            analysis += "(⚠️ Bradicardia leve)\n"
        else:
            analysis += "(✅ Normal)\n"
            
        analysis += f"- Temperatura: {temp}°C "
        if temp > 38.5:
            analysis += "(🚨 FIEBRE ALTA - Buscar foco infeccioso URGENTE)\n"
        elif temp > 37.8:
            analysis += "(⚠️ Febrícula - Monitorizar evolución)\n"
        elif temp < 36.0:
            analysis += "(⚠️ Hipotermia - Medidas de calentamiento)\n"
        else:
            analysis += "(✅ Normal)\n"
            
        analysis += f"- Saturación O₂: {spo2}% "
        if spo2 < 90:
            analysis += "(🚨 HIPOXEMIA SEVERA - Oxígeno INMEDIATO)\n"
        elif spo2 < 95:
            analysis += "(⚠️ Hipoxemia - Evaluar oxigenoterapia)\n"
        else:
            analysis += "(✅ Normal)\n"
            
        analysis += f"- Nivel de dolor: {pain}/10 "
        if pain >= 8:
            analysis += "(🚨 DOLOR SEVERO - Analgesia urgente)\n"
        elif pain >= 6:
            analysis += "(⚠️ Dolor moderado-severo - Optimizar analgesia)\n"
        elif pain >= 4:
            analysis += "(⚠️ Dolor moderado)\n"
        elif pain > 0:
            analysis += "(⚠️ Dolor leve)\n"
        else:
            analysis += "(✅ Sin dolor)\n"
        
        analysis += "\n## ⚠️ ALERTAS Y RIESGOS DETECTADOS\n\n"
        
        alerts = []
        critical_alerts = []
        
        # Alertas críticas
        if bp_sys > 180 or bp_dia > 110:
            critical_alerts.append("🚨 CRISIS HIPERTENSIVA - Llamar médico INMEDIATAMENTE")
        if hr > 120 or hr < 50:
            critical_alerts.append("🚨 Frecuencia cardíaca crítica - Evaluación urgente")
        if temp > 38.5:
            critical_alerts.append("🚨 Fiebre alta - Buscar foco infeccioso URGENTE")
        if spo2 < 90:
            critical_alerts.append("🚨 Hipoxemia severa - Administrar oxígeno INMEDIATO")
        if pain >= 8:
            critical_alerts.append("🚨 Dolor severo - Analgesia urgente requerida")
            
        # Alertas de precaución
        if bp_sys > 140 or bp_dia > 90:
            alerts.append("⚠️ Hipertensión - Controlar más frecuentemente")
        if bp_sys < 90 or bp_dia < 60:
            alerts.append("⚠️ Hipotensión - Vigilar signos de mareo y caídas")
        if hr > 100 and hr <= 120:
            alerts.append("⚠️ Taquicardia - Investigar causas (dolor, ansiedad, medicación)")
        if temp > 37.8 and temp <= 38.5:
            alerts.append("⚠️ Febrícula - Monitorizar evolución cada 2-4 horas")
        if spo2 < 95 and spo2 >= 90:
            alerts.append("⚠️ Saturación límite - Considerar oxigenoterapia")
        if pain >= 4 and pain < 8:
            alerts.append("⚠️ Dolor significativo - Revisar pauta analgésica")
            
        # Estado general
        mobility = general.get('mobility', 'N/A')
        if mobility == 'Inmóvil':
            alerts.append("⚠️ Paciente inmóvil - Riesgo úlceras y trombosis")
        elif mobility == 'Asistencia Total':
            alerts.append("⚠️ Dependencia total - Vigilar complicaciones")
            
        appetite = general.get('appetite', 'N/A')
        if appetite == 'Malo':
            alerts.append("⚠️ Pérdida apetito - Riesgo desnutrición")
            
        mood = general.get('mood', 'N/A')
        if mood == 'Triste':
            alerts.append("⚠️ Estado ánimo bajo - Evaluar depresión")
        elif mood == 'Agitado':
            alerts.append("⚠️ Agitación - Investigar causas (dolor, infección, medicación)")
        elif mood == 'Apático':
            alerts.append("⚠️ Apatía - Posible deterioro cognitivo o depresión")
            
        cognitive = general.get('cognitive_status', 'N/A')
        if cognitive == 'Confuso':
            alerts.append("⚠️ Confusión - Evaluar delirium, buscar causas reversibles")
        elif cognitive == 'Agitado':
            alerts.append("⚠️ Agitación cognitiva - Protocolo delirium")
            
        # Síntomas específicos
        if symptoms:
            for symptom in symptoms:
                if symptom == 'Dolor torácico':
                    critical_alerts.append("🚨 DOLOR TORÁCICO - Protocolo SCA inmediato")
                elif symptom == 'Dificultad respiratoria':
                    critical_alerts.append("🚨 DISNEA - Evaluación respiratoria urgente")
                elif symptom == 'Caídas recientes':
                    critical_alerts.append("🚨 CAÍDA RECIENTE - Protocolo post-caída")
                elif symptom == 'Confusión':
                    alerts.append("⚠️ Confusión - Evaluar delirium")
                elif symptom == 'Mareos':
                    alerts.append("⚠️ Mareos - Riesgo caídas, revisar medicación")
                elif symptom == 'Náuseas' or symptom == 'Vómitos':
                    alerts.append("⚠️ Síntomas digestivos - Vigilar hidratación")
        
        # Mostrar alertas
        if critical_alerts:
            analysis += "**🚨 ALERTAS CRÍTICAS - ACCIÓN INMEDIATA:**\n"
            for alert in critical_alerts:
                analysis += f"- {alert}\n"
            analysis += "\n"
            
        if alerts:
            analysis += "**⚠️ ALERTAS DE PRECAUCIÓN:**\n"
            for alert in alerts:
                analysis += f"- {alert}\n"
            analysis += "\n"
        
        if not critical_alerts and not alerts:
            analysis += "- ✅ No se detectan alertas críticas en esta evaluación\n\n"
        
        analysis += "## 📋 RECOMENDACIONES ESPECÍFICAS\n\n"
        
        recommendations = []
        
        # Recomendaciones específicas según hallazgos
        if critical_alerts:
            recommendations.append("🚨 CONTACTAR MÉDICO O SERVICIO DE URGENCIAS INMEDIATAMENTE")
            
        if bp_sys > 160:
            recommendations.append("Revisar cumplimiento medicación antihipertensiva")
        if hr > 100:
            recommendations.append("Descartar dolor, ansiedad, fiebre como causa de taquicardia")
        if temp > 37.8:
            recommendations.append("Hemocultivos y búsqueda sistemática foco infeccioso")
        if pain >= 6:
            recommendations.append("Reevaluar pauta analgésica según escalera OMS")
        if mobility == 'Inmóvil':
            recommendations.append("Cambios posturales cada 2h, colchón antiescaras")
        if appetite == 'Malo':
            recommendations.append("Evaluación nutricional y suplementos si precisa")
        if mood in ['Triste', 'Apático']:
            recommendations.append("Valoración psicológica y actividades de estimulación")
        if cognitive == 'Confuso':
            recommendations.append("Protocolo delirium: descartar causas reversibles")
            
        # Recomendaciones según condiciones del paciente
        conditions = patient.get('conditions', {})
        if conditions.get('diabetes') and temp > 37.5:
            recommendations.append("Paciente diabético con fiebre - Control glucemia estricto")
        if conditions.get('heart_disease') and hr > 100:
            recommendations.append("Cardiopatía conocida con taquicardia - ECG y monitorización")
        if conditions.get('dementia') and cognitive == 'Confuso':
            recommendations.append("Demencia con confusión aguda - Buscar desencadenantes")
            
        # Recomendaciones generales
        patient_age = patient.get('age', 75)
        if patient_age > 85:
            recommendations.append("Paciente muy anciano - Vigilancia estrecha")
        if patient.get('risk_level') == 'Alto':
            recommendations.append("Paciente alto riesgo - Evaluaciones más frecuentes")
            
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                analysis += f"{i}. {rec}\n"
        else:
            analysis += "- Continuar cuidados habituales según protocolo\n"
        
        analysis += "\n## 📊 PLAN DE SEGUIMIENTO\n\n"
        
        if critical_alerts:
            analysis += "- **Reevaluación:** En 2-4 horas o según evolución\n"
            analysis += "- **Signos vitales:** Cada 15-30 minutos hasta estabilización\n"
            analysis += "- **Contacto médico:** Inmediato\n"
        elif alerts:
            analysis += "- **Reevaluación:** En 4-8 horas\n"
            analysis += "- **Signos vitales:** Cada 2-4 horas\n"
            analysis += "- **Contacto médico:** En las próximas 24 horas\n"
        else:
            analysis += "- **Reevaluación:** En 24 horas\n"
            analysis += "- **Signos vitales:** Según protocolo habitual\n"
            analysis += "- **Contacto médico:** Si cambios significativos\n"
        
        analysis += f"\n---\n*Evaluación generada: {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n"
        analysis += "*Sistema: Asistente Geriátrico IA v1.0*"
        
        return analysis
    
    def _build_system_prompt(self) -> str:
        """Construye el prompt del sistema con conocimientos geriátricos"""
        return """Eres un médico especialista en geriatría que ayuda a cuidadores en residencias de ancianos en España. 

Tu conocimiento se basa en:
- Guías de práctica clínica geriátricas del Sistema Nacional de Salud español
- Protocolos de cuidados en residencias según normativa española
- Evaluación de riesgos específicos en ancianos
- Manejo de polifarmacia en geriatría (criterios Beers, STOPP/START)
- Prevención de caídas (escalas Morse, Downton)
- Cuidados paliativos geriátricos
- Manejo del delirium y deterioro cognitivo
- Normativa sanitaria española vigente

INSTRUCCIONES ESPECÍFICAS:
- Prioriza SIEMPRE la seguridad del paciente
- Identifica situaciones que requieren contacto médico inmediato
- Usa terminología médica precisa pero comprensible para cuidadores
- Considera las particularidades del envejecimiento normal vs patológico
- Ten en cuenta la fragilidad y pluripatología típica del anciano
- Sugiere medidas preventivas específicas

RESPONDE SIEMPRE en este formato estructurado:
## 🔍 ANÁLISIS CLÍNICO DETALLADO
[Evaluación exhaustiva de signos vitales, estado general y síntomas]

## ⚠️ ALERTAS Y FACTORES DE RIESGO
[Identifica riesgos inmediatos, caídas, medicamentosos, etc.]

## 📋 RECOMENDACIONES CLÍNICAS
[Acciones específicas priorizadas para cuidadores]

## 🚨 URGENCIA MÉDICA
[Indica claramente si requiere atención médica inmediata y por qué]

## 📊 PLAN DE SEGUIMIENTO
[Frecuencia de controles, parámetros a monitorizar, cuándo contactar médico]

Sé específico, práctico y siempre prioriza la seguridad del paciente anciano."""

    def _build_user_prompt(self, patient, assessment_data: Dict) -> str:
        """Construye el prompt del usuario con datos del paciente"""
        
        patient_info = f"""
DATOS DEL PACIENTE:
Nombre: {patient['name']}
Edad: {patient['age']} años
Género: {patient['gender']}
Habitación: {patient['room']}
Nivel de riesgo conocido: {patient.get('risk_level', 'N/A')}
Nivel cognitivo previo: {patient.get('cognitive_level', 'N/A')}
Fecha de ingreso: {patient.get('admission_date', 'N/A')}

CONDICIONES MÉDICAS CONOCIDAS:
"""
        
        conditions = patient.get('conditions', {})
        active_conditions = []
        for condition, status in conditions.items():
            if status:
                active_conditions.append(condition.replace('_', ' ').title())
        
        if active_conditions:
            patient_info += "- " + "\n- ".join(active_conditions) + "\n"
        else:
            patient_info += "- No se registran condiciones médicas específicas\n"
        
        if patient.get('allergies'):
            patient_info += f"\nALERGIAS CONOCIDAS: {patient['allergies']}"
        
        if patient.get('medical_history'):
            patient_info += f"\nHISTORIAL MÉDICO RELEVANTE: {patient['medical_history']}"
            
        if patient.get('medications'):
            patient_info += f"\nMEDICACIÓN ACTUAL: {patient['medications']}"
        
        vitals = assessment_data.get('vital_signs', {})
        general = assessment_data.get('general_status', {})
        
        evaluation_info = f"""

EVALUACIÓN ACTUAL - {assessment_data.get('date', 'fecha no registrada')} a las {assessment_data.get('time', 'hora no registrada')}:

SIGNOS VITALES:
- Presión arterial: {vitals.get('systolic_bp', 'N/A')}/{vitals.get('diastolic_bp', 'N/A')} mmHg
- Frecuencia cardíaca: {vitals.get('heart_rate', 'N/A')} latidos por minuto
- Temperatura corporal: {vitals.get('temperature', 'N/A')}°C
- Saturación de oxígeno: {vitals.get('oxygen_saturation', 'N/A')}%
- Nivel de dolor (escala 0-10): {vitals.get('pain_level', 'N/A')}

ESTADO GENERAL OBSERVADO:
- Estado de movilidad: {general.get('mobility', 'N/A')}
- Apetito: {general.get('appetite', 'N/A')}
- Calidad del sueño: {general.get('sleep_quality', 'N/A')}
- Estado de ánimo: {general.get('mood', 'N/A')}
- Estado cognitivo aparente: {general.get('cognitive_status', 'N/A')}
- Control de esfínteres: {general.get('continence', 'N/A')}
"""
        
        symptoms = assessment_data.get('symptoms', [])
        if symptoms:
            evaluation_info += f"\nSÍNTOMAS ESPECÍFICOS OBSERVADOS:\n"
            for symptom in symptoms:
                evaluation_info += f"- {symptom}\n"
        else:
            evaluation_info += f"\nSÍNTOMAS ESPECÍFICOS: No se reportan síntomas adicionales\n"
        
        observations = assessment_data.get('observations', '')
        if observations:
            evaluation_info += f"\nOBSERVACIONES ADICIONALES DEL CUIDADOR:\n{observations}\n"
        
        evaluator = assessment_data.get('evaluator', 'No especificado')
        evaluation_info += f"\nEvaluación realizada por: {evaluator}"
        
        final_prompt = patient_info + evaluation_info + """

SOLICITUD DE ANÁLISIS:
Como especialista en geriatría, proporciona un análisis clínico completo y detallado de este paciente anciano. Considera todos los factores de riesgo geriátricos, posibles interacciones y complicaciones típicas de la edad avanzada. Identifica cualquier situación que requiera atención médica inmediata y proporciona recomendaciones específicas y prácticas para el equipo de cuidadores.

Presta especial atención a:
1. Signos vitales fuera de rango normal para la edad
2. Riesgo de caídas y factores precipitantes  
3. Posible delirium o cambios cognitivos agudos
4. Signos de infección o descompensación
5. Necesidad de contacto médico urgente
6. Medidas preventivas específicas para este paciente
"""
        
        return final_prompt

    def check_medication_interactions(self, medications: List[str]) -> str:
        """Verifica posibles interacciones entre medicamentos"""
        if not self.client:
            return "Función de verificación de medicamentos requiere API key de OpenAI"
        
        try:
            prompt = f"""Analiza las siguientes medicaciones para un paciente geriátrico y identifica:
1. Posibles interacciones medicamentosas
2. Efectos adversos específicos en ancianos
3. Recomendaciones de monitorización
4. Sugerencias de optimización terapéutica

Medicamentos: {', '.join(medications)}

Responde basándote en criterios Beers y STOPP/START para geriatría."""

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
            return f"Error al analizar medicamentos: {str(e)}"