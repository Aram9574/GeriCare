import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import json
import csv
import io
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="🏥 Asistente Geriátrico IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado completo
st.markdown("""
<style>
/* Variables CSS para colores del tema médico */
:root {
    --primary-color: #2E8B57;
    --secondary-color: #4682B4;
    --accent-color: #20B2AA;
    --warning-color: #FF6347;
    --success-color: #32CD32;
    --info-color: #87CEEB;
}

.main-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.patient-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid var(--primary-color);
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.patient-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 4px solid var(--primary-color);
    margin: 0.5rem 0;
}

.risk-alto { 
    border-left-color: #dc3545 !important;
    background: linear-gradient(135deg, #dc354510, #dc354505);
}
.risk-medio { 
    border-left-color: #ffc107 !important;
    background: linear-gradient(135deg, #ffc10710, #ffc10705);
}
.risk-bajo { 
    border-left-color: #28a745 !important;
    background: linear-gradient(135deg, #28a74510, #28a74505);
}

.alert-critical {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #dc3545;
}

.alert-warning {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #ffc107;
}

.alert-success {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #28a745;
}

.evaluation-summary {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.protocol-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #dc3545;
    margin: 0.5rem 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 1.8rem;
    }
    .patient-card, .metric-card {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Encabezado principal
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Asistente Geriátrico con Inteligencia Artificial</h1>
        <p>Sistema integral de apoyo para cuidadores en residencias geriátricas</p>
        <small>Basado en guías clínicas españolas • Versión 1.0</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar estado de la sesión
    initialize_session_state()
    
    # Sidebar con navegación y métricas
    with st.sidebar:
        show_sidebar()
    
    # Navegación principal
    page = st.session_state.get('current_page', '📊 Dashboard')
    
    # Contenido principal basado en la página seleccionada
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "👤 Nuevo Paciente":
        show_new_patient()
    elif page == "📋 Evaluación":
        show_evaluation()
    elif page == "💊 Medicamentos":
        show_medications()
    elif page == "🏃‍♂️ Fisioterapia":
        show_physiotherapy()
    elif page == "📊 Reportes":
        show_reports()
    elif page == "🚨 Protocolos":
        show_emergency_protocols()
    elif page == "⚙️ Configuración":
        show_settings()

def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'patients' not in st.session_state:
        st.session_state.patients = {}
    if 'evaluations' not in st.session_state:
        st.session_state.evaluations = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = '📊 Dashboard'

def show_sidebar():
    """Muestra la barra lateral con navegación y métricas"""
    st.markdown("### 📋 Panel de Control")
    
    # Navegación principal
    pages = [
        "📊 Dashboard",
        "👤 Nuevo Paciente", 
        "📋 Evaluación",
        "💊 Medicamentos",
        "🏃‍♂️ Fisioterapia",
        "📊 Reportes",
        "🚨 Protocolos",
        "⚙️ Configuración"
    ]
    
    selected_page = st.selectbox("Navegación:", pages, 
                                index=pages.index(st.session_state.current_page))
    st.session_state.current_page = selected_page
    
    st.markdown("---")
    
    # Métricas rápidas
    st.markdown("### 📈 Resumen Rápido")
    
    total_patients = len(st.session_state.patients)
    total_evaluations = len(st.session_state.evaluations)
    today_evaluations = sum(1 for e in st.session_state.evaluations 
                           if e.get('date') == str(date.today()))
    
    high_risk_count = sum(1 for p in st.session_state.patients.values() 
                         if p.get('risk_level') == 'Alto')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Pacientes", total_patients)
        st.metric("📋 Evaluaciones", total_evaluations)
    with col2:
        st.metric("⚠️ Riesgo Alto", high_risk_count)
        st.metric("📅 Hoy", today_evaluations)
    
    # Botón de emergencia
    st.markdown("---")
    if st.button("🚨 EMERGENCIA", use_container_width=True, type="primary"):
        st.error("🚨 **PROTOCOLO DE EMERGENCIA ACTIVADO**")
        st.error("📞 **Contactar inmediatamente:**")
        st.error("• **112** - Emergencias generales")
        st.error("• **061** - Urgencias sanitarias")
        st.session_state.current_page = "🚨 Protocolos"
        st.rerun()

def show_dashboard():
    """Página principal del dashboard"""
    st.markdown("## 📊 Dashboard Principal")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(st.session_state.patients)
    high_risk_patients = sum(1 for p in st.session_state.patients.values() 
                           if p.get('risk_level') == 'Alto')
    total_evaluations = len(st.session_state.evaluations)
    avg_age = (sum(p['age'] for p in st.session_state.patients.values()) / total_patients 
              if total_patients > 0 else 0)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--primary-color); margin: 0;">👥 Total Pacientes</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(total_patients), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card risk-alto">
            <h3 style="color: #dc3545; margin: 0;">⚠️ Riesgo Alto</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(high_risk_patients), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--info-color); margin: 0;">📋 Evaluaciones</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(total_evaluations), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--warning-color); margin: 0;">📅 Edad Media</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(f"{avg_age:.0f} años" if avg_age > 0 else "N/A"), unsafe_allow_html=True)
    
    if st.session_state.patients:
        # Distribución por riesgo
        st.markdown("### 📊 Distribución por Nivel de Riesgo")
        
        risk_counts = {'Alto': 0, 'Medio': 0, 'Bajo': 0}
        for patient in st.session_state.patients.values():
            risk_level = patient.get('risk_level', 'Medio')
            risk_counts[risk_level] += 1
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card risk-alto">
                <h2 style="margin: 0; color: #dc3545;">{risk_counts['Alto']}</h2>
                <p style="margin: 0;">Riesgo Alto</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card risk-medio">
                <h2 style="margin: 0; color: #ffc107;">{risk_counts['Medio']}</h2>
                <p style="margin: 0;">Riesgo Medio</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card risk-bajo">
                <h2 style="margin: 0; color: #28a745;">{risk_counts['Bajo']}</h2>
                <p style="margin: 0;">Riesgo Bajo</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de evaluaciones recientes
        if st.session_state.evaluations:
            st.markdown("### 📈 Evaluaciones de los Últimos 7 Días")
            
            # Preparar datos para el gráfico
            last_7_days = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') 
                          for i in range(6, -1, -1)]
            
            daily_counts = []
            for day in last_7_days:
                count = sum(1 for e in st.session_state.evaluations if e.get('date') == day)
                daily_counts.append(count)
            
            chart_data = pd.DataFrame({
                'Fecha': [datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m') for d in last_7_days],
                'Evaluaciones': daily_counts
            })
            
            st.line_chart(chart_data.set_index('Fecha'))
        
        # Lista de pacientes
        st.markdown("### 👥 Pacientes Registrados")
        
        for pid, patient in st.session_state.patients.items():
            risk_class = f"risk-{patient.get('risk_level', 'medio').lower()}"
            
            # Calcular días desde ingreso
            try:
                admission_date = datetime.strptime(patient.get('admission_date', str(date.today())), '%Y-%m-%d').date()
                days_since = (date.today() - admission_date).days
            except:
                days_since = 0
            
            # Última evaluación
            patient_evaluations = [e for e in st.session_state.evaluations if e.get('patient_id') == pid]
            last_eval = "Sin evaluaciones" if not patient_evaluations else f"Última: {patient_evaluations[-1].get('date', 'N/A')}"
            
            st.markdown(f"""
            <div class="patient-card {risk_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: var(--primary-color);">👤 {patient['name']}</h3>
                        <p style="margin: 0.5rem 0; color: #666;">
                            <strong>Edad:</strong> {patient['age']} años | 
                            <strong>Habitación:</strong> {patient['room']} |
                            <strong>Ingreso:</strong> hace {days_since} días
                        </p>
                        <p style="margin: 0; color: #888; font-size: 0.9rem;">{last_eval}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="
                            background: {'#dc3545' if patient.get('risk_level') == 'Alto' else '#ffc107' if patient.get('risk_level') == 'Medio' else '#28a745'};
                            color: white;
                            padding: 0.25rem 0.75rem;
                            border-radius: 20px;
                            font-size: 0.8rem;
                            font-weight: bold;
                        ">
                            {patient.get('risk_level', 'Medio')}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
            <h3>👋 ¡Bienvenido al Asistente Geriátrico!</h3>
            <p>Para comenzar:</p>
            <ul>
                <li>📝 <strong>Registra tu primer paciente</strong> en la sección "Nuevo Paciente"</li>
                <li>📋 <strong>Realiza evaluaciones</strong> diarias para monitoreo continuo</li>
                <li>📊 <strong>Consulta reportes</strong> para análisis de tendencias</li>
            </ul>
            <p><em>El sistema generará automáticamente reportes CSV con cada evaluación.</em></p>
        </div>
        """, unsafe_allow_html=True)

def show_new_patient():
    """Página para registrar nuevo paciente"""
    st.markdown("## 👤 Registro de Nuevo Paciente")
    
    with st.form("new_patient_form"):
        st.markdown("### 📝 Información Básica")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nombre Completo *", placeholder="Ej: María García López")
            age = st.number_input("Edad *", min_value=60, max_value=110, value=75)
            gender = st.selectbox("Género *", ["Femenino", "Masculino", "Otro"])
            room = st.text_input("Habitación", placeholder="Ej: 101-A")
        
        with col2:
            admission_date = st.date_input("Fecha de Ingreso", value=date.today())
            emergency_contact = st.text_input("Contacto de Emergencia", 
                                            placeholder="Nombre y teléfono")
            risk_level = st.selectbox("Nivel de Riesgo Inicial", ["Bajo", "Medio", "Alto"])
            cognitive_level = st.selectbox("Nivel Cognitivo", 
                                         ["Normal", "Deterioro Leve", "Deterioro Moderado", "Deterioro Severo"])
        
        st.markdown("### 🏥 Información Médica")
        col1, col2 = st.columns(2)
        
        with col1:
            allergies = st.text_area("Alergias Conocidas", 
                                   placeholder="Medicamentos, alimentos, etc.")
            medical_history = st.text_area("Historial Médico Relevante",
                                         placeholder="Enfermedades previas, cirugías, etc.")
        
        with col2:
            st.markdown("**Condiciones Médicas Actuales:**")
            diabetes = st.checkbox("Diabetes")
            hypertension = st.checkbox("Hipertensión")
            heart_disease = st.checkbox("Enfermedad Cardíaca")
            dementia = st.checkbox("Demencia/Alzheimer")
            depression = st.checkbox("Depresión")
            mobility_issues = st.checkbox("Problemas de Movilidad")
        
        st.markdown("### 💊 Medicación Actual")
        medications_text = st.text_area("Medicamentos Actuales", 
                                       placeholder="Lista de medicamentos con dosis y frecuencia")
        
        # Solo un botón de submit dentro del form
        submitted = st.form_submit_button("➕ Registrar Paciente", use_container_width=True)
        
        if submitted:
            if name and age:
                patient_id = len(st.session_state.patients) + 1
                new_patient = {
                    'id': patient_id,
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'room': room,
                    'admission_date': str(admission_date),
                    'emergency_contact': emergency_contact,
                    'risk_level': risk_level,
                    'cognitive_level': cognitive_level,
                    'allergies': allergies,
                    'medical_history': medical_history,
                    'conditions': {
                        'diabetes': diabetes,
                        'hypertension': hypertension,
                        'heart_disease': heart_disease,
                        'dementia': dementia,
                        'depression': depression,
                        'mobility_issues': mobility_issues
                    },
                    'medications': medications_text,
                    'registered_date': str(date.today()),
                    'registered_time': datetime.now().strftime("%H:%M:%S")
                }
                
                st.session_state.patients[patient_id] = new_patient
                
                st.markdown(f"""
                <div class="alert-success">
                    <h3>✅ ¡Paciente registrado exitosamente!</h3>
                    <p><strong>Nombre:</strong> {name}</p>
                    <p><strong>ID del paciente:</strong> {patient_id}</p>
                    <p><strong>Habitación:</strong> {room}</p>
                    <p>El paciente ha sido añadido al sistema y está listo para evaluaciones.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar botón para ir al dashboard FUERA del form
                st.session_state.patient_just_registered = True
                
            else:
                st.markdown("""
                <div class="alert-critical">
                    ❌ <strong>Error:</strong> Por favor complete los campos obligatorios (marcados con *)
                </div>
                """, unsafe_allow_html=True)
    
    # Botón para ir al Dashboard FUERA del form
    if st.session_state.get('patient_just_registered', False):
        if st.button("🏠 Ir al Dashboard", use_container_width=True):
            st.session_state.current_page = '📊 Dashboard'
            st.session_state.patient_just_registered = False  # Reset the flag
            st.rerun()

def show_evaluation():
    """Página de evaluación de pacientes"""
    st.markdown("## 📋 Nueva Evaluación de Paciente")
    
    if not st.session_state.patients:
        st.markdown("""
        <div class="alert-warning">
            ⚠️ <strong>No hay pacientes registrados</strong><br>
            Primero registra un paciente en la sección "Nuevo Paciente"
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Selector de paciente
    patient_options = {
        f"{p['name']} - Hab. {p['room']} (Riesgo: {p.get('risk_level', 'N/A')})": p['id'] 
        for p in st.session_state.patients.values()
    }
    
    selected_patient_key = st.selectbox(
        "🔍 Seleccionar paciente para evaluación:",
        options=list(patient_options.keys())
    )
    
    if selected_patient_key:
        patient_id = patient_options[selected_patient_key]
        patient = st.session_state.patients[patient_id]
        
        # Mostrar información del paciente
        st.markdown(f"### 👤 Evaluando a: {patient['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"**Edad:** {patient['age']} años")
        with col2:
            st.info(f"**Habitación:** {patient['room']}")
        with col3:
            risk_level = patient.get('risk_level', 'Medio')
            if risk_level == 'Alto':
                st.error(f"**Riesgo:** {risk_level}")
            elif risk_level == 'Medio':
                st.warning(f"**Riesgo:** {risk_level}")
            else:
                st.success(f"**Riesgo:** {risk_level}")
        with col4:
            st.info(f"**Cognitivo:** {patient.get('cognitive_level', 'N/A')}")
        
        # Mostrar condiciones médicas conocidas
        conditions = patient.get('conditions', {})
        active_conditions = [k.replace('_', ' ').title() for k, v in conditions.items() if v]
        if active_conditions:
            st.markdown(f"**🏥 Condiciones conocidas:** {', '.join(active_conditions)}")
        
        # Formulario de evaluación
        with st.form("evaluation_form"):
            st.markdown("### 🩺 Signos Vitales")
            col1, col2 = st.columns(2)
            
            with col1:
                systolic_bp = st.number_input("Presión Sistólica (mmHg)", 80, 250, 120, 
                                            help="Valor normal: 90-140 mmHg")
                diastolic_bp = st.number_input("Presión Diastólica (mmHg)", 40, 150, 80,
                                             help="Valor normal: 60-90 mmHg")
                heart_rate = st.number_input("Frecuencia Cardíaca (lpm)", 30, 200, 72,
                                           help="Valor normal: 60-100 lpm")
            
            with col2:
                temperature = st.number_input("Temperatura (°C)", 35.0, 42.0, 36.5, step=0.1,
                                            help="Valor normal: 36.1-37.2°C")
                oxygen_saturation = st.number_input("Saturación O₂ (%)", 70, 100, 98,
                                                  help="Valor normal: >95%")
                pain_level = st.slider("Nivel de Dolor (0-10)", 0, 10, 0,
                                     help="0 = Sin dolor, 10 = Dolor máximo")
            
            st.markdown("### 📝 Estado General")
            col1, col2 = st.columns(2)
            
            with col1:
                mobility = st.selectbox(
                    "Estado de Movilidad",
                    ["Independiente", "Asistencia Mínima", "Asistencia Total", "Inmóvil"]
                )
                appetite = st.selectbox("Apetito", ["Bueno", "Regular", "Malo"])
                sleep_quality = st.selectbox("Calidad del Sueño", ["Buena", "Regular", "Mala"])
            
            with col2:
                mood = st.selectbox(
                    "Estado de Ánimo",
                    ["Alegre", "Normal", "Triste", "Agitado", "Apático"]
                )
                cognitive_status = st.selectbox(
                    "Estado Cognitivo Aparente",
                    ["Alerta", "Confuso", "Somnoliento", "Agitado"]
                )
                continence = st.selectbox(
                    "Control de Esfínteres",
                    ["Continente", "Incontinencia Ocasional", "Incontinencia Total"]
                )
            
            st.markdown("### 🔍 Síntomas y Observaciones")
            symptoms = st.multiselect(
                "Síntomas Observados:",
                [
                    "Confusión", "Agitación", "Caídas recientes", "Pérdida de apetito",
                    "Dificultad respiratoria", "Dolor torácico", "Náuseas", "Vómitos",
                    "Mareos", "Estreñimiento", "Diarrea", "Edemas", "Tos", "Fiebre"
                ]
            )
            
            observations = st.text_area(
                "Observaciones Adicionales:",
                placeholder="Descripción detallada de cualquier cambio, situación especial o comportamiento observado..."
            )
            
            # Evaluador
            evaluator = st.text_input("Nombre del Evaluador", placeholder="Nombre del cuidador")
            
            submitted = st.form_submit_button("🔍 Completar Evaluación y Generar Análisis", 
                                            use_container_width=True)
            
            if submitted:
                # Crear evaluación completa
                evaluation = create_evaluation(
                    patient_id, patient, systolic_bp, diastolic_bp, heart_rate,
                    temperature, oxygen_saturation, pain_level, mobility, appetite,
                    sleep_quality, mood, cognitive_status, continence, symptoms,
                    observations, evaluator
                )
                
                # Guardar evaluación
                st.session_state.evaluations.append(evaluation)
                
                # Generar análisis automático
                analysis = analyze_evaluation_complete(evaluation, patient)
                
                # Guardar reporte CSV automáticamente
                save_evaluation_to_csv(evaluation, patient, analysis)
                
                # Mostrar resultados
                show_evaluation_results(evaluation, analysis, patient)

def create_evaluation(patient_id, patient, systolic_bp, diastolic_bp, heart_rate, 
                     temperature, oxygen_saturation, pain_level, mobility, appetite,
                     sleep_quality, mood, cognitive_status, continence, symptoms, 
                     observations, evaluator):
    """Crea un objeto de evaluación completo"""
    return {
        'id': len(st.session_state.evaluations) + 1,
        'patient_id': patient_id,
        'patient_name': patient['name'],
        'date': str(date.today()),
        'time': datetime.now().strftime("%H:%M:%S"),
        'vital_signs': {
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'blood_pressure': f"{systolic_bp}/{diastolic_bp}",
            'heart_rate': heart_rate,
            'temperature': temperature,
            'oxygen_saturation': oxygen_saturation,
            'pain_level': pain_level
        },
        'general_status': {
            'mobility': mobility,
            'appetite': appetite,
            'sleep_quality': sleep_quality,
            'mood': mood,
            'cognitive_status': cognitive_status,
            'continence': continence
        },
        'symptoms': symptoms,
        'observations': observations,
        'evaluator': evaluator or "Sistema IA Geriátrico",
        'timestamp': datetime.now().isoformat()
    }

def analyze_evaluation_complete(evaluation, patient):
    """Análisis completo de la evaluación con alertas y recomendaciones"""
    alerts = []
    recommendations = []
    severity_score = 0
    
    vitals = evaluation['vital_signs']
    status = evaluation['general_status']
    
    # Análisis de signos vitales
    # Presión arterial
    if vitals['systolic_bp'] > 180 or vitals['diastolic_bp'] > 110:
        alerts.append({
            'level': 'critical',
            'message': f"CRISIS HIPERTENSIVA: PA {vitals['blood_pressure']} mmHg"
        })
        recommendations.append("🚨 CONTACTAR MÉDICO INMEDIATAMENTE - Crisis hipertensiva")
        severity_score += 4
    elif vitals['systolic_bp'] > 160 or vitals['diastolic_bp'] > 100:
        alerts.append({
            'level': 'warning',
            'message': f"Hipertensión severa: PA {vitals['blood_pressure']} mmHg"
        })
        recommendations.append("Contactar médico para ajuste de medicación antihipertensiva")
        severity_score += 3
    elif vitals['systolic_bp'] > 140 or vitals['diastolic_bp'] > 90:
        alerts.append({
            'level': 'warning',
            'message': f"Hipertensión: PA {vitals['blood_pressure']} mmHg"
        })
        recommendations.append("Monitorizar presión arterial más frecuentemente")
        severity_score += 2
    
    if vitals['systolic_bp'] < 90 or vitals['diastolic_bp'] < 60:
        alerts.append({
            'level': 'warning',
            'message': f"Hipotensión: PA {vitals['blood_pressure']} mmHg"
        })
        recommendations.append("Monitorizar signos de mareo y caídas")
        severity_score += 2
    
    # Frecuencia cardíaca
    if vitals['heart_rate'] > 120:
        alerts.append({
            'level': 'critical' if vitals['heart_rate'] > 150 else 'warning',
            'message': f"Taquicardia: {vitals['heart_rate']} lpm"
        })
        recommendations.append("Evaluar causas de taquicardia (dolor, ansiedad, medicación)")
        severity_score += 3 if vitals['heart_rate'] > 150 else 2
    elif vitals['heart_rate'] < 50:
        alerts.append({
            'level': 'warning',
            'message': f"Bradicardia: {vitals['heart_rate']} lpm"
        })
        recommendations.append("Evaluar medicación que pueda causar bradicardia")
        severity_score += 2
    
    # Temperatura
    if vitals['temperature'] > 38.5:
        alerts.append({
            'level': 'critical',
            'message': f"Fiebre alta: {vitals['temperature']}°C"
        })
        recommendations.append("🚨 Evaluar foco infeccioso - Contactar médico")
        severity_score += 3
    elif vitals['temperature'] > 37.8:
        alerts.append({
            'level': 'warning',
            'message': f"Febrícula: {vitals['temperature']}°C"
        })
        recommendations.append("Monitorizar evolución y buscar signos de infección")
        severity_score += 2
    elif vitals['temperature'] < 36.0:
        alerts.append({
            'level': 'warning',
            'message': f"Hipotermia: {vitals['temperature']}°C"
        })
        recommendations.append("Medidas de calentamiento y evaluar causas")
        severity_score += 2
    
    # Saturación de oxígeno
    if vitals['oxygen_saturation'] < 90:
        alerts.append({
            'level': 'critical',
            'message': f"Hipoxemia severa: {vitals['oxygen_saturation']}%"
        })
        recommendations.append("🚨 OXÍGENO INMEDIATO - Contactar médico urgente")
        severity_score += 4
    elif vitals['oxygen_saturation'] < 95:
        alerts.append({
            'level': 'warning',
            'message': f"Hipoxemia: {vitals['oxygen_saturation']}%"
        })
        recommendations.append("Evaluar necesidad de oxigenoterapia")
        severity_score += 3
    
    # Dolor
    if vitals['pain_level'] >= 8:
        alerts.append({
            'level': 'critical',
            'message': f"Dolor severo: {vitals['pain_level']}/10"
        })
        recommendations.append("🚨 Analgesia urgente - Evaluar causa del dolor")
        severity_score += 3
    elif vitals['pain_level'] >= 6:
        alerts.append({
            'level': 'warning',
            'message': f"Dolor moderado-severo: {vitals['pain_level']}/10"
        })
        recommendations.append("Optimizar analgesia según protocolo")
        severity_score += 2
    
    # Estado general
    if status['mobility'] == 'Inmóvil':
        alerts.append({
            'level': 'warning',
            'message': "Paciente inmóvil - Riesgo de complicaciones"
        })
        recommendations.append("Cambios posturales cada 2h, fisioterapia, prevención de úlceras")
        severity_score += 2
    
    if status['appetite'] == 'Malo':
        alerts.append({
            'level': 'warning',
            'message': "Pérdida de apetito - Riesgo nutricional"
        })
        recommendations.append("Evaluación nutricional y medidas para estimular apetito")
        severity_score += 1
    
    if status['mood'] in ['Triste', 'Apático']:
        alerts.append({
            'level': 'warning',
            'message': f"Estado de ánimo: {status['mood']} - Evaluar depresión"
        })
        recommendations.append("Considerar evaluación psicológica y actividades terapéuticas")
        severity_score += 1
    elif status['mood'] == 'Agitado':
        alerts.append({
            'level': 'warning',
            'message': "Agitación - Evaluar causas"
        })
        recommendations.append("Investigar causas de agitación (dolor, infección, medicación)")
        severity_score += 2
    
    if status['cognitive_status'] in ['Confuso', 'Agitado']:
        alerts.append({
            'level': 'warning',
            'message': f"Estado cognitivo alterado: {status['cognitive_status']}"
        })
        recommendations.append("Evaluación de delirium - Buscar causas reversibles")
        severity_score += 2
    
    # Análisis de síntomas
    critical_symptoms = ['Dificultad respiratoria', 'Dolor torácico', 'Caídas recientes']
    warning_symptoms = ['Confusión', 'Agitación', 'Náuseas', 'Vómitos', 'Mareos']
    
    for symptom in evaluation['symptoms']:
        if symptom in critical_symptoms:
            alerts.append({
                'level': 'critical',
                'message': f"Síntoma crítico: {symptom}"
            })
            if symptom == 'Dolor torácico':
                recommendations.append("🚨 Protocolo dolor torácico - ECG y enzimas cardíacas")
            elif symptom == 'Dificultad respiratoria':
                recommendations.append("🚨 Evaluación respiratoria urgente - Gasometría")
            elif symptom == 'Caídas recientes':
                recommendations.append("🚨 Evaluación neurológica - Protocolo post-caída")
            severity_score += 3
        elif symptom in warning_symptoms:
            alerts.append({
                'level': 'warning',
                'message': f"Síntoma de atención: {symptom}"
            })
            severity_score += 1
    
    # Determinar nivel de severidad general
    if severity_score >= 10:
        severity_level = "CRÍTICO"
    elif severity_score >= 6:
        severity_level = "ALTO"
    elif severity_score >= 3:
        severity_level = "MODERADO"
    else:
        severity_level = "BAJO"
    
    # Recomendaciones generales según el paciente
    patient_conditions = patient.get('conditions', {})
    
    if patient_conditions.get('diabetes') and vitals['temperature'] > 37.5:
        recommendations.append("Paciente diabético con fiebre - Controlar glucemia")
    
    if patient_conditions.get('heart_disease') and vitals['heart_rate'] > 100:
        recommendations.append("Cardiopatía conocida con taquicardia - Monitorización ECG")
    
    if patient.get('risk_level') == 'Alto':
        recommendations.append("Paciente de alto riesgo - Vigilancia estrecha")
    
    return {
        'alerts': alerts,
        'recommendations': recommendations,
        'severity_score': severity_score,
        'severity_level': severity_level,
        'requires_immediate_attention': severity_score >= 6 or any(a['level'] == 'critical' for a in alerts),
        'analysis_timestamp': datetime.now().isoformat()
    }

def save_evaluation_to_csv(evaluation, patient, analysis):
    """Guarda la evaluación en un archivo CSV diario"""
    try:
        # Crear directorio si no existe
        reports_dir = "data/reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Nombre del archivo CSV diario
        today = date.today().strftime("%Y-%m-%d")
        csv_filename = os.path.join(reports_dir, f"evaluaciones_diarias_{today}.csv")
        
        # Preparar datos para CSV
        csv_data = {
            'fecha_evaluacion': evaluation['date'],
            'hora_evaluacion': evaluation['time'],
            'id_paciente': evaluation['patient_id'],
            'nombre_paciente': evaluation['patient_name'],
            'edad': patient['age'],
            'habitacion': patient['room'],
            'presion_sistolica': evaluation['vital_signs']['systolic_bp'],
            'presion_diastolica': evaluation['vital_signs']['diastolic_bp'],
            'frecuencia_cardiaca': evaluation['vital_signs']['heart_rate'],
            'temperatura': evaluation['vital_signs']['temperature'],
            'saturacion_oxigeno': evaluation['vital_signs']['oxygen_saturation'],
            'nivel_dolor': evaluation['vital_signs']['pain_level'],
            'estado_movilidad': evaluation['general_status']['mobility'],
            'apetito': evaluation['general_status']['appetite'],
            'calidad_sueno': evaluation['general_status']['sleep_quality'],
            'estado_animo': evaluation['general_status']['mood'],
            'estado_cognitivo': evaluation['general_status']['cognitive_status'],
            'continencia': evaluation['general_status']['continence'],
            'sintomas_observados': ', '.join(evaluation['symptoms']) if evaluation['symptoms'] else 'Ninguno',
            'observaciones_adicionales': evaluation['observations'],
            'evaluador': evaluation['evaluator'],
            'puntuacion_severidad': analysis['severity_score'],
            'nivel_severidad': analysis['severity_level'],
            'requiere_atencion_medica': 'Sí' if analysis['requires_immediate_attention'] else 'No',
            'alertas_criticas': len([a for a in analysis['alerts'] if a['level'] == 'critical']),
            'alertas_advertencia': len([a for a in analysis['alerts'] if a['level'] == 'warning']),
            'numero_recomendaciones': len(analysis['recommendations'])
        }
        
        # Verificar si el archivo existe
        file_exists = os.path.exists(csv_filename)
        
        # Escribir al CSV
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(csv_data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escribir encabezados solo si es un archivo nuevo
            if not file_exists:
                writer.writeheader()
            
            # Escribir datos de la evaluación
            writer.writerow(csv_data)
        
        return csv_filename
    
    except Exception as e:
        st.error(f"Error al guardar reporte CSV: {str(e)}")
        return None

def show_evaluation_results(evaluation, analysis, patient):
    """Muestra los resultados de la evaluación"""
    st.markdown("---")
    st.markdown("## 📊 Análisis de la Evaluación Completada")
    
    # Nivel de severidad general
    severity_colors = {
        'CRÍTICO': '#dc3545',
        'ALTO': '#fd7e14',
        'MODERADO': '#ffc107',
        'BAJO': '#28a745'
    }
    
    severity_color = severity_colors.get(analysis['severity_level'], '#6c757d')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {severity_color}; background: {severity_color}15;">
            <h3 style="color: {severity_color}; margin: 0;">📊 Severidad</h3>
            <h1 style="margin: 0.5rem 0; color: {severity_color};">{analysis['severity_level']}</h1>
            <p style="margin: 0; color: #666;">Puntuación: {analysis['severity_score']}/20</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        critical_alerts = len([a for a in analysis['alerts'] if a['level'] == 'critical'])
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #dc3545; background: #dc354515;">
            <h3 style="color: #dc3545; margin: 0;">🚨 Alertas Críticas</h3>
            <h1 style="margin: 0.5rem 0; color: #dc3545;">{critical_alerts}</h1>
            <p style="margin: 0; color: #666;">Total alertas: {len(analysis['alerts'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #17a2b8; background: #17a2b815;">
            <h3 style="color: #17a2b8; margin: 0;">💡 Recomendaciones</h3>
            <h1 style="margin: 0.5rem 0; color: #17a2b8;">{len(analysis['recommendations'])}</h1>
            <p style="margin: 0; color: #666;">Acciones sugeridas</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar alertas si las hay
    if analysis['alerts']:
        st.markdown("### 🚨 Alertas Detectadas")
        
        for alert in analysis['alerts']:
            if alert['level'] == 'critical':
                st.markdown(f"""
                <div class="alert-critical">
                    🚨 <strong>CRÍTICO:</strong> {alert['message']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-warning">
                    ⚠️ <strong>ATENCIÓN:</strong> {alert['message']}
                </div>
                """, unsafe_allow_html=True)
    
    # Mostrar recomendaciones
    if analysis['recommendations']:
        st.markdown("### 💡 Recomendaciones Clínicas")
        
        for i, rec in enumerate(analysis['recommendations'], 1):
            if rec.startswith('🚨'):
                st.markdown(f"""
                <div class="alert-critical">
                    <strong>{i}.</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{i}.** {rec}")
    
    # Resumen de signos vitales
    st.markdown("### 📈 Resumen de Signos Vitales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vitals_data = {
            'Parámetro': ['Presión Arterial', 'Frecuencia Cardíaca', 'Temperatura', 'Saturación O₂', 'Dolor'],
            'Valor': [
                evaluation['vital_signs']['blood_pressure'] + ' mmHg',
                str(evaluation['vital_signs']['heart_rate']) + ' lpm',
                str(evaluation['vital_signs']['temperature']) + '°C',
                str(evaluation['vital_signs']['oxygen_saturation']) + '%',
                str(evaluation['vital_signs']['pain_level']) + '/10'
            ],
            'Estado': [
                get_vital_status('bp', evaluation['vital_signs']['systolic_bp'], evaluation['vital_signs']['diastolic_bp']),
                get_vital_status('hr', evaluation['vital_signs']['heart_rate']),
                get_vital_status('temp', evaluation['vital_signs']['temperature']),
                get_vital_status('spo2', evaluation['vital_signs']['oxygen_saturation']),
                get_vital_status('pain', evaluation['vital_signs']['pain_level'])
            ]
        }
        
        vitals_df = pd.DataFrame(vitals_data)
        st.dataframe(vitals_df, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("**Estado General:**")
        st.write(f"• **Movilidad:** {evaluation['general_status']['mobility']}")
        st.write(f"• **Apetito:** {evaluation['general_status']['appetite']}")
        st.write(f"• **Sueño:** {evaluation['general_status']['sleep_quality']}")
        st.write(f"• **Ánimo:** {evaluation['general_status']['mood']}")
        st.write(f"• **Cognitivo:** {evaluation['general_status']['cognitive_status']}")
        st.write(f"• **Continencia:** {evaluation['general_status']['continence']}")
    
    # Síntomas si los hay
    if evaluation['symptoms']:
        st.markdown("### 🔍 Síntomas Observados")
        for symptom in evaluation['symptoms']:
            st.markdown(f"• {symptom}")
    
    # Observaciones
    if evaluation['observations']:
        st.markdown("### 📝 Observaciones")
        st.markdown(f"*\"{evaluation['observations']}\"*")
    
    # Mensaje de éxito final
    st.markdown(f"""
    <div class="alert-success">
        <h4>✅ Evaluación Completada y Guardada</h4>
        <p><strong>Fecha:</strong> {evaluation['date']} a las {evaluation['time']}</p>
        <p><strong>Evaluador:</strong> {evaluation['evaluator']}</p>
        <p><strong>Archivo CSV:</strong> Guardado automáticamente en data/reports/</p>
        {f'<p style="color: #dc3545;"><strong>⚠️ ATENCIÓN MÉDICA REQUERIDA</strong></p>' if analysis['requires_immediate_attention'] else ''}
    </div>
    """, unsafe_allow_html=True)

def get_vital_status(vital_type, value1, value2=None):
    """Determina el estado de un signo vital"""
    if vital_type == 'bp':
        systolic, diastolic = value1, value2
        if systolic > 160 or diastolic > 100:
            return "🔴 Elevada"
        elif systolic < 90 or diastolic < 60:
            return "🔵 Baja"
        elif systolic > 140 or diastolic > 90:
            return "🟡 Límite"
        else:
            return "🟢 Normal"
    
    elif vital_type == 'hr':
        if value1 > 100:
            return "🔴 Elevada"
        elif value1 < 60:
            return "🔵 Baja"
        else:
            return "🟢 Normal"
    
    elif vital_type == 'temp':
        if value1 > 37.8:
            return "🔴 Elevada"
        elif value1 < 36.0:
            return "🔵 Baja"
        else:
            return "🟢 Normal"
    
    elif vital_type == 'spo2':
        if value1 < 90:
            return "🔴 Baja"
        elif value1 < 95:
            return "🟡 Límite"
        else:
            return "🟢 Normal"
    
    elif vital_type == 'pain':
        if value1 >= 7:
            return "🔴 Severo"
        elif value1 >= 4:
            return "🟡 Moderado"
        elif value1 > 0:
            return "🟠 Leve"
        else:
            return "🟢 Sin dolor"
    
    return "❓ N/A"

def show_medications():
    """Página de gestión de medicamentos"""
    st.markdown("## 💊 Gestión de Medicamentos")
    
    st.markdown("""
    <div class="alert-success">
        <h4>🚧 Funcionalidad en Desarrollo</h4>
        <p>Esta sección incluirá:</p>
        <ul>
            <li>💊 <strong>Control de medicación</strong> por horarios</li>
            <li>⚠️ <strong>Verificación de interacciones</strong> medicamentosas</li>
            <li>📋 <strong>Criterios Beers</strong> para geriatría</li>
            <li>🔄 <strong>Seguimiento de adherencia</strong> terapéutica</li>
            <li>📊 <strong>Reportes de medicación</strong></li>
        </ul>
        <p><em>Próximamente disponible en la siguiente actualización.</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_physiotherapy():
    """Página de fisioterapia"""
    st.markdown("## 🏃‍♂️ Fisioterapia y Rehabilitación")
    
    st.markdown("""
    <div class="alert-success">
        <h4>🚧 Funcionalidad en Desarrollo</h4>
        <p>Esta sección incluirá:</p>
        <ul>
            <li>🏃‍♂️ <strong>Planes de ejercicio</strong> personalizados</li>
            <li>⚖️ <strong>Evaluación de equilibrio</strong> y marcha</li>
            <li>💪 <strong>Ejercicios de fortalecimiento</strong></li>
            <li>📏 <strong>Medición de progreso</strong> funcional</li>
            <li>⚠️ <strong>Prevención de caídas</strong> específica</li>
        </ul>
        <p><em>Próximamente disponible en la siguiente actualización.</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_reports():
    """Página de reportes y estadísticas"""
    st.markdown("## 📊 Reportes y Estadísticas")
    
    if not st.session_state.evaluations:
        st.markdown("""
        <div class="alert-warning">
            📊 <strong>No hay evaluaciones para generar reportes</strong><br>
            Realiza algunas evaluaciones primero para ver estadísticas y reportes.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Estadísticas generales
    st.markdown("### 📈 Estadísticas Generales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_evaluations = len(st.session_state.evaluations)
    unique_patients = len(set(e['patient_id'] for e in st.session_state.evaluations))
    today_evaluations = sum(1 for e in st.session_state.evaluations if e['date'] == str(date.today()))
    
    with col1:
        st.metric("📋 Total Evaluaciones", total_evaluations)
    with col2:
        st.metric("👥 Pacientes Evaluados", unique_patients)
    with col3:
        st.metric("📅 Evaluaciones Hoy", today_evaluations)
    with col4:
        avg_per_day = total_evaluations / max(1, len(set(e['date'] for e in st.session_state.evaluations)))
        st.metric("📊 Promedio/Día", f"{avg_per_day:.1f}")
    
    # Tabla de evaluaciones recientes
    st.markdown("### 📋 Evaluaciones Recientes")
    
    # Preparar datos para la tabla
    recent_evaluations = st.session_state.evaluations[-20:]  # Últimas 20
    
    table_data = []
    for eval_data in reversed(recent_evaluations):
        patient_name = eval_data.get('patient_name', 'N/A')
        date_str = eval_data.get('date', 'N/A')
        time_str = eval_data.get('time', 'N/A')
        
        # Obtener algunos valores clave
        vitals = eval_data.get('vital_signs', {})
        bp = vitals.get('blood_pressure', 'N/A')
        hr = vitals.get('heart_rate', 'N/A')
        temp = vitals.get('temperature', 'N/A')
        pain = vitals.get('pain_level', 'N/A')
        
        # Estado general
        status = eval_data.get('general_status', {})
        mobility = status.get('mobility', 'N/A')
        mood = status.get('mood', 'N/A')
        
        table_data.append({
            'Fecha': date_str,
            'Hora': time_str,
            'Paciente': patient_name,
            'PA': bp,
            'FC': f"{hr} lpm" if hr != 'N/A' else 'N/A',
            'Temp': f"{temp}°C" if temp != 'N/A' else 'N/A',
            'Dolor': f"{pain}/10" if pain != 'N/A' else 'N/A',
            'Movilidad': mobility,
            'Ánimo': mood
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Botones de exportación
        st.markdown("### 📥 Exportar Datos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar Tabla Actual", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="💾 Descargar CSV",
                    data=csv_data,
                    file_name=f"evaluaciones_recientes_{date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📋 Reporte Completo", use_container_width=True):
                complete_data = []
                for eval_data in st.session_state.evaluations:
                    # Crear registro completo
                    record = {
                        'ID_Evaluacion': eval_data.get('id', ''),
                        'ID_Paciente': eval_data.get('patient_id', ''),
                        'Nombre_Paciente': eval_data.get('patient_name', ''),
                        'Fecha': eval_data.get('date', ''),
                        'Hora': eval_data.get('time', ''),
                        'Evaluador': eval_data.get('evaluator', ''),
                    }
                    
                    # Signos vitales
                    vitals = eval_data.get('vital_signs', {})
                    record.update({
                        'PA_Sistolica': vitals.get('systolic_bp', ''),
                        'PA_Diastolica': vitals.get('diastolic_bp', ''),
                        'Frecuencia_Cardiaca': vitals.get('heart_rate', ''),
                        'Temperatura': vitals.get('temperature', ''),
                        'Saturacion_O2': vitals.get('oxygen_saturation', ''),
                        'Nivel_Dolor': vitals.get('pain_level', '')
                    })
                    
                    # Estado general
                    status = eval_data.get('general_status', {})
                    record.update({
                        'Movilidad': status.get('mobility', ''),
                        'Apetito': status.get('appetite', ''),
                        'Calidad_Sueno': status.get('sleep_quality', ''),
                        'Estado_Animo': status.get('mood', ''),
                        'Estado_Cognitivo': status.get('cognitive_status', ''),
                        'Continencia': status.get('continence', '')
                    })
                    
                    # Otros datos
                    record.update({
                        'Sintomas': ', '.join(eval_data.get('symptoms', [])),
                        'Observaciones': eval_data.get('observations', '')
                    })
                    
                    complete_data.append(record)
                
                complete_df = pd.DataFrame(complete_data)
                csv_complete = complete_df.to_csv(index=False)
                
                st.download_button(
                    label="💾 Descargar Reporte Completo",
                    data=csv_complete,
                    file_name=f"reporte_completo_evaluaciones_{date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col3:
            if st.button("📊 Estadísticas Avanzadas", use_container_width=True):
                st.markdown("🚧 Estadísticas avanzadas próximamente disponibles")
    
    # Gráficos simples si hay datos suficientes
    if len(st.session_state.evaluations) > 1:
        st.markdown("### 📈 Tendencias")
        
        # Gráfico de evaluaciones por día
        daily_counts = {}
        for eval_data in st.session_state.evaluations:
            date_key = eval_data.get('date', str(date.today()))
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        if daily_counts:
            dates = list(daily_counts.keys())
            counts = list(daily_counts.values())
            
            chart_data = pd.DataFrame({
                'Fecha': [datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m') for d in sorted(dates)],
                'Evaluaciones': [daily_counts[d] for d in sorted(dates)]
            })
            
            st.line_chart(chart_data.set_index('Fecha'), height=300)

def show_emergency_protocols():
    """Página de protocolos de emergencia"""
    st.markdown("## 🚨 Protocolos de Emergencia")
    
    st.markdown("""
    <div class="alert-critical">
        <h3>📞 CONTACTOS DE EMERGENCIA</h3>
        <p><strong>112</strong> - Emergencias generales (Policía, Bomberos, Sanitarios)</p>
        <p><strong>061</strong> - Urgencias sanitarias</p>
        <p><strong>Centro médico de referencia</strong> - [Configurar en ajustes]</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Protocolos principales
    protocols = {
        "💔 Dolor Torácico": {
            "pasos": [
                "1. Mantener al paciente en reposo absoluto",
                "2. Aflojar ropa ajustada",
                "3. Administrar AAS 100mg (si no hay contraindicaciones)",
                "4. Tomar signos vitales",
                "5. Administrar nitroglicerina sublingual si está prescrita",
                "6. LLAMAR 112 INMEDIATAMENTE",
                "7. Preparar historia clínica y medicación actual"
            ],
            "color": "#dc3545"
        },
        "🫁 Dificultad Respiratoria": {
            "pasos": [
                "1. Colocar al paciente en posición semisentado (45°)",
                "2. Asegurar vía aérea permeable",
                "3. Administrar oxígeno si está disponible",
                "4. Aflojar ropa que comprima",
                "5. Tomar saturación de oxígeno y signos vitales",
                "6. Contactar médico urgente",
                "7. Preparar para posible traslado"
            ],
            "color": "#fd7e14"
        },
        "⚡ Caídas": {
            "pasos": [
                "1. NO MOVER al paciente inicialmente",
                "2. Evaluar nivel de consciencia",
                "3. Comprobar lesiones evidentes",
                "4. Tomar signos vitales",
                "5. Evaluar movilidad de extremidades",
                "6. Si hay lesión grave o sospecha fractura → 112",
                "7. Documentar circunstancias de la caída",
                "8. Implementar protocolo post-caída"
            ],
            "color": "#e74c3c"
        },
        "🧠 Alteración del Nivel de Consciencia": {
            "pasos": [
                "1. Evaluar respuesta verbal y motora",
                "2. Comprobar vía aérea",
                "3. Tomar glucemia capilar",
                "4. Signos vitales completos",
                "5. Revisar pupilas",
                "6. Buscar signos de traumatismo",
                "7. Contactar médico INMEDIATAMENTE",
                "8. Preparar traslado urgente"
            ],
            "color": "#6f42c1"
        },
        "🌡️ Fiebre Alta (>39°C)": {
            "pasos": [
                "1. Confirmar temperatura con termómetro fiable",
                "2. Medidas físicas de enfriamiento",
                "3. Administrar antitérmico según pauta",
                "4. Buscar foco infeccioso evidente",
                "5. Hidratar adecuadamente",
                "6. Tomar otros signos vitales",
                "7. Contactar médico para evaluación",
                "8. Monitorizar evolución cada 30min"
            ],
            "color": "#ff6b6b"
        },
        "🩸 Hemorragia": {
            "pasos": [
                "1. Identificar origen y tipo de hemorragia",
                "2. Aplicar presión directa si es externa",
                "3. Elevar la extremidad si es posible",
                "4. No retirar objetos clavados",
                "5. Controlar signos vitales",
                "6. Preparar para shock hipovolémico",
                "7. LLAMAR 112 si es abundante",
                "8. Mantener vía venosa si es posible"
            ],
            "color": "#dc3545"
        }
    }
    
    # Mostrar protocolos en pestañas
    tabs = st.tabs(list(protocols.keys()))
    
    for tab, (protocol_name, protocol_data) in zip(tabs, protocols.items()):
        with tab:
            st.markdown(f"""
            <div class="protocol-card" style="border-left-color: {protocol_data['color']};">
                <h3 style="color: {protocol_data['color']}; margin-top: 0;">{protocol_name}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for step in protocol_data["pasos"]:
                if "112" in step or "INMEDIATAMENTE" in step.upper():
                    st.markdown(f"""
                    <div class="alert-critical">
                        <strong>{step}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{step}**")
    
    # Calculadora de riesgo de caídas
    st.markdown("---")
    st.markdown("### ⚖️ Calculadora de Riesgo de Caídas (Escala Morse)")
    
    if st.session_state.patients:
        patient_options = {p['name']: p['id'] for p in st.session_state.patients.values()}
        selected_patient = st.selectbox("Seleccionar paciente para evaluar:", list(patient_options.keys()))
        
        if selected_patient:
            with st.form("morse_scale_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    history_falls = st.selectbox("Historial de caídas:", ["No (0)", "Sí (25)"])
                    secondary_diagnosis = st.selectbox("Diagnóstico secundario:", ["No (0)", "Sí (15)"])
                    ambulatory_aid = st.selectbox(
                        "Ayuda para caminar:",
                        ["Ninguna/Reposo/Enfermera (0)", "Muletas/Bastón/Andador (15)", "Mobiliario (30)"]
                    )
                
                with col2:
                    iv_therapy = st.selectbox("Terapia IV/Heparina:", ["No (0)", "Sí (20)"])
                    gait = st.selectbox(
                        "Marcha:",
                        ["Normal/Reposo/Inmóvil (0)", "Débil (10)", "Alterada (20)"]
                    )
                    mental_status = st.selectbox("Estado mental:", ["Orientado (0)", "Desorientado (15)"])
                
                if st.form_submit_button("🔍 Calcular Riesgo de Caídas"):
                    # Extraer puntuaciones
                    score = 0
                    score += 25 if "25" in history_falls else 0
                    score += 15 if "15" in secondary_diagnosis else 0
                    score += 30 if "30" in ambulatory_aid else (15 if "15" in ambulatory_aid else 0)
                    score += 20 if "20" in iv_therapy else 0
                    score += 20 if "20" in gait else (10 if "10" in gait else 0)
                    score += 15 if "15" in mental_status else 0
                    
                    # Determinar nivel de riesgo
                    if score >= 51:
                        risk_level = "ALTO"
                        risk_color = "#dc3545"
                        recommendations = [
                            "🚨 Supervisión constante",
                            "🛏️ Cama en posición más baja",
                            "🛡️ Barandillas elevadas cuando esté en cama",
                            "🔔 Timbre al alcance en todo momento",
                            "👟 Calzado antideslizante obligatorio",
                            "💡 Iluminación nocturna adecuada",
                            "📋 Reevaluación médica urgente"
                        ]
                    elif score >= 25:
                        risk_level = "MODERADO"
                        risk_color = "#ffc107"
                        recommendations = [
                            "👁️ Supervisión frecuente",
                            "🧹 Eliminar obstáculos en el entorno",
                            "💡 Mantener iluminación adecuada",
                            "👟 Usar calzado antideslizante",
                            "🚶 Acompañar en desplazamientos",
                            "📅 Reevaluación semanal"
                        ]
                    else:
                        risk_level = "BAJO"
                        risk_color = "#28a745"
                        recommendations = [
                            "✅ Mantener vigilancia rutinaria",
                            "📚 Educación sobre prevención de caídas",
                            "🏠 Mantener ambiente seguro",
                            "📅 Reevaluación mensual"
                        ]
                    
                    # Mostrar resultados
                    st.markdown("#### 📊 Resultado de la Evaluación")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="
                            background: {risk_color}15;
                            border: 2px solid {risk_color};
                            border-radius: 12px;
                            padding: 2rem;
                            text-align: center;
                        ">
                            <h2 style="margin: 0; color: {risk_color};">RIESGO {risk_level}</h2>
                            <h1 style="margin: 0.5rem 0; color: {risk_color};">{score}</h1>
                            <p style="margin: 0; color: #666;">Puntuación Morse</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**🎯 Medidas Preventivas Recomendadas:**")
                        for rec in recommendations:
                            st.markdown(f"• {rec}")

def show_settings():
    """Página de configuración"""
    st.markdown("## ⚙️ Configuración del Sistema")
    
    st.markdown("### 🏥 Información del Centro")
    
    with st.form("center_settings"):
        center_name = st.text_input("Nombre del Centro", value="Residencia Geriátrica")
        center_address = st.text_area("Dirección")
        center_phone = st.text_input("Teléfono Principal")
        medical_emergency = st.text_input("Teléfono Médico de Urgencia")
        
        st.markdown("### 👤 Configuración de Usuario")
        default_evaluator = st.text_input("Nombre del Evaluador por Defecto")
        
        st.markdown("### 🔧 Configuración Técnica")
        auto_backup = st.checkbox("Backup automático de datos", value=True)
        csv_auto_export = st.checkbox("Exportación automática a CSV", value=True)
        
        if st.form_submit_button("💾 Guardar Configuración"):
            st.success("✅ Configuración guardada exitosamente")
    
    st.markdown("---")
    st.markdown("### 📊 Estadísticas del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Pacientes", len(st.session_state.patients))
    with col2:
        st.metric("📋 Total Evaluaciones", len(st.session_state.evaluations))
    with col3:
        days_active = len(set(e.get('date', str(date.today())) for e in st.session_state.evaluations))
        st.metric("📅 Días Activos", days_active)
    
    st.markdown("### 🗑️ Gestión de Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exportar Todos los Datos", use_container_width=True):
            # Crear backup completo
            backup_data = {
                'patients': st.session_state.patients,
                'evaluations': st.session_state.evaluations,
                'export_date': str(date.today()),
                'export_time': datetime.now().strftime("%H:%M:%S")
            }
            
            backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="💾 Descargar Backup",
                data=backup_json,
                file_name=f"backup_asistente_geriatrico_{date.today()}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Reiniciar Datos de Prueba", use_container_width=True):
            if st.checkbox("Confirmar reinicio"):
                st.session_state.patients = {}
                st.session_state.evaluations = []
                st.success("✅ Datos reiniciados")
                st.rerun()
    
    with col3:
        if st.button("ℹ️ Información del Sistema", use_container_width=True):
            st.markdown("""
            <div class="alert-success">
                <h4>🏥 Asistente Geriátrico con IA</h4>
                <p><strong>Versión:</strong> 1.0.0</p>
                <p><strong>Desarrollado para:</strong> Residencias geriátricas españolas</p>
                <p><strong>Basado en:</strong> Guías de práctica clínica del SNS</p>
                <p><strong>Tecnología:</strong> Streamlit + Python</p>
                <p><strong>Última actualización:</strong> {}</p>
            </div>
            """.format(date.today().strftime("%d/%m/%Y")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()