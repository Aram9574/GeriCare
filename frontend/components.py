import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from typing import Dict, List, Any, Optional

def create_metric_card(title: str, value: str, status: str = "info", help_text: str = None):
    """
    Crea una tarjeta de métrica personalizada
    """
    colors = {
        "success": "#28a745",
        "danger": "#dc3545", 
        "warning": "#ffc107",
        "info": "#17a2b8"
    }
    
    color = colors.get(status, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}15, {color}05);
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h4 style="margin: 0; color: {color}; font-size: 0.9rem;">{title}</h4>
        <h2 style="margin: 0.5rem 0 0 0; color: #333;">{value}</h2>
    </div>
    """, unsafe_allow_html=True)

def create_patient_card(patient, show_actions: bool = True):
    """
    Crea una tarjeta de información del paciente
    """
    # Determinar color del riesgo
    risk_colors = {
        "Alto": "#dc3545",
        "Medio": "#ffc107", 
        "Bajo": "#28a745"
    }
    risk_color = risk_colors.get(patient.risk_level, "#6c757d")
    
    # Calcular días desde ingreso
    days_since_admission = (date.today() - patient.admission_date).days
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {risk_color};
    ">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3 style="margin: 0; color: #2c3e50;">{patient.name}</h3>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">
                    <strong>Edad:</strong> {patient.age} años | 
                    <strong>Habitación:</strong> {patient.room}
                </p>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">
                    <strong>Ingreso:</strong> {patient.admission_date.strftime('%d/%m/%Y')} 
                    ({days_since_admission} días)
                </p>
            </div>
            <div style="text-align: right;">
                <span style="
                    background: {risk_color};
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: bold;
                ">
                    Riesgo {patient.risk_level}
                </span>
                <p style="margin: 0.5rem 0; color: #7f8c8d; font-size: 0.8rem;">
                    <strong>Cognitivo:</strong> {patient.cognitive_level}
                </p>
            </div>
        </div>
        
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ecf0f1;">
            <p style="margin: 0; color: #5a6c7d; font-size: 0.9rem;">
                <strong>Condiciones:</strong> {patient.get_condition_summary()}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_vital_signs_chart(vital_signs_history: List[Dict]):
    """
    Crea gráficos de signos vitales
    """
    if not vital_signs_history:
        st.info("📊 No hay historial de signos vitales disponible")
        return
    
    # Preparar datos
    dates = [entry['date'] for entry in vital_signs_history]
    temps = [entry.get('temperature', 36.5) for entry in vital_signs_history]
    hrs = [entry.get('heart_rate', 70) for entry in vital_signs_history]
    spo2s = [entry.get('oxygen_saturation', 98) for entry in vital_signs_history]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌡️ Temperatura")
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=dates, y=temps,
            mode='lines+markers',
            name='Temperatura',
            line=dict(color='#e74c3c', width=2),
            marker=dict(size=6)
        ))
        fig_temp.add_hline(y=37.5, line_dash="dash", line_color="orange", 
                          annotation_text="Límite superior normal")
        fig_temp.update_layout(
            yaxis_title="Temperatura (°C)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        st.markdown("#### 💗 Frecuencia Cardíaca")
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Scatter(
            x=dates, y=hrs,
            mode='lines+markers',
            name='FC',
            line=dict(color='#e91e63', width=2),
            marker=dict(size=6)
        ))
        fig_hr.add_hline(y=100, line_dash="dash", line_color="orange",
                        annotation_text="Taquicardia")
        fig_hr.add_hline(y=60, line_dash="dash", line_color="blue",
                        annotation_text="Bradicardia")
        fig_hr.update_layout(
            yaxis_title="Frecuencia (lpm)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    with col2:
        st.markdown("#### 🫁 Saturación de Oxígeno")
        fig_spo2 = go.Figure()
        fig_spo2.add_trace(go.Scatter(
            x=dates, y=spo2s,
            mode='lines+markers',
            name='SpO2',
            line=dict(color='#3498db', width=2),
            marker=dict(size=6)
        ))
        fig_spo2.add_hline(y=95, line_dash="dash", line_color="orange",
                          annotation_text="Límite inferior normal")
        fig_spo2.update_layout(
            yaxis_title="Saturación (%)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_spo2, use_container_width=True)

def create_alert_banner(message: str, alert_type: str = "info"):
    """
    Crea un banner de alerta personalizado
    """
    colors = {
        "success": {"bg": "#d4edda", "border": "#28a745", "text": "#155724", "icon": "✅"},
        "warning": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404", "icon": "⚠️"},
        "danger": {"bg": "#f8d7da", "border": "#dc3545", "text": "#721c24", "icon": "🚨"},
        "info": {"bg": "#d1ecf1", "border": "#17a2b8", "text": "#0c5460", "icon": "ℹ️"}
    }
    
    style = colors.get(alert_type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background-color: {style['bg']};
        border: 1px solid {style['border']};
        border-left: 4px solid {style['border']};
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: {style['text']};
        font-weight: 500;
    ">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{style['icon']}</span>
        {message}
    </div>
    """, unsafe_allow_html=True)

def create_assessment_timeline(assessments: List[Dict]):
    """
    Crea una línea de tiempo de evaluaciones
    """
    if not assessments:
        st.info("📋 No hay evaluaciones registradas")
        return
    
    st.markdown("### 📅 Línea de Tiempo de Evaluaciones")
    
    for i, assessment in enumerate(assessments[-5:]):  # Últimas 5 evaluaciones
        severity = assessment.get('severity_level', 'Bajo')
        date_str = assessment.get('date', '')
        time_str = assessment.get('time', '')
        
        # Color según severidad
        severity_colors = {
            "Crítico": "#dc3545",
            "Alto": "#fd7e14", 
            "Moderado": "#ffc107",
            "Bajo": "#28a745"
        }
        color = severity_colors.get(severity, "#6c757d")
        
        # Ícono según severidad
        severity_icons = {
            "Crítico": "🚨",
            "Alto": "⚠️",
            "Moderado": "⚡",
            "Bajo": "✅"
        }
        icon = severity_icons.get(severity, "📋")
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: white;
            border-radius: 8px;
            border-left: 4px solid {color};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="
                background: {color};
                color: white;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                font-size: 1.2rem;
            ">
                {icon}
            </div>
            <div style="flex-grow: 1;">
                <div style="font-weight: bold; color: #2c3e50;">
                    {date_str} - {time_str}
                </div>
                <div style="color: {color}; font-weight: 500;">
                    Severidad: {severity}
                </div>
                <div style="color: #7f8c8d; font-size: 0.9rem;">
                    {assessment.get('ai_analysis', '')[:100]}...
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_medication_list(medications: List[Dict]):
    """
    Crea una lista visual de medicamentos
    """
    if not medications:
        st.info("💊 No hay medicamentos registrados")
        return
    
    st.markdown("### 💊 Medicamentos Activos")
    
    for med in medications:
        if med.get('active', True):
            st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 0.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            ">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">{med.get('name', 'N/A')}</h4>
                        <p style="margin: 0.25rem 0; color: #7f8c8d;">
                            <strong>Dosis:</strong> {med.get('dosage', 'N/A')} | 
                            <strong>Frecuencia:</strong> {med.get('frequency', 'N/A')}
                        </p>
                        <p style="margin: 0.25rem 0; color: #7f8c8d;">
                            <strong>Indicación:</strong> {med.get('indication', 'N/A')}
                        </p>
                    </div>
                    <div style="
                        background: #28a745;
                        color: white;
                        padding: 0.25rem 0.5rem;
                        border-radius: 4px;
                        font-size: 0.8rem;
                    ">
                        Activo
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_risk_assessment_radar(risk_factors: Dict[str, int]):
    """
    Crea un gráfico de radar para evaluación de riesgo
    """
    if not risk_factors:
        st.info("📊 No hay datos de factores de riesgo disponibles")
        return
    
    categories = list(risk_factors.keys())
    values = list(risk_factors.values())
    
    # Crear gráfico de radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Factores de Riesgo',
        line=dict(color='#e74c3c'),
        fillcolor='rgba(231, 76, 60, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        title="Evaluación de Factores de Riesgo",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_progress_bar(value: float, max_value: float = 100, 
                       color: str = "#17a2b8", label: str = ""):
    """
    Crea una barra de progreso personalizada
    """
    percentage = min((value / max_value) * 100, 100)
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        {f'<label style="font-weight: 500; color: #2c3e50;">{label}</label>' if label else ''}
        <div style="
            background-color: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin-top: 0.5rem;
        ">
            <div style="
                background-color: {color};
                height: 100%;
                width: {percentage}%;
                border-radius: 10px;
                transition: width 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 0.8rem;
                font-weight: bold;
            ">
                {percentage:.1f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_stats_summary(stats: Dict[str, Any]):
    """
    Crea un resumen estadístico visual
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "📊 Total Evaluaciones", 
            str(stats.get('total_evaluations', 0)),
            "info"
        )
    
    with col2:
        create_metric_card(
            "⚠️ Casos Urgentes", 
            str(stats.get('urgent_cases', 0)),
            "danger" if stats.get('urgent_cases', 0) > 0 else "success"
        )
    
    with col3:
        avg_temp = stats.get('avg_vitals', {}).get('temperature', 0)
        create_metric_card(
            "🌡️ Temperatura Media", 
            f"{avg_temp:.1f}°C",
            "warning" if avg_temp > 37.5 else "success"
        )
    
    with col4:
        avg_hr = stats.get('avg_vitals', {}).get('heart_rate', 0)
        create_metric_card(
            "💗 FC Media", 
            f"{avg_hr:.0f} lpm",
            "info"
        )

def create_emergency_protocols_panel():
    """
    Panel de protocolos de emergencia de acceso rápido
    """
    st.markdown("### 🚨 Protocolos de Emergencia")
    
    emergency_protocols = {
        "Caída": {
            "icon": "⚡",
            "color": "#dc3545",
            "actions": [
                "1. No mover al paciente",
                "2. Evaluar consciencia y lesiones",
                "3. Comprobar signos vitales",
                "4. Si hay lesión grave → 112"
            ]
        },
        "Dificultad Respiratoria": {
            "icon": "🫁",
            "color": "#fd7e14",
            "actions": [
                "1. Posición semisentado",
                "2. Oxígeno si disponible",
                "3. Comprobar vías respiratorias",
                "4. Contactar médico urgente"
            ]
        },
        "Dolor Torácico": {
            "icon": "💔",
            "color": "#e74c3c",
            "actions": [
                "1. Reposo absoluto",
                "2. AAS 100mg si no alergia",
                "3. Nitroglicerina sublingual",
                "4. Llamar 112 inmediatamente"
            ]
        },
        "Confusión Aguda": {
            "icon": "🧠",
            "color": "#6f42c1",
            "actions": [
                "1. Ambiente tranquilo",
                "2. Evaluar causas reversibles",
                "3. Revisar medicación",
                "4. Contactar médico"
            ]
        }
    }
    
    cols = st.columns(2)
    for i, (protocol, data) in enumerate(emergency_protocols.items()):
        with cols[i % 2]:
            with st.expander(f"{data['icon']} {protocol}", expanded=False):
                for action in data['actions']:
                    st.markdown(f"**{action}**")

def create_fall_risk_calculator():
    """
    Calculadora interactiva de riesgo de caídas
    """
    st.markdown("### ⚠️ Calculadora de Riesgo de Caídas (Escala Morse)")
    
    with st.form("fall_risk_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            history_falls = st.selectbox(
                "Historial de caídas:",
                ["No", "Sí"],
                help="¿Ha tenido caídas en los últimos 3 meses?"
            )
            
            secondary_diagnosis = st.selectbox(
                "Diagnóstico secundario:",
                ["No", "Sí"],
                help="¿Tiene más de un diagnóstico médico?"
            )
            
            ambulatory_aid = st.selectbox(
                "Ayuda para caminar:",
                ["Ninguna/Cama/Silla/Enfermera", "Muletas/Bastón/Andador", "Mobiliario"],
                help="¿Qué ayuda necesita para movilizarse?"
            )
        
        with col2:
            iv_therapy = st.selectbox(
                "Terapia IV:",
                ["No", "Sí"],
                help="¿Tiene vía intravenosa o dispositivos?"
            )
            
            gait = st.selectbox(
                "Marcha:",
                ["Normal/Cama/Inmóvil", "Débil", "Alterada"],
                help="¿Cómo es su patrón de marcha?"
            )
            
            mental_status = st.selectbox(
                "Estado mental:",
                ["Orientado", "Desorientado"],
                help="¿Está orientado en tiempo, espacio y persona?"
            )
        
        submitted = st.form_submit_button("🔍 Calcular Riesgo", use_container_width=True)
        
        if submitted:
            # Cálculo según escala Morse
            score = 0
            
            # Historial de caídas
            if history_falls == "Sí":
                score += 25
            
            # Diagnóstico secundario
            if secondary_diagnosis == "Sí":
                score += 15
            
            # Ayuda ambulatoria
            if ambulatory_aid == "Muletas/Bastón/Andador":
                score += 15
            elif ambulatory_aid == "Mobiliario":
                score += 30
            
            # Terapia IV
            if iv_therapy == "Sí":
                score += 20
            
            # Marcha
            if gait == "Débil":
                score += 10
            elif gait == "Alterada":
                score += 20
            
            # Estado mental
            if mental_status == "Desorientado":
                score += 15
            
            # Interpretación
            if score >= 51:
                risk_level = "ALTO"
                risk_color = "#dc3545"
                recommendations = [
                    "Supervisión constante",
                    "Cama en posición más baja",
                    "Barandillas elevadas",
                    "Evaluación médica urgente"
                ]
            elif score >= 25:
                risk_level = "MODERADO"
                risk_color = "#ffc107"
                recommendations = [
                    "Supervisión frecuente",
                    "Eliminar obstáculos",
                    "Iluminación adecuada",
                    "Calzado antideslizante"
                ]
            else:
                risk_level = "BAJO"
                risk_color = "#28a745"
                recommendations = [
                    "Mantener vigilancia rutinaria",
                    "Educación sobre prevención",
                    "Ambiente seguro"
                ]
            
            # Mostrar resultados
            st.markdown("---")
            st.markdown("#### 📊 Resultado de la Evaluación")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: {risk_color}15;
                    border: 2px solid {risk_color};
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <h2 style="margin: 0; color: {risk_color};">RIESGO {risk_level}</h2>
                    <h3 style="margin: 0.5rem 0 0 0; color: {risk_color};">Puntuación: {score}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**🎯 Recomendaciones:**")
                for rec in recommendations:
                    st.markdown(f"• {rec}")

def create_medication_interaction_checker():
    """
    Verificador de interacciones medicamentosas
    """
    st.markdown("### 💊 Verificador de Interacciones")
    
    # Medicamentos comunes en geriatría
    common_geriatric_meds = [
        "Amlodipino", "Atorvastatina", "Enalapril", "Furosemida", "Metformina",
        "Omeprazol", "Paracetamol", "Simvastatina", "Losartán", "Metoprolol",
        "Warfarina", "Digoxina", "Donepezilo", "Lorazepam", "Tramadol"
    ]
    
    selected_meds = st.multiselect(
        "Seleccione los medicamentos actuales:",
        options=common_geriatric_meds,
        help="Seleccione todos los medicamentos que toma el paciente"
    )
    
    if len(selected_meds) >= 2:
        st.markdown("#### ⚠️ Posibles Interacciones Detectadas:")
        
        # Interacciones conocidas (simplificado para demo)
        known_interactions = {
            ("Warfarina", "Omeprazol"): {
                "severity": "Moderada",
                "effect": "Aumento del efecto anticoagulante",
                "action": "Monitorizar INR más frecuentemente"
            },
            ("Enalapril", "Furosemida"): {
                "severity": "Leve",
                "effect": "Posible hipotensión",
                "action": "Controlar presión arterial"
            },
            ("Digoxina", "Furosemida"): {
                "severity": "Grave",
                "effect": "Toxicidad digitálica por hipopotasemia",
                "action": "Monitorizar potasio y niveles de digoxina"
            }
        }
        
        interactions_found = False
        for (med1, med2), interaction in known_interactions.items():
            if med1 in selected_meds and med2 in selected_meds:
                interactions_found = True
                severity_color = {
                    "Leve": "#28a745",
                    "Moderada": "#ffc107", 
                    "Grave": "#dc3545"
                }[interaction["severity"]]
                
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {severity_color};
                    background: {severity_color}15;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-radius: 4px;
                ">
                    <strong>{med1} + {med2}</strong><br>
                    <span style="color: {severity_color}; font-weight: bold;">
                        Severidad: {interaction["severity"]}
                    </span><br>
                    <strong>Efecto:</strong> {interaction["effect"]}<br>
                    <strong>Acción:</strong> {interaction["action"]}
                </div>
                """, unsafe_allow_html=True)
        
        if not interactions_found:
            st.success("✅ No se detectaron interacciones conocidas entre los medicamentos seleccionados")
    
    elif len(selected_meds) == 1:
        st.info("ℹ️ Seleccione al menos 2 medicamentos para verificar interacciones")

def create_daily_schedule_widget(patient_id: Optional[int] = None):
    """
    Widget de horario diario para cuidados
    """
    st.markdown("### 📅 Horario de Cuidados Diario")
    
    # Horarios típicos de cuidados geriátricos
    daily_schedule = {
        "07:00": "Despertar - Signos vitales matutinos",
        "08:00": "Desayuno - Medicación matutina",
        "09:30": "Higiene personal y vestido",
        "11:00": "Actividades terapéuticas",
        "12:30": "Almuerzo - Medicación mediodía",
        "14:00": "Siesta / Descanso",
        "16:00": "Merienda - Control de signos vitales",
        "17:30": "Actividad física suave",
        "19:00": "Cena - Medicación vespertina",
        "21:00": "Actividades tranquilas",
        "22:00": "Preparación para dormir",
        "22:30": "Medicación nocturna"
    }
    
    current_hour = datetime.now().hour
    
    for time, activity in daily_schedule.items():
        hour = int(time.split(':')[0])
        
        # Resaltar la actividad actual
        if hour == current_hour:
            st.markdown(f"""
            <div style="
                background: #007bff15;
                border: 2px solid #007bff;
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.25rem 0;
            ">
                <strong>🔵 {time}</strong> - {activity}
            </div>
            """, unsafe_allow_html=True)
        elif hour < current_hour:
            st.markdown(f"""
            <div style="
                background: #28a74515;
                border-left: 3px solid #28a745;
                padding: 0.5rem 0.75rem;
                margin: 0.25rem 0;
                color: #666;
            ">
                ✅ {time} - {activity}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                border-left: 3px solid #dee2e6;
                padding: 0.5rem 0.75rem;
                margin: 0.25rem 0;
            ">
                ⏰ {time} - {activity}
            </div>
            """, unsafe_allow_html=True)

def create_export_buttons(patient_id: Optional[int] = None):
    """
    Botones para exportar diferentes tipos de reportes
    """
    st.markdown("### 📋 Exportar Reportes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Reporte Diario", use_container_width=True):
            st.info("🔄 Generando reporte diario...")
            # Aquí iría la lógica de exportación
            st.success("✅ Reporte diario generado")
    
    with col2:
        if st.button("📈 Resumen Semanal", use_container_width=True):
            st.info("🔄 Generando resumen semanal...")
            st.success("✅ Resumen semanal generado")
    
    with col3:
        if st.button("📁 Historial Paciente", use_container_width=True):
            if patient_id:
                st.info(f"🔄 Exportando historial del paciente {patient_id}...")
                st.success("✅ Historial exportado")
            else:
                st.warning("⚠️ Seleccione un paciente primero")

def create_quick_actions_sidebar():
    """
    Panel de acciones rápidas en la barra lateral
    """
    st.sidebar.markdown("### ⚡ Acciones Rápidas")
    
    if st.sidebar.button("🚨 Emergencia", use_container_width=True):
        st.sidebar.error("🚨 Modo emergencia activado")
        st.sidebar.markdown("**Contactar:**")
        st.sidebar.markdown("• 📞 **112** - Emergencias")
        st.sidebar.markdown("• 📞 **061** - Urgencias Sanitarias")
        st.sidebar.markdown("• 🏥 **Centro Médico**")
    
    if st.sidebar.button("📋 Nueva Evaluación", use_container_width=True):
        st.sidebar.success("Redirigiendo a nueva evaluación...")
    
    if st.sidebar.button("💊 Medicamentos", use_container_width=True):
        st.sidebar.info("Abriendo gestión de medicamentos...")
    
    if st.sidebar.button("📊 Reportes", use_container_width=True):
        st.sidebar.info("Generando reportes...")