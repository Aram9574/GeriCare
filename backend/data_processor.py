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
        """
        Asegura que existe el directorio de reportes
        """
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_daily_report(self, assessment, patient_data=None):
        """
        Genera reporte CSV diario para cada evaluación de paciente
        """
        try:
            today = date.today().strftime("%Y-%m-%d")
            report_filename = f"reporte_diario_{today}.csv"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            # Preparar datos para el CSV
            report_data = self._prepare_assessment_data_for_csv(assessment, patient_data)
            
            # Verificar si el archivo ya existe
            file_exists = os.path.exists(report_path)
            
            # Escribir al CSV
            with open(report_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'fecha_evaluacion', 'hora_evaluacion', 'id_paciente', 'nombre_paciente',
                    'edad', 'habitacion', 'presion_sistolica', 'presion_diastolica',
                    'frecuencia_cardiaca', 'temperatura', 'saturacion_oxigeno',
                    'nivel_dolor', 'estado_movilidad', 'apetito', 'calidad_sueno',
                    'estado_animo', 'sintomas_observados', 'observaciones_adicionales',
                    'riesgo_caidas', 'nivel_cognitivo', 'requiere_atencion_medica',
                    'recomendaciones_ia', 'evaluador'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escribir encabezados solo si es un archivo nuevo
                if not file_exists:
                    writer.writeheader()
                
                # Escribir datos de la evaluación
                writer.writerow(report_data)
            
            print(f"✅ Reporte diario guardado en: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Error al generar reporte diario: {str(e)}")
            return None
    
    def _prepare_assessment_data_for_csv(self, assessment, patient_data=None) -> Dict:
        """
        Prepara los datos de evaluación para el formato CSV
        """
        data = assessment.data if hasattr(assessment, 'data') else assessment
        
        # Extraer signos vitales
        vital_signs = data.get('vital_signs', {})
        blood_pressure = vital_signs.get('blood_pressure', '0/0').split('/')
        
        # Extraer estado general
        general_status = data.get('general_status', {})
        
        # Determinar si requiere atención médica basado en análisis IA
        ai_analysis = getattr(assessment, 'ai_analysis', '') or data.get('ai_analysis', '')
        requires_medical_attention = self._analyze_medical_urgency(ai_analysis, vital_signs, general_status)
        
        return {
            'fecha_evaluacion': data.get('date', date.today()),
            'hora_evaluacion': data.get('time', datetime.now().time()),
            'id_paciente': data.get('patient_id', 'N/A'),
            'nombre_paciente': patient_data.name if patient_data else 'N/A',
            'edad': patient_data.age if patient_data else 'N/A',
            'habitacion': patient_data.room if patient_data else 'N/A',
            'presion_sistolica': blood_pressure[0] if len(blood_pressure) >= 1 else 'N/A',
            'presion_diastolica': blood_pressure[1] if len(blood_pressure) >= 2 else 'N/A',
            'frecuencia_cardiaca': vital_signs.get('heart_rate', 'N/A'),
            'temperatura': vital_signs.get('temperature', 'N/A'),
            'saturacion_oxigeno': vital_signs.get('oxygen_saturation', 'N/A'),
            'nivel_dolor': general_status.get('pain_level', 'N/A'),
            'estado_movilidad': general_status.get('mobility', 'N/A'),
            'apetito': general_status.get('appetite', 'N/A'),
            'calidad_sueno': general_status.get('sleep', 'N/A'),
            'estado_animo': general_status.get('mood', 'N/A'),
            'sintomas_observados': ', '.join(data.get('symptoms', [])),
            'observaciones_adicionales': data.get('observations', ''),
            'riesgo_caidas': patient_data.fall_risk if patient_data else 'N/A',
            'nivel_cognitivo': patient_data.cognitive_level if patient_data else 'N/A',
            'requiere_atencion_medica': 'Sí' if requires_medical_attention else 'No',
            'recomendaciones_ia': ai_analysis.replace('\n', ' | ') if ai_analysis else 'N/A',
            'evaluador': 'Sistema IA Geriátrico'
        }
    
    def _analyze_medical_urgency(self, ai_analysis: str, vital_signs: Dict, general_status: Dict) -> bool:
        """
        Analiza si requiere atención médica urgente basado en parámetros
        """
        # Criterios de urgencia por signos vitales
        urgent_vitals = False
        
        try:
            # Presión arterial
            bp = vital_signs.get('blood_pressure', '0/0')
            if '/' in bp:
                sys_bp, dia_bp = map(int, bp.split('/'))
                if sys_bp > 180 or sys_bp < 90 or dia_bp > 110 or dia_bp < 60:
                    urgent_vitals = True
            
            # Frecuencia cardíaca
            hr = vital_signs.get('heart_rate', 0)
            if isinstance(hr, (int, float)) and (hr > 120 or hr < 50):
                urgent_vitals = True
            
            # Temperatura
            temp = vital_signs.get('temperature', 36.5)
            if isinstance(temp, (int, float)) and (temp > 38.5 or temp < 36.0):
                urgent_vitals = True
            
            # Saturación de oxígeno
            spo2 = vital_signs.get('oxygen_saturation', 98)
            if isinstance(spo2, (int, float)) and spo2 < 90:
                urgent_vitals = True
        
        except (ValueError, TypeError):
            pass
        
        # Criterios de urgencia por dolor severo
        urgent_pain = False
        pain_level = general_status.get('pain_level', 0)
        if isinstance(pain_level, (int, float)) and pain_level >= 8:
            urgent_pain = True
        
        # Palabras clave en análisis IA que indican urgencia
        urgent_keywords = [
            'emergencia', 'urgente', 'inmediata', '112', 'crítico', 'grave',
            'hospitalización', 'médico urgente', 'atención inmediata'
        ]
        ai_urgency = any(keyword in ai_analysis.lower() for keyword in urgent_keywords)
        
        return urgent_vitals or urgent_pain or ai_urgency
    
    def generate_weekly_summary(self, start_date: date = None) -> str:
        """
        Genera resumen semanal de evaluaciones
        """
        try:
            if not start_date:
                start_date = date.today() - timedelta(days=7)
            
            end_date = start_date + timedelta(days=6)
            
            # Buscar archivos de reportes de la semana
            weekly_data = []
            current_date = start_date
            
            while current_date <= end_date:
                report_file = f"reporte_diario_{current_date.strftime('%Y-%m-%d')}.csv"
                report_path = os.path.join(self.reports_dir, report_file)
                
                if os.path.exists(report_path):
                    df = pd.read_csv(report_path)
                    weekly_data.append(df)
                
                current_date += timedelta(days=1)
            
            if not weekly_data:
                return "No hay datos disponibles para la semana seleccionada."
            
            # Combinar datos de la semana
            combined_data = pd.concat(weekly_data, ignore_index=True)
            
            # Generar estadísticas
            summary = self._generate_weekly_statistics(combined_data, start_date, end_date)
            
            # Guardar resumen semanal
            summary_filename = f"resumen_semanal_{start_date.strftime('%Y-%m-%d')}_al_{end_date.strftime('%Y-%m-%d')}.txt"
            summary_path = os.path.join(self.reports_dir, summary_filename)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            return summary_path
            
        except Exception as e:
            return f"❌ Error al generar resumen semanal: {str(e)}"
    
    def _generate_weekly_statistics(self, data: pd.DataFrame, start_date: date, end_date: date) -> str:
        """
        Genera estadísticas semanales a partir de los datos
        """
        total_evaluations = len(data)
        unique_patients = data['id_paciente'].nunique() if 'id_paciente' in data.columns else 0
        urgent_cases = data['requiere_atencion_medica'].value_counts().get('Sí', 0) if 'requiere_atencion_medica' in data.columns else 0
        
        # Estadísticas de signos vitales
        avg_temp = data['temperatura'].mean() if 'temperatura' in data.columns else 0
        avg_hr = data['frecuencia_cardiaca'].mean() if 'frecuencia_cardiaca' in data.columns else 0
        avg_spo2 = data['saturacion_oxigeno'].mean() if 'saturacion_oxigeno' in data.columns else 0
        
        # Síntomas más frecuentes
        all_symptoms = []
        if 'sintomas_observados' in data.columns:
            for symptoms_str in data['sintomas_observados'].dropna():
                if symptoms_str and symptoms_str != 'N/A':
                    symptoms = [s.strip() for s in symptoms_str.split(',')]
                    all_symptoms.extend(symptoms)
        
        symptom_counts = pd.Series(all_symptoms).value_counts().head(5)
        
        # Distribución por estado de ánimo
        mood_distribution = data['estado_animo'].value_counts() if 'estado_animo' in data.columns else pd.Series()
        
        summary = f"""
RESUMEN SEMANAL DE EVALUACIONES GERIÁTRICAS
Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}
Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

═══════════════════════════════════════════════════════════════

📊 ESTADÍSTICAS GENERALES
─────────────────────────
• Total de evaluaciones realizadas: {total_evaluations}
• Número de pacientes únicos: {unique_patients}
• Casos que requirieron atención médica: {urgent_cases}
• Porcentaje de urgencias: {(urgent_cases/total_evaluations*100):.1f}%

📈 PROMEDIOS DE SIGNOS VITALES
─────────────────────────────
• Temperatura promedio: {avg_temp:.1f}°C
• Frecuencia cardíaca promedio: {avg_hr:.0f} lpm
• Saturación oxígeno promedio: {avg_spo2:.1f}%

🔍 SÍNTOMAS MÁS FRECUENTES
─────────────────────────
"""
        
        for i, (symptom, count) in enumerate(symptom_counts.items(), 1):
            if symptom and symptom.strip():
                summary += f"{i}. {symptom}: {count} casos ({count/total_evaluations*100:.1f}%)\n"
        
        summary += f"""
😊 DISTRIBUCIÓN ESTADO DE ÁNIMO
──────────────────────────────
"""
        
        for mood, count in mood_distribution.items():
            if mood and mood != 'N/A':
                summary += f"• {mood}: {count} casos ({count/total_evaluations*100:.1f}%)\n"
        
        # Recomendaciones generales
        summary += f"""

💡 RECOMENDACIONES GENERALES
──────────────────────────
"""
        
        if urgent_cases > total_evaluations * 0.15:  # Más del 15% urgencias
            summary += "• ⚠️  Alto porcentaje de casos urgentes - Revisar protocolos de prevención\n"
        
        if avg_temp > 37.5:
            summary += "• 🌡️  Temperatura promedio elevada - Vigilar posibles procesos infecciosos\n"
        
        if 'Confusión' in [s.strip() for s in all_symptoms]:
            summary += "• 🧠  Casos de confusión detectados - Evaluar causas reversibles (medicación, infecciones)\n"
        
        if 'Caídas recientes' in [s.strip() for s in all_symptoms]:
            summary += "• ⚠️  Caídas reportadas - Reforzar medidas de prevención ambiental\n"
        
        summary += f"""

═══════════════════════════════════════════════════════════════
Reporte generado por Sistema IA Geriátrico v1.0
Para más información, consultar reportes diarios individuales
═══════════════════════════════════════════════════════════════
"""
        
        return summary
    
    def export_patient_history(self, patient_id: str, days: int = 30) -> str:
        """
        Exporta el historial completo de un paciente específico
        """
        try:
            # Buscar evaluaciones del paciente en los últimos días
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            
            patient_data = []
            current_date = start_date
            
            while current_date <= end_date:
                report_file = f"reporte_diario_{current_date.strftime('%Y-%m-%d')}.csv"
                report_path = os.path.join(self.reports_dir, report_file)
                
                if os.path.exists(report_path):
                    df = pd.read_csv(report_path)
                    patient_rows = df[df['id_paciente'] == patient_id]
                    if not patient_rows.empty:
                        patient_data.append(patient_rows)
                
                current_date += timedelta(days=1)
            
            if not patient_data:
                return f"No se encontraron datos para el paciente {patient_id} en los últimos {days} días."
            
            # Combinar datos del paciente
            combined_data = pd.concat(patient_data, ignore_index=True)
            combined_data = combined_data.sort_values('fecha_evaluacion')
            
            # Exportar a CSV
            export_filename = f"historial_paciente_{patient_id}_{start_date.strftime('%Y-%m-%d')}_al_{end_date.strftime('%Y-%m-%d')}.csv"
            export_path = os.path.join(self.reports_dir, export_filename)
            
            combined_data.to_csv(export_path, index=False, encoding='utf-8')
            
            return export_path
            
        except Exception as e:
            return f"❌ Error al exportar historial del paciente: {str(e)}"
    
    def get_statistics_dashboard_data(self) -> Dict:
        """
        Obtiene datos para el dashboard de estadísticas
        """
        try:
            # Buscar reportes de los últimos 30 días
            stats_data = {
                'total_evaluations': 0,
                'unique_patients': 0,
                'urgent_cases': 0,
                'avg_vitals': {},
                'symptom_trends': {},
                'mood_distribution': {},
                'daily_evaluations': {}
            }
            
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            current_date = start_date
            
            all_data = []
            
            while current_date <= end_date:
                report_file = f"reporte_diario_{current_date.strftime('%Y-%m-%d')}.csv"
                report_path = os.path.join(self.reports_dir, report_file)
                
                if os.path.exists(report_path):
                    df = pd.read_csv(report_path)
                    all_data.append(df)
                    
                    # Evaluaciones por día
                    stats_data['daily_evaluations'][current_date.strftime('%Y-%m-%d')] = len(df)
                
                current_date += timedelta(days=1)
            
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                
                stats_data['total_evaluations'] = len(combined_df)
                stats_data['unique_patients'] = combined_df['id_paciente'].nunique()
                stats_data['urgent_cases'] = len(combined_df[combined_df['requiere_atencion_medica'] == 'Sí'])
                
                # Promedios de signos vitales
                if 'temperatura' in combined_df.columns:
                    stats_data['avg_vitals']['temperature'] = combined_df['temperatura'].mean()
                if 'frecuencia_cardiaca' in combined_df.columns:
                    stats_data['avg_vitals']['heart_rate'] = combined_df['frecuencia_cardiaca'].mean()
                if 'saturacion_oxigeno' in combined_df.columns:
                    stats_data['avg_vitals']['oxygen_sat'] = combined_df['saturacion_oxigeno'].mean()
                
                # Distribución de estado de ánimo
                if 'estado_animo' in combined_df.columns:
                    mood_counts = combined_df['estado_animo'].value_counts().to_dict()
                    stats_data['mood_distribution'] = mood_counts
            
            return stats_data
            
        except Exception as e:
            return {'error': f"Error al obtener estadísticas: {str(e)}"}
    
    def cleanup_old_reports(self, days_to_keep: int = 365):
        """
        Limpia reportes antiguos para ahorrar espacio
        """
        try:
            cutoff_date = date.today() - timedelta(days=days_to_keep)
            deleted_files = 0
            
            for filename in os.listdir(self.reports_dir):
                if filename.startswith('reporte_diario_') and filename.endswith('.csv'):
                    # Extraer fecha del nombre del archivo
                    try:
                        date_str = filename.replace('reporte_diario_', '').replace('.csv', '')
                        file_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        
                        if file_date < cutoff_date:
                            file_path = os.path.join(self.reports_dir, filename)
                            os.remove(file_path)
                            deleted_files += 1
                    
                    except ValueError:
                        continue  # Saltar archivos con formato de fecha inválido
            
            return f"✅ {deleted_files} archivos antiguos eliminados."
            
        except Exception as e:
            return f"❌ Error al limpiar reportes antiguos: {str(e)}"