# 🏥 GeriCare Assistant - Asistente Geriátrico con IA

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-412991?style=for-the-badge&logo=openai&logoColor=white)

Sistema integral de apoyo para cuidadores en residencias geriátricas, desarrollado con **Streamlit** y **ChatGPT API**, basado en **guías clínicas españolas**.

## ✨ Características Principales

### 🏥 Para Cuidadores
- ✅ **Evaluación integral** de pacientes con análisis IA
- ✅ **Alertas automáticas** de riesgo y deterioro
- ✅ **Recomendaciones clínicas** personalizadas
- ✅ **Protocolos de emergencia** integrados
- ✅ **Reportes CSV automáticos** de cada evaluación

### 📊 Para Administración
- ✅ **Dashboard centralizado** con métricas en tiempo real
- ✅ **Gestión de múltiples pacientes** 
- ✅ **Estadísticas de salud** y tendencias
- ✅ **Exportación de datos** completa
- ✅ **Cumplimiento normativo** español

### 🇪🇸 Basado en Normativa Española
- ✅ **Guías SNS** de práctica clínica geriátrica
- ✅ **Escalas validadas** (Morse, Downton, MMSE)
- ✅ **Criterios Beers** y STOPP/START
- ✅ **Protocolos residencias** según normativa

## 🚀 Demo en Vivo

[🌐 **Ver Demo Online**](https://tu-app.streamlit.app) *(próximamente)*

## 📱 Funcionalidades

| Módulo | Estado | Descripción |
|--------|--------|-------------|
| 📊 **Dashboard** | ✅ Completo | Métricas y visualización en tiempo real |
| 👤 **Pacientes** | ✅ Completo | Registro y gestión completa |
| 📋 **Evaluaciones** | ✅ Completo | Sistema de evaluación con IA |
| 🚨 **Protocolos** | ✅ Completo | Emergencias + Calculadora Morse |
| 📊 **Reportes** | ✅ Completo | Exportación CSV automática |
| 💊 **Medicamentos** | 🚧 En desarrollo | Control de medicación |
| 🏃‍♂️ **Fisioterapia** | 🚧 En desarrollo | Planes de ejercicio |

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- API Key de OpenAI
- Git

### Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/gericare-assistant.git
cd gericare-assistant

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API Key de OpenAI

# 5. Ejecutar aplicación
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 🔧 Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
OPENAI_API_KEY=tu-clave-api-aqui
CENTER_NAME=Tu Residencia
CENTER_PHONE=+34-XXX-XXX-XXX
```

### Estructura de Datos

Los reportes CSV se guardan automáticamente en:
```
data/reports/evaluaciones_diarias_YYYY-MM-DD.csv
```

## 📊 Campos del Reporte CSV

Cada evaluación genera un registro con **25+ campos**:

- 📅 Fecha y hora de evaluación
- 👤 Datos del paciente (ID, nombre, edad, habitación)
- 🩺 Signos vitales completos
- 📝 Estado general (movilidad, apetito, sueño, ánimo)
- 🔍 Síntomas y observaciones
- 🤖 Análisis IA con puntuación de severidad
- ⚠️ Alertas críticas y recomendaciones

## 🚨 Protocolos de Emergencia

El sistema incluye protocolos automatizados para:

- 💔 **Dolor torácico** - Protocolo SCA
- 🫁 **Dificultad respiratoria** - Oxigenoterapia urgente
- ⚡ **Caídas** - Evaluación post-caída
- 🧠 **Alteración consciencia** - Protocolo neurológico
- 🌡️ **Fiebre alta** - Búsqueda foco infeccioso
- 🩸 **Hemorragias** - Control de sangrado

## 📈 Análisis IA

El sistema analiza automáticamente:

- 🔴 **Signos vitales críticos** (PA, FC, Temp, SpO₂)
- ⚠️ **Factores de riesgo** específicos
- 📊 **Puntuación de severidad** (0-20)
- 💡 **Recomendaciones clínicas** personalizadas
- 🚨 **Alertas de urgencia** médica

## 🌐 Deploy en Streamlit Cloud

1. **Fork este repositorio**
2. **Conectar con Streamlit Cloud**
3. **Configurar variables de entorno**
4. **Deploy automático**

[![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tu-usuario/gericare-assistant/main/app.py)

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📋 Roadmap

### v1.1 - Próximo
- [ ] 💊 Sistema completo de medicamentos
- [ ] 🏃‍♂️ Módulo de fisioterapia
- [ ] 📧 Notificaciones por email
- [ ] 🌐 Multi-idioma (catalán, euskera, gallego)

### v1.2 - Futuro
- [ ] 📱 App móvil companion
- [ ] 🔗 Integración HIS/EMR
- [ ] 🤖 IA predictiva avanzada
- [ ] 📊 Analytics con ML

## 🛡️ Seguridad y Privacidad

- 🔒 **Datos médicos** no se almacenan permanentemente
- 🔑 **API Keys** gestionadas de forma segura
- 📋 **GDPR compliant** para protección de datos
- 🏥 **Diseñado para entornos sanitarios**

## 📞 Soporte

- 📧 **Issues:** [GitHub Issues](https://github.com/tu-usuario/gericare-assistant/issues)
- 📖 **Documentación:** [Wiki del proyecto](https://github.com/tu-usuario/gericare-assistant/wiki)
- 💬 **Comunidad:** [Discussions](https://github.com/tu-usuario/gericare-assistant/discussions)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## ⚠️ Disclaimer Médico

Este sistema es una **herramienta de apoyo** para cuidadores y NO reemplaza el criterio médico profesional. Siempre consulte con profesionales sanitarios para decisiones médicas importantes.

---

**Desarrollado con ❤️ para mejorar la calidad de vida de nuestros mayores**

*Basado en guías clínicas del Sistema Nacional de Salud de España*

## 🏆 Reconocimientos

- Guías clínicas del **Sistema Nacional de Salud**
- Escalas geriátricas **validadas científicamente**
- Comunidad **Streamlit** por la plataforma
- **OpenAI** por la tecnología de IA