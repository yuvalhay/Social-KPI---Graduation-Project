import streamlit as st

header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()

with header:
    st.title("The visualization of our KPI's")
    st.text("1: Loneliness KPI")
    st.text("2: Health KPI")
    st.text("3: Economic Strength KPI")

with kpi_selection:
    st.header("KPI Selection")
    loneliness_kpi_button = st.button("Loneliness")
    health_kpi_button = st.button("Health")
    economic_strength_kpi_button = st.button("Economic Strength")

with kpi_weights:
    st.header("KPI weights")
    if loneliness_kpi_button:
        pass
    elif health_kpi_button:
        pass
    elif economic_strength_kpi_button:
        pass
    else:
        st.text("In this section you will see all the weights that create the KPI you selected")
