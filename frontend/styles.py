import streamlit as st

def apply_custom_css():
    """
    Aplica estilos CSS personalizados para el tema médico/geriátrico
    """
    st.markdown("""
    <style>
    /* Variables CSS para colores del tema médico */
    :root {
        --primary-color: #2E8B57; /* Verde médico */
        --secondary-color: #4682B4; /* Azul médico */
        --accent-color: #20B2AA; /* Turquesa */
        --warning-color: #FF6347; /* Rojo coral para alertas */
        --success-color: #32CD32; /* Verde lima */
        --info-color: #87CEEB; /* Azul cielo */
        --light-bg: #F0F8FF; /* Azul muy claro */
        --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --border-radius: 12px;
    }
    
    /* Estilos generales de la aplicación */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem 1rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Sidebar personalizada */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* Métricas personalizadas */
    .metric-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        border-left: 4px solid var(--primary-color);
        margin: 0.5rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-title {
        color: var(--primary-color);
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Tarjetas de pacientes */
    .patient-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border-left: 4px solid var(--secondary-color);
        transition: all 0.3s ease;
    }
    
    .patient-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .patient-name {
        color: var(--primary-color);
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .patient-info {
        color: #7f8c8d;
        margin: 0.25rem 0;
        display: flex;
        align-items: center;
    }
    
    .risk-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        text-align: center;
        color: white;
    }
    
    .risk-alto { background-color: #e74c3c; }
    .risk-medio { background-color: #f39c12; }
    .risk-bajo { background-color: #27ae60; }
    
    /* Formularios */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        border: 1px solid #e9ecef;
    }
    
    .stForm > div {
        margin-bottom: 1rem;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: var(--card-shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(46, 139, 87, 0.4);
        background: linear-gradient(135deg, #228B22, #4682B4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Botones de emergencia */
    .emergency-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
        100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
    }
    
    /* Alertas y notificaciones */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: var(--card-shadow);
    }
    
    .alert-success {
        background-color: #d4edda;
        border-left-color: var(--success-color);
        color: #155724;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border-left-color: var(--warning-color);
        color: #721c24;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border-left-color: var(--info-color);
        color: #0c5460;
    }
    
    /* Línea de tiempo */
    .timeline-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        border-left: 4px solid var(--primary-color);
        transition: all 0.3s ease;
    }
    
    .timeline-item:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .timeline-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 1rem;
        color: white;
        background: var(--primary-color);
    }
    
    .timeline-content {
        flex-grow: 1;
    }
    
    .timeline-date {
        font-weight: bold;
        color: var(--primary-color);
        margin-bottom: 0.25rem;
    }
    
    .timeline-description {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Gráficos y charts */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
    }
    
    .chart-title {
        color: var(--primary-color);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Medicamentos */
    .medication-item {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .medication-name {
        font-weight: bold;
        color: var(--primary-color);
        font-size: 1.1rem;
    }
    
    .medication-details {
        color: #7f8c8d;
        margin: 0.25rem 0;
        font-size: 0.9rem;
    }
    
    .medication-status {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-active {
        background: var(--success-color);
        color: white;
    }
    
    .status-inactive {
        background: #6c757d;
        color: white;
    }
    
    /* Tablas responsivas */
    .dataframe {
        background: white;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--card-shadow);
    }
    
    .dataframe th {
        background: var(--primary-color);
        color: white;
        font-weight: 600;
        padding: 1rem;
        text-align: left;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .dataframe tr:hover {
        background-color: #e3f2fd;
    }
    
    /* Progress bars */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .progress-success { background: linear-gradient(90deg, #27ae60, #2ecc71); }
    .progress-warning { background: linear-gradient(90deg, #f39c12, #e67e22); }
    .progress-danger { background: linear-gradient(90deg, #e74c3c, #c0392b); }
    .progress-info { background: linear-gradient(90deg, #3498db, #2980b9); }
    
    /* Horario diario */
    .schedule-item {
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: var(--border-radius);
        transition: all 0.3s ease;
    }
    
    .schedule-current {
        background: rgba(0, 123, 255, 0.1);
        border: 2px solid #007bff;
        color: #007bff;
        font-weight: bold;
    }
    
    .schedule-completed {
        background: rgba(40, 167, 69, 0.1);
        border-left: 3px solid #28a745;
        color: #666;
    }
    
    .schedule-pending {
        background: #f8f9fa;
        border-left: 3px solid #dee2e6;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .patient-card {
            padding: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .timeline-item {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .timeline-icon {
            margin-right: 0;
            margin-bottom: 0.5rem;
        }
    }
    
    /* Animaciones */
    @keyframes slideInUp {
        from {
            transform: translate3d(0, 40px, 0);
            opacity: 0;
        }
        to {
            transform: translate3d(0, 0, 0);
            opacity: 1;
        }
    }
    
    .slide-in-up {
        animation: slideInUp 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Indicadores de severidad */
    .severity-critical {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        animation: pulse 1.5s infinite;
    }
    
    .severity-high {
        background: linear-gradient(135deg, #fd7e14, #e55910);
        color: white;
    }
    
    .severity-moderate {
        background: linear-gradient(135deg, #ffc107, #e0a800);
        color: #212529;
    }
    
    .severity-low {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }
    
    /* Efectos especiales para emergencias */
    .emergency-mode {
        animation: emergency-flash 2s infinite;
    }
    
    @keyframes emergency-flash {
        0%, 50%, 100% { background-color: transparent; }
        25%, 75% { background-color: rgba(220, 53, 69, 0.1); }
    }
    
    /* Tooltips personalizados */
    .custom-tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .custom-tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 1000;
        opacity: 0;
        animation: fadeIn 0.3s ease-in forwards;
    }
    
    /* Estilos para el calculador de riesgo de caídas */
    .fall-risk-calculator {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--card-shadow);
        border: 1px solid #e9ecef;
    }
    
    .risk-result {
        text-align: center;
        padding: 2rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    .risk-score {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    
    .risk-level {
        font-size: 1.5rem;
        margin: 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Protocolos de emergencia */
    .emergency-protocol {
        background: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: var(--card-shadow);
        border-left: 4px solid #dc3545;
    }
    
    .emergency-protocol h4 {
        color: #dc3545;
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
    }
    
    .emergency-protocol ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .emergency-protocol li {
        margin: 0.25rem 0;
        font-weight: 500;
    }
    
    /* Medication checker */
    .interaction-warning {
        border-left: 4px solid #ffc107;
        background: rgba(255, 193, 7, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .interaction-danger {
        border-left: 4px solid #dc3545;
        background: rgba(220, 53, 69, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .interaction-info {
        border-left: 4px solid #17a2b8;
        background: rgba(23, 162, 184, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    /* Accesibilidad mejorada */
    .high-contrast {
        filter: contrast(1.5);
    }
    
    .large-text {
        font-size: 1.2em;
        line-height: 1.6;
    }
    
    /* Estados de carga */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(46, 139, 87, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Estilos para selectores y inputs */
    .stSelectbox > div > div {
        border-radius: var(--border-radius);
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: var(--border-radius);
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
    }
    
    /* Número input especial */
    .stNumberInput > div > div > input {
        border-radius: var(--border-radius);
        border: 2px solid #e9ecef;
        font-weight: 600;
        text-align: center;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--secondary-color);
        box-shadow: 0 0 0 2px rgba(70, 130, 180, 0.2);
    }
    
    /* Slider personalizado */
    .stSlider > div > div > div {
        color: var(--primary-color);
    }
    
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    /* Checkbox y radio personalizado */
    .stCheckbox > label {
        color: var(--primary-color);
        font-weight: 500;
    }
    
    .stRadio > label {
        color: var(--primary-color);
        font-weight: 500;
    }
    
    /* Multiselect personalizado */
    .stMultiSelect > div {
        border-radius: var(--border-radius);
    }
    
    /* Date input personalizado */
    .stDateInput > div > div > input {
        border-radius: var(--border-radius);
        border: 2px solid #e9ecef;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(32, 178, 170, 0.2);
    }
    
    /* Time input personalizado */
    .stTimeInput > div > div > input {
        border-radius: var(--border-radius);
        border: 2px solid #e9ecef;
    }
    
    .stTimeInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(32, 178, 170, 0.2);
    }
    
    /* Footer personalizado */
    .main-footer {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-radius: var(--border-radius);
    }
    
    /* Mensaje de bienvenida */
    .welcome-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 2rem 0;
        box-shadow: var(--card-shadow);
    }
    
    .welcome-message h2 {
        margin: 0 0 1rem 0;
        font-size: 2rem;
    }
    
    .welcome-message p {
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Personalizar la barra superior */
    .stApp > header {
        background: transparent;
    }
    
    /* Estilos específicos para el modo oscuro (opcional) */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #4CAF50;
            --secondary-color: #2196F3;
            --accent-color: #00BCD4;
        }
        
        .main {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        }
        
        .patient-card, .metric-card, .chart-container {
            background: #2d2d2d;
            color: white;
        }
    }
    </style>
    """, unsafe_allow_html=True)