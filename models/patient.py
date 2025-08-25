from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional, Any
import json

@dataclass
class Patient:
    """
    Modelo de datos para un paciente geriátrico
    """
    id: int
    name: str
    age: int
    gender: str
    room: str
    admission_date: date
    emergency_contact: str = ""
    allergies: str = ""
    medical_history: str = ""
    conditions: Dict[str, bool] = field(default_factory=dict)
    fall_risk: str = "Medio"  # Bajo, Medio, Alto
    cognitive_level: str = "Normal"  # Normal, Deterioro Leve, Moderado, Severo
    medications: List[Dict[str, Any]] = field(default_factory=list)
    care_plan: Dict[str, Any] = field(default_factory=dict)
    last_assessment_date: Optional[date] = None
    
    @property
    def risk_level(self) -> str:
        """
        Calcula el nivel de riesgo general basado en múltiples factores
        """
        risk_score = 0
        
        # Factores de edad
        if self.age >= 85:
            risk_score += 3
        elif self.age >= 80:
            risk_score += 2
        elif self.age >= 75:
            risk_score += 1
        
        # Factores cognitivos
        cognitive_risks = {
            "Deterioro Severo": 4,
            "Deterioro Moderado": 3,
            "Deterioro Leve": 2,
            "Normal": 0
        }
        risk_score += cognitive_risks.get(self.cognitive_level, 2)
        
        # Factores de caídas
        fall_risks = {
            "Alto": 4,
            "Medio": 2,
            "Bajo": 1
        }
        risk_score += fall_risks.get(self.fall_risk, 2)
        
        # Factores médicos
        high_risk_conditions = [
            'dementia', 'heart_disease', 'diabetes', 
            'depression', 'mobility_issues'
        ]
        
        for condition in high_risk_conditions:
            if self.conditions.get(condition, False):
                risk_score += 1
        
        # Polifarmacia (si tiene más de 5 medicamentos)
        if len(self.medications) > 5:
            risk_score += 2
        
        # Clasificación final
        if risk_score >= 10:
            return "Alto"
        elif risk_score >= 6:
            return "Medio"
        else:
            return "Bajo"
    
    @property
    def age_group(self) -> str:
        """
        Devuelve el grupo etario del paciente
        """
        if self.age >= 90:
            return "Nonagenario"
        elif self.age >= 80:
            return "Octogenario"
        elif self.age >= 75:
            return "Adulto Mayor Avanzado"
        elif self.age >= 65:
            return "Adulto Mayor"
        else:
            return "Menor de 65"
    
    def add_medication(self, name: str, dosage: str, frequency: str, 
                      indication: str, prescribing_doctor: str = ""):
        """
        Añade un medicamento al régimen del paciente
        """
        medication = {
            "name": name,
            "dosage": dosage,
            "frequency": frequency,
            "indication": indication,
            "prescribing_doctor": prescribing_doctor,
            "start_date": date.today().isoformat(),
            "active": True
        }
        self.medications.append(medication)
    
    def discontinue_medication(self, medication_name: str):
        """
        Descontinúa un medicamento
        """
        for med in self.medications:
            if med["name"].lower() == medication_name.lower():
                med["active"] = False
                med["end_date"] = date.today().isoformat()
                break
    
    def get_active_medications(self) -> List[Dict[str, Any]]:
        """
        Devuelve solo los medicamentos activos
        """
        return [med for med in self.medications if med.get("active", True)]
    
    def update_care_plan(self, plan_data: Dict[str, Any]):
        """
        Actualiza el plan de cuidados
        """
        self.care_plan.update(plan_data)
        self.care_plan["last_updated"] = date.today().isoformat()
    
    def get_condition_summary(self) -> str:
        """
        Devuelve un resumen de las condiciones médicas
        """
        active_conditions = [
            condition.replace('_', ' ').title() 
            for condition, active in self.conditions.items() 
            if active
        ]
        
        if active_conditions:
            return ", ".join(active_conditions)
        else:
            return "Sin condiciones médicas registradas"
    
    def days_since_admission(self) -> int:
        """
        Calcula los días desde el ingreso
        """
        return (date.today() - self.admission_date).days
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto paciente a diccionario para serialización
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "room": self.room,
            "admission_date": self.admission_date.isoformat(),
            "emergency_contact": self.emergency_contact,
            "allergies": self.allergies,
            "medical_history": self.medical_history,
            "conditions": self.conditions,
            "fall_risk": self.fall_risk,
            "cognitive_level": self.cognitive_level,
            "medications": self.medications,
            "care_plan": self.care_plan,
            "last_assessment_date": self.last_assessment_date.isoformat() if self.last_assessment_date else None,
            "risk_level": self.risk_level,
            "age_group": self.age_group,
            "days_since_admission": self.days_since_admission()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """
        Crea un objeto Patient desde un diccionario
        """
        # Convertir fechas de string a objetos date
        admission_date = date.fromisoformat(data["admission_date"])
        last_assessment_date = None
        if data.get("last_assessment_date"):
            last_assessment_date = date.fromisoformat(data["last_assessment_date"])
        
        return cls(
            id=data["id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            room=data["room"],
            admission_date=admission_date,
            emergency_contact=data.get("emergency_contact", ""),
            allergies=data.get("allergies", ""),
            medical_history=data.get("medical_history", ""),
            conditions=data.get("conditions", {}),
            fall_risk=data.get("fall_risk", "Medio"),
            cognitive_level=data.get("cognitive_level", "Normal"),
            medications=data.get("medications", []),
            care_plan=data.get("care_plan", {}),
            last_assessment_date=last_assessment_date
        )
    
    def validate_data(self) -> List[str]:
        """
        Valida los datos del paciente y devuelve lista de errores
        """
        errors = []
        
        if not self.name or len(self.name.strip()) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
        
        if not isinstance(self.age, int) or self.age < 0 or self.age > 120:
            errors.append("La edad debe ser un número entre 0 y 120")
        
        if self.gender not in ["Masculino", "Femenino", "Otro"]:
            errors.append("El género debe ser Masculino, Femenino u Otro")
        
        if self.fall_risk not in ["Bajo", "Medio", "Alto"]:
            errors.append("El riesgo de caídas debe ser Bajo, Medio o Alto")
        
        cognitive_levels = ["Normal", "Deterioro Leve", "Deterioro Moderado", "Deterioro Severo"]
        if self.cognitive_level not in cognitive_levels:
            errors.append(f"El nivel cognitivo debe ser uno de: {', '.join(cognitive_levels)}")
        
        if self.admission_date > date.today():
            errors.append("La fecha de admission no puede ser futura")
        
        return errors
    
    def __str__(self) -> str:
        return f"Paciente {self.name} (ID: {self.id}, Edad: {self.age}, Habitación: {self.room})"
    
    def __repr__(self) -> str:
        return f"Patient(id={self.id}, name='{self.name}', age={self.age}, risk_level='{self.risk_level}')"