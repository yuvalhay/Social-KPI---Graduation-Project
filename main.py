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
    firstKPI, secondKPI, thirdKPI, clear = st.columns([0.5, 0.4, 1, 1])
    with firstKPI:
        loneliness_kpi_button = st.button("Loneliness")

    with secondKPI:
        health_kpi_button = st.button("Health")

    with thirdKPI:
        economic_strength_kpi_button = st.button("Economic Strength")

    with clear:
        clear_button = st.button("Clear")

with kpi_weights:
    st.header("KPI weights")
    if loneliness_kpi_button:
        arnona_cat = st.slider("arnona_cat", 0.0, 1.0, 0.15)
        # loneliness_weights = [["arnona_cat", 0.15], ["members_Water", 0.15], ["martial", 0.15], ["widow_grown", 0.04],
        #                       ["widow_elderlies", 0.1], ["lonely_elderlies", 0.3], ["p85_plus", 0.06],
        #                       ["accumulated_cases", 0.05]]

    elif health_kpi_button:
        pass
    elif economic_strength_kpi_button:
        pass
    elif clear_button:
        st.text("In this section you will see all the weights that create the KPI you selected")
