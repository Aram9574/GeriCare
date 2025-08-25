from dataclasses import dataclass, field
from datetime import date, time, datetime
from typing import Dict, List, Optional, Any
import json

@dataclass
class Assessment:
    """
    Modelo de datos para una evaluación geriátrica
    """
    patient_id: int
    date: date
    time: time = field(default_factory=lambda: datetime.now().time())
    data: Dict[str, Any] = field(default_factory=dict)
    ai_analysis: str = ""
    evaluator_id: Optional[str] = None
    evaluator_name: str = "Sistema IA Geriátrico"
    assessment_type: str = "routine"  # routine, emergency, discharge, admission
    
    @property
    def severity_score(self) -> int:
        """
        Calcula un puntaje de severidad basado en los datos de la evaluación
        """
        score = 0
        
        # Signos vitales críticos
        vital_signs = self.data.get('vital_signs', {})
        
        # Presión arterial
        bp = vital_signs.get('blood_pressure', '120/80')
        if '/' in bp:
            try:
                sys_bp, dia_bp = map(int, bp.split('/'))
                if sys_bp > 180 or sys_bp < 90:
                    score += 3
                elif sys_bp > 160 or sys_bp < 100:
                    score += 2
                
                if dia_bp > 110 or dia_bp < 60:
                    score += 3
                elif dia_bp > 100 or dia_bp < 70:
                    score += 2
            except ValueError:
                pass
        
        # Frecuencia cardíaca
        hr = vital_signs.get('heart_rate', 70)
        if isinstance(hr, (int, float)):
            if hr > 120 or hr < 50:
                score += 3
            elif hr > 100 or hr < 60:
                score += 1
        
        # Temperatura
        temp = vital_signs.get('temperature', 36.5)
        if isinstance(temp, (int, float)):
            if temp > 39 or temp < 36:
                score += 3
            elif temp > 38 or temp < 36.5:
                score += 2
        
        # Saturación de oxígeno
        spo2 = vital_signs.get('oxygen_saturation', 98)
        if isinstance(spo2, (int, float)):
            if spo2 < 90:
                score += 4
            elif spo2 < 95:
                score += 2
        
        # Estado general
        general_status = self.data.get('general_status', {})
        
        # Nivel de dolor
        pain_level = general_status.get('pain_level', 0)
        if isinstance(pain_level, (int, float)):
            if pain_level >= 8:
                score += 4
            elif pain_level >= 6:
                score += 2
            elif pain_level >= 4:
                score += 1
        
        # Estado de movilidad
        mobility = general_status.get('mobility', '')
        mobility_scores = {
            'Inmóvil': 4,
            'Asistencia Total': 3,
            'Asistencia Mínima': 1,
            'Independiente': 0
        }
        score += mobility_scores.get(mobility, 0)
        
        # Apetito
        appetite = general_status.get('appetite', '')
        if appetite == 'Malo':
            score += 2
        elif appetite == 'Regular':
            score += 1
        
        # Calidad del sueño
        sleep = general_status.get('sleep', '')
        if sleep == 'Mala':
            score += 2
        elif sleep == 'Regular':
            score += 1
        
        # Estado de ánimo
        mood = general_status.get('mood', '')
        mood_scores = {
            'Agitado': 3,
            'Triste': 2,
            'Apático': 2,
            'Normal': 0,
            'Alegre': 0
        }
        score += mood_scores.get(mood, 1)
        
        # Síntomas preocupantes
        symptoms = self.data.get('symptoms', [])
        critical_symptoms = [
            'Confusión', 'Dificultad respiratoria', 'Dolor', 
            'Caídas recientes', 'Pérdida de apetito'
        ]
        
        for symptom in symptoms:
            if symptom in critical_symptoms:
                score += 2
            else:
                score += 1
        
        return min(score, 20)  # Máximo 20 puntos
    
    @property
    def severity_level(self) -> str:
        """
        Convierte el puntaje de severidad en una clasificación
        """
        score = self.severity_score
        if score >= 15:
            return "Crítico"
        elif score >= 10:
            return "Alto"
        elif score >= 5:
            return "Moderado"
        else:
            return "Bajo"
    
    @property
    def requires_immediate_attention(self) -> bool:
        """
        Determina si requiere atención médica inmediata
        """
        return self.severity_score >= 10 or "emergencia" in self.ai_analysis.lower()
    
    def get_vital_signs_summary(self) -> Dict[str, str]:
        """
        Obtiene un resumen formateado de los signos vitales
        """
        vital_signs = self.data.get('vital_signs', {})
        
        return {
            'presion_arterial': f"{vital_signs.get('blood_pressure', 'N/A')} mmHg",
            'frecuencia_cardiaca': f"{vital_signs.get('heart_rate', 'N/A')} lpm",
            'temperatura': f"{vital_signs.get('temperature', 'N/A')}°C",
            'saturacion_oxigeno': f"{vital_signs.get('oxygen_saturation', 'N/A')}%"
        }
    
    def get_symptoms_list(self) -> List[str]:
        """
        Obtiene la lista de síntomas observados
        """
        return self.data.get('symptoms', [])
    
    def has_symptom(self, symptom: str) -> bool:
        """
        Verifica si el paciente presenta un síntoma específico
        """
        symptoms = self.get_symptoms_list()
        return symptom.lower() in [s.lower() for s in symptoms]
    
    def add_note(self, note: str, note_type: str = "general"):
        """
        Añade una nota adicional a la evaluación
        """
        if 'notes' not in self.data:
            self.data['notes'] = []
        
        self.data['notes'].append({
            'timestamp': datetime.now().isoformat(),
            'type': note_type,
            'content': note,
            'author': self.evaluator_name
        })
    
    def get_notes(self, note_type: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene las notas de la evaluación, opcionalmente filtradas por tipo
        """
        notes = self.data.get('notes', [])
        if note_type:
            return [note for note in notes if note.get('type') == note_type]
        return notes
    
    def calculate_trend_indicators(self, previous_assessment: 'Assessment' = None) -> Dict[str, str]:
        """
        Calcula indicadores de tendencia comparando con evaluación previa
        """
        if not previous_assessment:
            return {}
        
        trends = {}
        
        # Comparar signos vitales
        current_vitals = self.data.get('vital_signs', {})
        previous_vitals = previous_assessment.data.get('vital_signs', {})
        
        # Presión arterial sistólica
        try:
            current_sys = int(current_vitals.get('blood_pressure', '0/0').split('/')[0])
            previous_sys = int(previous_vitals.get('blood_pressure', '0/0').split('/')[0])
            
            if current_sys > previous_sys + 10:
                trends['presion_arterial'] = '↗️ Aumentando'
            elif current_sys < previous_sys - 10:
                trends['presion_arterial'] = '↘️ Disminuyendo'
            else:
                trends['presion_arterial'] = '➡️ Estable'
        except (ValueError, IndexError):
            trends['presion_arterial'] = '❓ Sin datos'
        
        # Frecuencia cardíaca
        current_hr = current_vitals.get('heart_rate', 0)
        previous_hr = previous_vitals.get('heart_rate', 0)
        
        if isinstance(current_hr, (int, float)) and isinstance(previous_hr, (int, float)):
            if current_hr > previous_hr + 5:
                trends['frecuencia_cardiaca'] = '↗️ Aumentando'
            elif current_hr < previous_hr - 5:
                trends['frecuencia_cardiaca'] = '↘️ Disminuyendo'
            else:
                trends['frecuencia_cardiaca'] = '➡️ Estable'
        
        # Temperatura
        current_temp = current_vitals.get('temperature', 0)
        previous_temp = previous_vitals.get('temperature', 0)
        
        if isinstance(current_temp, (int, float)) and isinstance(previous_temp, (int, float)):
            if current_temp > previous_temp + 0.5:
                trends['temperatura'] = '↗️ Aumentando'
            elif current_temp < previous_temp - 0.5:
                trends['temperatura'] = '↘️ Disminuyendo'
            else:
                trends['temperatura'] = '➡️ Estable'
        
        # Comparar nivel de dolor
        current_pain = self.data.get('general_status', {}).get('pain_level', 0)
        previous_pain = previous_assessment.data.get('general_status', {}).get('pain_level', 0)
        
        if isinstance(current_pain, (int, float)) and isinstance(previous_pain, (int, float)):
            if current_pain > previous_pain + 1:
                trends['dolor'] = '↗️ Empeorando'
            elif current_pain < previous_pain - 1:
                trends['dolor'] = '↘️ Mejorando'
            else:
                trends['dolor'] = '➡️ Estable'
        
        return trends
    
    def generate_summary_text(self) -> str:
        """
        Genera un resumen textual de la evaluación
        """
        vital_signs = self.get_vital_signs_summary()
        symptoms = self.get_symptoms_list()
        
        summary = f"""
EVALUACIÓN GERIÁTRICA - {self.date.strftime('%d/%m/%Y')} a las {self.time.strftime('%H:%M')}
Severidad: {self.severity_level} (Puntuación: {self.severity_score}/20)

SIGNOS VITALES:
• Presión Arterial: {vital_signs['presion_arterial']}
• Frecuencia Cardíaca: {vital_signs['frecuencia_cardiaca']}
• Temperatura: {vital_signs['temperatura']}
• Saturación O₂: {vital_signs['saturacion_oxigeno']}

ESTADO GENERAL:
• Dolor: {self.data.get('general_status', {}).get('pain_level', 'N/A')}/10
• Movilidad: {self.data.get('general_status', {}).get('mobility', 'N/A')}
• Apetito: {self.data.get('general_status', {}).get('appetite', 'N/A')}
• Sueño: {self.data.get('general_status', {}).get('sleep', 'N/A')}
• Estado Ánimo: {self.data.get('general_status', {}).get('mood', 'N/A')}
"""
        
        if symptoms:
            summary += f"\nSÍNTOMAS OBSERVADOS:\n"
            for symptom in symptoms:
                summary += f"• {symptom}\n"
        
        if self.data.get('observations'):
            summary += f"\nOBSERVACIONES:\n{self.data['observations']}\n"
        
        if self.ai_analysis:
            summary += f"\nANÁLISIS IA:\n{self.ai_analysis}\n"
        
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la evaluación a diccionario para serialización
        """
        return {
            'patient_id': self.patient_id,
            'date': self.date.isoformat(),
            'time': self.time.isoformat(),
            'data': self.data,
            'ai_analysis': self.ai_analysis,
            'evaluator_id': self.evaluator_id,
            'evaluator_name': self.evaluator_name,
            'assessment_type': self.assessment_type,
            'severity_score': self.severity_score,
            'severity_level': self.severity_level,
            'requires_immediate_attention': self.requires_immediate_attention
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Assessment':
        """
        Crea una evaluación desde un diccionario
        """
        assessment_date = date.fromisoformat(data['date'])
        assessment_time = time.fromisoformat(data['time'])
        
        return cls(
            patient_id=data['patient_id'],
            date=assessment_date,
            time=assessment_time,
            data=data.get('data', {}),
            ai_analysis=data.get('ai_analysis', ''),
            evaluator_id=data.get('evaluator_id'),
            evaluator_name=data.get('evaluator_name', 'Sistema IA Geriátrico'),
            assessment_type=data.get('assessment_type', 'routine')
        )
    
    def validate_data(self) -> List[str]:
        """
        Valida los datos de la evaluación
        """
        errors = []
        
        if not isinstance(self.patient_id, int) or self.patient_id <= 0:
            errors.append("ID de paciente debe ser un entero positivo")
        
        if self.date > date.today():
            errors.append("La fecha de evaluación no puede ser futura")
        
        if not self.data:
            errors.append("Los datos de evaluación no pueden estar vacíos")
        
        # Validar signos vitales si están presentes
        vital_signs = self.data.get('vital_signs', {})
        if vital_signs:
            hr = vital_signs.get('heart_rate')
            if hr and (not isinstance(hr, (int, float)) or hr < 30 or hr > 200):
                errors.append("Frecuencia cardíaca debe estar entre 30 y 200")
            
            temp = vital_signs.get('temperature')
            if temp and (not isinstance(temp, (int, float)) or temp < 30 or temp > 45):
                errors.append("Temperatura debe estar entre 30 y 45°C")
            
            spo2 = vital_signs.get('oxygen_saturation')
            if spo2 and (not isinstance(spo2, (int, float)) or spo2 < 70 or spo2 > 100):
                errors.append("Saturación de oxígeno debe estar entre 70 y 100%")
        
        return errors
    
    def __str__(self) -> str:
        return f"Evaluación Paciente {self.patient_id} - {self.date} ({self.severity_level})"
    
    def __repr__(self) -> str:
        return f"Assessment(patient_id={self.patient_id}, date='{self.date}', severity='{self.severity_level}')"