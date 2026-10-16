"""
app.py - Interfaz en Streamlit.

Responsables: Equipo 4 (UI). Revisa: Equipo 3 (Métricas).

Formulario para configurar la simulación (genera el JSON del contrato de
entrada) y vistas de resultados (tablas y gráficas). Puede desarrollarse con
datos de ejemplo antes de conectar con engine.py y metrics.py.

Correr con:  streamlit run src/app.py
"""
import streamlit as st


def main() -> None:
    st.title("Simulación de sistemas de colas")
    st.info("Interfaz pendiente: Equipo 4 (Issues de UI).")


if __name__ == "__main__":
    main()
