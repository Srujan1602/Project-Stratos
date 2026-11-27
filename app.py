import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="STRATOS | Global Control Center",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. GLOBAL UI STYLING
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #070d19;
    --panel: #101d31;
    --panel2: #142640;
    --border: #203d5c;
    --cyan: #42dcff;
    --blue: #168fc4;
    --text: #eaf4ff;
    --muted: #91a9c3;
    --green: #39e6a5;
}

.stApp {
    background:
        radial-gradient(circle at 85% 0%, #142b49 0%, transparent 35%),
        linear-gradient(135deg, #070d19, #091426 55%, #060b15);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* MAIN CONTENT */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091629, #050a14);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] h1 {
    color: var(--cyan) !important;
    letter-spacing: 2px;
    font-weight: 800;
}

[data-testid="stSidebar"] h3 {
    color: #d7eaff !important;
}

[data-testid="stSidebar"] p {
    color: var(--muted);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #c3d6eb !important;
    font-size: 14px;
}

/* HEADINGS */

h1 {
    color: #f1f7ff !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2, h3, h4 {
    color: #dceeff !important;
    font-weight: 700 !important;
}

p, label {
    color: var(--muted);
}

/* METRIC CARDS */

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #142a45, #0c192b);
    border: 1px solid #254a6c;
    border-radius: 15px;
    padding: 18px 20px;
    min-height: 115px;
    box-shadow: 0 5px 22px rgba(0, 180, 255, 0.05);
    transition: 0.2s ease;
}

div[data-testid="metric-container"]:hover {
    border-color: var(--cyan);
    box-shadow: 0 5px 24px rgba(50, 210, 255, 0.10);
}

div[data-testid="metric-container"] label {
    color: #9db5cf !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
}

div[data-testid="stMetricValue"] {
    color: var(--cyan) !important;
    font-size: 29px !important;
    font-weight: 800 !important;
}

/* BUTTONS */

.stButton button {
    background: linear-gradient(90deg, #087cae, #13a9d1);
    color: white;
    border: 1px solid #25bce8;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
    transition: 0.2s ease;
}

.stButton button:hover {
    background: linear-gradient(90deg, #079bd3, #37d9ff);
    color: white;
    border-color: #69e8ff;
    box-shadow: 0 0 18px rgba(54, 217, 255, 0.2);
}

/* INPUTS */

.stSelectbox div[data-baseweb="select"],
.stNumberInput input,
.stTextInput input {
    background-color: #101f34;
    color: white;
    border-radius: 8px;
}

.stSlider [data-baseweb="slider"] {
    color: var(--cyan);
}

/* DATA TABLES */

[data-testid="stDataFrame"] {
    border: 1px solid #244663;
    border-radius: 12px;
    overflow: hidden;
}

/* TABS AND EXPANDERS */

[data-testid="stExpander"] {
    background: rgba(15, 31, 51, 0.8);
    border: 1px solid var(--border);
    border-radius: 12px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* DIVIDERS */

hr {
    border-color: #203b58;
}

/* CUSTOM COMPONENTS */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 17px;
    background: rgba(13, 29, 49, 0.88);
    border: 1px solid #244765;
    border-radius: 12px;
    margin-bottom: 22px;
}

.brand {
    color: #42dcff;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
}

.brand-sub {
    color: #829bb8;
    font-size: 11px;
    letter-spacing: 1px;
}

.status {
    color: #39e6a5;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.section-heading {
    color: #43dfff;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 22px;
    margin-bottom: 12px;
}

.hero-panel {
    background: linear-gradient(120deg, #142e4d, #0c192c);
    border: 1px solid #285477;
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 27px;
    color: #f1f8ff;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.hero-subtitle {
    color: #9fb8d3;
    font-size: 13px;
    margin-top: 7px;
    line-height: 1.7;
}

.panel {
    background: linear-gradient(145deg, #132741, #0c192b);
    border: 1px solid #244663;
    border-radius: 14px;
    padding: 17px;
}

.footer {
    text-align: center;
    color: #718ba7;
    padding: 25px;
    font-size: 11px;
    letter-spacing: 1px;
    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. SIDEBAR NAVIGATION
# ==================================================

st.sidebar.markdown("# ☁ STRATOS")
st.sidebar.caption("AUTONOMOUS GLOBAL CLOUD FABRIC")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Global Overview",
        "Cloud Regions",
        "Workload Forecasting",
        "Anomaly Detection",
        "Intelligent Placement",
        "Simulation Analytics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### SYSTEM STATUS")

st.sidebar.markdown(
    "<span style='color:#39e6a5;font-weight:800;'>● SIMULATION ONLINE</span>",
    unsafe_allow_html=True
)

st.sidebar.caption(
    "Research prototype | Synthetic telemetry and simulated infrastructure"
)

st.sidebar.markdown("---")

st.sidebar.caption("STRATOS RESEARCH PLATFORM")
st.sidebar.caption("Version 1.0 | Academic Prototype")


# ==================================================
# 4. GLOBAL STATUS BAR
# ==================================================

st.markdown("""
<div class="topbar">
    <div>
        <span class="brand">STRATOS</span>
        <span class="brand-sub"> / GLOBAL CONTROL CENTER</span>
    </div>
    <div class="status">● SIMULATION ENVIRONMENT</div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# 5. SIMULATED CLOUD REGION DATA
# ==================================================

regions = pd.DataFrame({

    "Region": ["Region A", "Region B", "Region C"],

    "CPU Cores": [120, 90, 150],

    "Memory (GB)": [120, 96, 140],

    "Cost ($/hr)": [0.08, 0.06, 0.12],

    "Latency (ms)": [25, 45, 15],

    "CPU Usage (%)": [58, 72, 41],

    "Memory Usage (%)": [64, 55, 48]

})


# ==================================================
# 6. GLOBAL OVERVIEW
# ==================================================

if page == "Global Overview":

    st.markdown("""
    <div class="hero-panel">
        <div class="hero-title">☁ PROJECT STRATOS</div>
        <div class="hero-subtitle">
            AI-Driven Workload Placement via Telemetry Forecasting
            and Dynamic Anomaly Mitigation
            <br>
            Intelligent resource management across a simulated
            multi-region cloud infrastructure.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='section-heading'>GLOBAL INFRASTRUCTURE OVERVIEW</div>",
        unsafe_allow_html=True
    )

    # KPI CARDS

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "WORKLOADS SIMULATED",
            "1,000",
            help="Research simulation reference"
        )

    with c2:
        st.metric(
            "CLOUD REGIONS",
            "03",
            help="Three simulated infrastructure regions"
        )

    with c3:
        st.metric(
            "TELEMETRY RECORDS",
            "187,963",
            help="Research dataset reference"
        )

    with c4:
        st.metric(
            "SLA REDUCTION",
            "51.45%",
            help="Research simulation reference compared with Best Fit"
        )

    st.markdown(
        "<div class='section-heading'>CLOUD RESOURCE MONITORING</div>",
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    # CPU AND MEMORY CHART

    with left:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=regions["Region"],
                y=regions["CPU Usage (%)"],
                name="CPU Usage",
                marker_color="#20b9ed"
            )
        )

        fig.add_trace(
            go.Bar(
                x=regions["Region"],
                y=regions["Memory Usage (%)"],
                name="Memory Usage",
                marker_color="#8b75ed"
            )
        )

        fig.update_layout(
            title="Regional Resource Utilization",
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Utilization (%)",
            yaxis=dict(range=[0, 100]),
            legend_title="Resources",
            margin=dict(l=10, r=10, t=55, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    # CPU CAPACITY DISTRIBUTION

    with right:

        fig = px.pie(
            regions,
            values="CPU Cores",
            names="Region",
            hole=0.65,
            title="Regional CPU Capacity Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    # REGION TABLE

    st.markdown(
        "<div class='section-heading'>CLOUD REGION STATUS</div>",
        unsafe_allow_html=True
    )

    st.dataframe(
        regions,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Research context: Region capacities, costs and latencies "
        "are simulated infrastructure parameters, not live cloud measurements."
    )


# ==================================================
# 7. CLOUD REGIONS
# ==================================================

elif page == "Cloud Regions":

    st.title("🌐 Cloud Region Explorer")

    st.caption(
        "Explore the three simulated infrastructure regions."
    )

    st.markdown("---")

    for _, region in regions.iterrows():

        with st.container(border=True):

            st.subheader(f"🌐 {region['Region']}")

            a, b, c = st.columns(3)

            a.metric(
                "CPU Cores",
                int(region["CPU Cores"])
            )

            b.metric(
                "Memory",
                f'{region["Memory (GB)"]} GB'
            )

            c.metric(
                "Network Latency",
                f'{region["Latency (ms)"]} ms'
            )

            st.write("CPU Utilization")

            st.progress(
                int(region["CPU Usage (%)"]) / 100
            )

            st.caption(
                f'{region["CPU Usage (%)"]}% utilized'
            )

            st.write("Memory Utilization")

            st.progress(
                int(region["Memory Usage (%)"]) / 100
            )

            st.caption(
                f'{region["Memory Usage (%)"]}% utilized'
            )

            st.write(
                f'Estimated hourly cost: **${region["Cost ($/hr)"]:.3f}**'
            )

    st.info(
        "All region information is based on the project's simulated "
        "infrastructure configuration."
    )


# ==================================================
# 8. WORKLOAD FORECASTING
# ==================================================

elif page == "Workload Forecasting":

    from modules.forecasting import (
        train_forecasting_model,
        forecast_next_cpu
    )

    st.title("📈 CPU Resource Forecasting")

    st.caption(
        "Random Forest-based next-hour CPU utilization prediction."
    )

    st.success(
        "Random Forest CPU Forecasting Model is integrated."
    )

    st.info(
        "Demo mode: Predictions use synthetic cloud telemetry, "
        "not live cloud-provider data."
    )

    @st.cache_resource
    def load_forecasting_model():
        return train_forecasting_model()

    with st.spinner("Loading forecasting model..."):

        model, telemetry, predictions, results = (
            load_forecasting_model()
        )

    st.subheader("Model Performance")

    a, b, c = st.columns(3)

    a.metric("MAE", results["MAE"])
    b.metric("RMSE", results["RMSE"])
    c.metric("R² Score", results["R2 Score"])

    st.divider()

    st.subheader("Select Cloud Region")

    region = st.selectbox(
        "Choose a region",
        ["Region A", "Region B", "Region C"]
    )

    region_data = telemetry[
        telemetry["region"] == region
    ].sort_values("timestamp")

    latest = region_data.iloc[-1]

    a, b, c = st.columns(3)

    a.metric(
        "Current CPU",
        f"{latest['cpu_usage']:.2f}%"
    )

    b.metric(
        "Memory Usage",
        f"{latest['memory_usage']:.2f}%"
    )

    c.metric(
        "Network Usage",
        f"{latest['network_usage']:.2f}%"
    )

    st.divider()

    st.subheader("Next-Hour CPU Forecast")

    if st.button(
        "Generate CPU Forecast",
        use_container_width=True
    ):

        predicted_cpu = forecast_next_cpu(
            model,
            telemetry,
            region
        )

        st.metric(
            "Predicted CPU Utilization",
            f"{predicted_cpu}%"
        )

        if predicted_cpu >= 80:

            st.warning(
                "High CPU demand predicted. "
                "Consider workload redistribution."
            )

        elif predicted_cpu >= 60:

            st.info(
                "Moderate CPU demand predicted."
            )

        else:

            st.success(
                "CPU capacity appears sufficient for the predicted demand."
            )

    st.divider()

    st.subheader("Actual vs Predicted CPU Usage")

    chart_data = predictions[
        predictions["region"] == region
    ].tail(100)

    st.line_chart(
        chart_data.set_index("timestamp")[
            ["next_cpu", "predicted_cpu"]
        ]
    )

    st.caption(
        "Actual next-hour CPU readings are compared with "
        "Random Forest predictions on the test dataset."
    )


# ==================================================
# 9. ANOMALY DETECTION
# ==================================================

elif page == "Anomaly Detection":

    from modules.anomaly_detection import (
        detect_anomalies,
        classify_resource_usage
    )

    st.title("🔍 Resource Anomaly Explorer")

    st.caption(
        "Isolation Forest-based statistical anomaly detection."
    )

    st.success(
        "Isolation Forest Anomaly Detection Model is integrated."
    )

    st.info(
        "Demo mode: Detection uses synthetic cloud telemetry, "
        "not live cloud-provider data."
    )

    @st.cache_resource
    def load_anomaly_model():
        return detect_anomalies()

    with st.spinner("Loading anomaly detection model..."):

        model, anomaly_data, summary = load_anomaly_model()

    st.subheader("Anomaly Detection Summary")

    a, b, c, d = st.columns(4)

    a.metric(
        "Total Records",
        summary["Total Records"]
    )

    b.metric(
        "Detected Anomalies",
        summary["Anomalies"]
    )

    c.metric(
        "Normal Records",
        summary["Normal Records"]
    )

    d.metric(
        "Anomaly Percentage",
        f'{summary["Anomaly Percentage"]}%'
    )

    st.divider()

    st.subheader("Cloud Resource Telemetry")

    selected_status = st.selectbox(
        "Filter Records",
        ["All", "Normal", "Anomaly"]
    )

    if selected_status == "All":

        filtered_data = anomaly_data

    else:

        filtered_data = anomaly_data[
            anomaly_data["status"] == selected_status
        ]

    st.dataframe(
        filtered_data[
            [
                "timestamp",
                "cpu_usage",
                "memory_usage",
                "network_usage",
                "status",
                "anomaly_score"
            ]
        ].tail(100),
        use_container_width=True
    )

    st.divider()

    st.subheader("Anomaly Distribution")

    chart_data = anomaly_data.copy()

    st.scatter_chart(
        chart_data,
        x="timestamp",
        y="cpu_usage",
        color="status"
    )

    st.divider()

    st.subheader("Test Resource Behaviour")

    st.write(
        "Enter resource utilization values to check "
        "whether the model identifies unusual behaviour."
    )

    a, b, c = st.columns(3)

    with a:

        cpu = st.slider(
            "CPU Utilization (%)",
            0, 100, 40
        )

    with b:

        memory = st.slider(
            "Memory Utilization (%)",
            0, 100, 50
        )

    with c:

        network = st.slider(
            "Network Utilization (%)",
            0, 100, 35
        )

    if st.button(
        "Analyze Resource Behaviour",
        use_container_width=True
    ):

        status, score = classify_resource_usage(
            model,
            cpu,
            memory,
            network
        )

        st.metric("Anomaly Score", score)

        if status == "Anomaly Detected":

            st.error(
                "⚠️ Anomalous resource behaviour detected!"
            )

        else:

            st.success(
                "Normal resource behaviour detected."
            )

        st.write("Detection Result:", status)

    st.caption(
        "Isolation Forest identifies statistical outliers. "
        "An anomaly is not necessarily a confirmed security attack."
    )


# ==================================================
# 10. INTELLIGENT WORKLOAD PLACEMENT
# ==================================================

elif page == "Intelligent Placement":

    from modules.placement import (
        get_cloud_regions,
        recommend_region,
        explain_placement
    )

    from modules.forecasting import (
        train_forecasting_model,
        forecast_next_cpu
    )

    from modules.anomaly_detection import detect_anomalies

    st.title("⚡ Intelligent Cloud Placement")

    st.caption(
        "Predictive resource-aware workload placement engine."
    )

    st.success(
        "STRATOS Predictive Placement Engine is integrated."
    )

    st.info(
        "Research simulation using synthetic cloud telemetry "
        "and simulated infrastructure parameters."
    )

    st.divider()

    st.subheader("Incoming Workload Requirements")

    a, b = st.columns(2)

    with a:

        workload_cpu = st.number_input(
            "Required CPU Cores",
            min_value=1,
            max_value=100,
            value=8
        )

    with b:

        workload_memory = st.number_input(
            "Required Memory (GB)",
            min_value=1,
            max_value=100,
            value=16
        )

    st.divider()

    st.subheader("Placement Optimization Priorities")

    latency_priority = st.slider(
        "Network Latency Priority",
        0, 100, 25
    )

    cost_priority = st.slider(
        "Operational Cost Priority",
        0, 100, 25
    )

    resource_priority = st.slider(
        "Resource Availability Priority",
        0, 100, 30
    )

    risk_priority = st.slider(
        "Anomaly Risk Priority",
        0, 100, 20
    )

    st.divider()

    st.subheader("Requested Workload")

    a, b = st.columns(2)

    a.metric(
        "CPU Requirement",
        f"{workload_cpu} Cores"
    )

    b.metric(
        "Memory Requirement",
        f"{workload_memory} GB"
    )

    @st.cache_resource
    def load_placement_forecasting_model():
        return train_forecasting_model()

    @st.cache_resource
    def load_placement_anomaly_model():
        return detect_anomalies()

    if st.button(
        "⚡ Generate Predictive Placement",
        use_container_width=True
    ):

        if sum([
            latency_priority,
            cost_priority,
            resource_priority,
            risk_priority
        ]) == 0:

            st.warning(
                "Please assign a priority to at least one parameter."
            )

        else:

            try:

                with st.spinner(
                    "STRATOS is forecasting and evaluating cloud regions..."
                ):

                    (
                        forecast_model,
                        telemetry,
                        predictions,
                        forecast_results
                    ) = load_placement_forecasting_model()

                    predicted_cpu = {}

                    for region_name in [
                        "Region A",
                        "Region B",
                        "Region C"
                    ]:

                        predicted_cpu[region_name] = (
                            forecast_next_cpu(
                                forecast_model,
                                telemetry,
                                region_name
                            )
                        )

                    (
                        anomaly_model,
                        anomaly_data,
                        anomaly_summary
                    ) = load_placement_anomaly_model()

                    cloud_regions = get_cloud_regions(
                        anomaly_data
                    )

                    best_region, eligible = recommend_region(

                        workload_cpu,
                        workload_memory,
                        cloud_regions,

                        latency_weight=latency_priority,
                        cost_weight=cost_priority,
                        resource_weight=resource_priority,
                        risk_weight=risk_priority,

                        predicted_cpu=predicted_cpu
                    )

                st.divider()

                st.subheader("📈 Regional CPU Forecasts")

                forecast_table = pd.DataFrame({

                    "Cloud Region": list(predicted_cpu.keys()),

                    "Predicted CPU (%)": list(
                        predicted_cpu.values()
                    )

                })

                st.dataframe(
                    forecast_table,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "Random Forest predictions estimate next-hour "
                    "CPU utilization for each simulated region."
                )

                st.divider()

                st.subheader("🔍 Anomaly Detection Results")

                a, b, c = st.columns(3)

                a.metric(
                    "Telemetry Records",
                    anomaly_summary["Total Records"]
                )

                b.metric(
                    "Detected Anomalies",
                    anomaly_summary["Anomalies"]
                )

                c.metric(
                    "Anomaly Percentage",
                    f'{anomaly_summary["Anomaly Percentage"]}%'
                )

                st.divider()

                st.subheader("⚡ Predictive Placement Decision")

                if best_region is None:

                    st.error(
                        "No suitable cloud region has sufficient "
                        "CPU and memory capacity after forecast adjustments."
                    )

                else:

                    result = explain_placement(best_region)

                    st.success(
                        f"Recommended Cloud Region: "
                        f"{result['Selected Region']}"
                    )

                    st.subheader("Selected Region Performance")

                    a, b, c = st.columns(3)

                    a.metric(
                        "Placement Score",
                        f"{result['Placement Score']}/100"
                    )

                    b.metric(
                        "Available CPU",
                        f"{result['Available CPU']} Cores"
                    )

                    c.metric(
                        "Available Memory",
                        f"{result['Available Memory']} GB"
                    )

                    a, b, c = st.columns(3)

                    a.metric(
                        "Predicted CPU",
                        f"{predicted_cpu[result['Selected Region']]}%"
                    )

                    b.metric(
                        "Network Latency",
                        f"{result['Latency']} ms"
                    )

                    c.metric(
                        "Hourly Cost",
                        f"${result['Hourly Cost']:.3f}"
                    )

                    st.metric(
                        "Regional Anomaly Risk",
                        f"{result['Anomaly Risk'] * 100:.2f}%"
                    )

                    st.divider()

                    st.subheader("Cloud Region Ranking")

                    ranking = eligible[
                        [
                            "region",
                            "available_cpu",
                            "available_memory",
                            "effective_cpu_usage",
                            "latency",
                            "cost",
                            "anomaly_risk",
                            "placement_score"
                        ]
                    ].copy()

                    ranking["predicted_cpu"] = (
                        ranking["region"].map(predicted_cpu)
                    )

                    ranking.columns = [
                        "Cloud Region",
                        "Available CPU",
                        "Available Memory",
                        "Forecast-Adjusted CPU (%)",
                        "Latency (ms)",
                        "Cost ($/hr)",
                        "Anomaly Risk",
                        "Placement Score",
                        "Predicted CPU (%)"
                    ]

                    ranking["Placement Score"] = (
                        ranking["Placement Score"].round(2)
                    )

                    ranking["Anomaly Risk"] = (
                        ranking["Anomaly Risk"] * 100
                    ).round(2)

                    st.dataframe(
                        ranking,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.divider()

                    st.subheader("STRATOS Decision Explanation")

                    st.write(
                        f"STRATOS recommends **"
                        f"{result['Selected Region']}** because "
                        "it achieved the highest weighted placement "
                        "score among regions satisfying the workload's "
                        "forecast-adjusted CPU and memory requirements."
                    )

                    st.info(
                        "The recommendation combines Random Forest "
                        "CPU forecasts, Isolation Forest anomaly risk "
                        "and regional infrastructure parameters."
                    )

                    st.warning(
                        "This is a simulated placement recommendation. "
                        "No actual cloud workload has been deployed or migrated."
                    )

            except Exception as e:

                st.error(
                    f"Predictive placement failed: {str(e)}"
                )

                st.exception(e)

# ==================================================
# 11. SIMULATION ANALYTICS
# ==================================================

elif page == "Simulation Analytics":

    from modules.simulation import run_simulation

    st.title("📊 Simulation Analytics")

    st.caption(
        "Evaluate traditional cloud scheduling algorithms "
        "against the intelligent STRATOS placement framework."
    )

    st.divider()

    st.subheader("⚙️ Simulation Configuration")

    col1, col2 = st.columns(2)

    with col1:

        num_workloads = st.slider(
            "Number of Workloads",
            min_value=20,
            max_value=500,
            value=100,
            step=20
        )

    with col2:

        seed = st.number_input(
            "Simulation Random Seed",
            min_value=1,
            max_value=9999,
            value=42,
            step=1
        )

    @st.cache_data(show_spinner=False)
    def load_simulation(num_workloads, seed):

        return run_simulation(
            num_workloads=int(num_workloads),
            seed=int(seed)
        )

    with st.spinner(
        "Running six cloud scheduling strategies..."
    ):

        (
            comparison,
            workloads,
            predicted_cpu,
            anomaly_summary,
            forecast_metrics
        ) = load_simulation(num_workloads, seed)

    st.success("Simulation completed successfully.")

    st.subheader("📌 Simulation Overview")

    a, b, c = st.columns(3)

    a.metric("Total Workloads", len(workloads))
    b.metric("Scheduling Strategies", len(comparison))
    c.metric("Cloud Regions", 3)

    st.divider()

    st.subheader("⚡ Full STRATOS Performance")

    stratos_result = comparison[
        comparison["Strategy"] == "Full STRATOS"
    ].iloc[0]

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "SLA Violations",
        int(stratos_result["SLA Violations"])
    )

    m2.metric(
        "Average Latency",
        f'{stratos_result["Latency (ms)"]} ms'
    )

    m3.metric(
        "Total Cost",
        f'${stratos_result["Total Cost ($)"]:.2f}'
    )

    m4, m5 = st.columns(2)

    m4.metric(
        "Placement Success",
        f'{stratos_result["Placement Success (%)"]}%'
    )

    m5.metric(
        "Resource Utilization",
        f'{stratos_result["Resource Utilization (%)"]}%'
    )

    st.divider()

    st.subheader("📉 SLA Violation Comparison")

    fig_sla = px.bar(
        comparison,
        x="Strategy",
        y="SLA Violations",
        color="Strategy",
        text="SLA Violations",
        title="SLA Violations Across Scheduling Strategies"
    )

    fig_sla.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title="Scheduling Strategy",
        yaxis_title="SLA Violations",
        margin=dict(l=10, r=10, t=55, b=10)
    )

    st.plotly_chart(fig_sla, use_container_width=True)

    st.subheader("🌐 Network Latency Comparison")

    fig_latency = px.bar(
        comparison,
        x="Strategy",
        y="Latency (ms)",
        color="Strategy",
        text="Latency (ms)",
        title="Average Network Latency"
    )

    fig_latency.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig_latency, use_container_width=True)

    st.subheader("💰 Infrastructure Cost Comparison")

    fig_cost = px.bar(
        comparison,
        x="Strategy",
        y="Total Cost ($)",
        color="Strategy",
        text="Total Cost ($)",
        title="Total Simulated Infrastructure Cost"
    )

    fig_cost.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig_cost, use_container_width=True)

    st.subheader("📦 Resource Utilization Comparison")

    fig_resource = px.bar(
        comparison,
        x="Strategy",
        y="Resource Utilization (%)",
        color="Strategy",
        text="Resource Utilization (%)",
        title="Average CPU and Memory Utilization"
    )

    fig_resource.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig_resource, use_container_width=True)

    st.divider()

    st.subheader("📊 Complete Scheduling Strategy Comparison")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📈 Regional CPU Forecasts")

    forecast_table = pd.DataFrame(
        list(predicted_cpu.items()),
        columns=["Cloud Region", "Predicted CPU (%)"]
    )

    st.dataframe(
        forecast_table,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🔍 Anomaly Detection Summary")

    x, y, z = st.columns(3)

    x.metric(
        "Telemetry Records",
        anomaly_summary["Total Records"]
    )

    y.metric(
        "Detected Anomalies",
        anomaly_summary["Anomalies"]
    )

    z.metric(
        "Anomaly Percentage",
        f'{anomaly_summary["Anomaly Percentage"]}%'
    )

    with st.expander("Forecast Model Evaluation"):

        st.write(
            "Random Forest forecasting evaluation results:"
        )

        st.json(forecast_metrics)

    st.divider()

    st.subheader("ℹ️ Simulation Methodology")

    st.markdown("""
    - All six scheduling strategies receive the same generated workload dataset.
    - Round Robin distributes workloads across eligible regions.
    - First Fit selects the first eligible region.
    - Best Fit selects the region with the smallest normalized remaining capacity.
    - Greedy Cost selects the least expensive eligible region.
    - Reactive STRATOS uses weighted placement scoring without forecast-adjusted CPU usage.
    - Full STRATOS uses weighted placement scoring with forecast-adjusted CPU usage and anomaly risk.
    - An SLA violation is counted when a workload cannot be placed or its selected region exceeds the simulated 40 ms latency threshold.
    - Infrastructure cost is estimated using regional hourly rates and workload duration.
    """)

    st.warning(
        "These are simulated research results. "
        "They do not represent actual cloud-provider "
        "deployment or migration measurements."
    )


# ==================================================
# 12. FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    <b style="color:#42dcff;">PROJECT STRATOS</b>
    | AUTONOMOUS GLOBAL CLOUD FABRIC
    <br><br>
    AI-Driven Workload Placement and Resource Intelligence
    <br><br>
    RESEARCH PROTOTYPE | PYTHON | STREAMLIT
</div>
""", unsafe_allow_html=True)                