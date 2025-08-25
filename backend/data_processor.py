import pandas as pd
import csv
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Any
import json

class DataProcessor:
    """
    Procesador de datos para generar reportes CSV y análisis estadísticos
    """
    
    def __init__(self):
        self.reports_dir = "data/reports"
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self):
        """Asegura que existe el directorio de reportes"""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_daily_report(self, assessment, patient_data=None):
        """Genera reporte CSV diario para cada evaluación de paciente"""
        try:
            today = date.today().strftime("%Y-%m-%d")
            report_filename = f"reporte_diario_{today}.csv"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            report_data = self._prepare_assessment_data_for_csv(assessment, patient_data)
            
            file_exists = os.path.exists(report_path)
            
            with open(report_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'fecha_evaluacion', 'hora_evaluacion', 'id_paciente', 'nombre_paciente',
                    'edad', 'habitacion', 'presion_sistolica', 'presion_diastolica',
                    'frecuencia_cardiaca', 'temperatura', 'saturacion_oxigeno',
                    'nivel_dolor', 'estado_movilidad', 'apetito', 'calidad_sueno',
                    'estado_animo', 'sintomas_observados', 'observaciones_adicionales',
                    'evaluador'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(report_data)
            
            return report_path
            
        except Exception as e:
            print(f"Error al generar reporte diario: {str(e)}")
            return None
    
    def _prepare_assessment_data_for_csv(self, assessment, patient_data=None) -> Dict:
        """Prepara los datos de evaluación para el formato CSV"""
        
        # Extraer datos de la evaluación
        if hasattr(assessment, 'data'):
            data = assessment.data
        elif isinstance(assessment, dict):
            data = assessment
        else:
            data = {}
        
        # Extraer signos vitales
        vital_signs = data.get('vital_signs', {})
        blood_pressure = vital_signs.get('blood_pressure', '0/0').split('/')
        
        # Extraer estado general
        general_status = data.get('general_status', {})
        
        return {
            'fecha_evaluacion': data.get('date', str(date.today())),
            'hora_evaluacion': data.get('time', datetime.now().strftime("%H:%M")),
            'id_paciente': data.get('patient_id', 'N/A'),
            'nombre_paciente': patient_data['name'] if patient_data else 'N/A',
            'edad': patient_data['age'] if patient_data else 'N/A',
            'habitacion': patient_data['room'] if patient_data else 'N/A',
            'presion_sistolica': blood_pressure[0] if len(blood_pressure) >= 1 else 'N/A',
            'presion_diastolica': blood_pressure[1] if len(blood_pressure) >= 2 else 'N/A',
            'frecuencia_cardiaca': vital_signs.get('heart_rate', 'N/A'),
            'temperatura': vital_signs.get('temperature', 'N/A'),
            'saturacion_oxigeno': vital_signs.get('oxygen_saturation', 'N/A'),
            'nivel_dolor': vital_signs.get('pain_level', 'N/A'),
            'estado_movilidad': general_status.get('mobility', 'N/A'),
            'apetito': general_status.get('appetite', 'N/A'),
            'calidad_sueno': general_status.get('sleep_quality', 'N/A'),
            'estado_animo': general_status.get('mood', 'N/A'),
            'sintomas_observados': ', '.join(data.get('symptoms', [])),
            'observaciones_adicionales': data.get('observations', ''),
            'evaluador': data.get('evaluator', 'Sistema IA Geriátrico')
        }
    
    def get_statistics_dashboard_data(self) -> Dict:
        """Obtiene datos para el dashboard de estadísticas"""
        try:
            stats_data = {
                'total_evaluations': 0,
                'unique_patients': 0,
                'urgent_cases': 0,
                'avg_vitals': {},
                'daily_evaluations': {}
            }
            
            return stats_data
            
        except Exception as e:
            return {'error': f"Error al obtener estadísticas: {str(e)}"}