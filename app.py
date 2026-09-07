import streamlit as st
import pandas as pd
from agents import analyze_script, statistical_forecasting_engine, generate_studio_memo

st.set_page_config(page_title="CineMetrics", layout="wide")

st.title("🎬 CineMetrics: Agentic Pre-Production Engine")
st.caption("Autonomous screenplay breakdown and probabilistic box office modeling.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Screenplay Input")
    default_script = """EXT. CYBERPUNK ALLEY - NIGHT
Rain cascades down neon signs. KAI (30s) sprints past glowing trash bins, clutching an encrypted drive. Behind him, TWO ENFORCERS round the corner firing pulse weapons.

INT. ABANDONED SUBWAY - MOMENTS LATER
Kai slides through a rusted turnstile, gasping for breath. The comms unit in his ear crackles to life."""
    
    script_text = st.text_area("Paste Script Scene / Treatment", default_script, height=220)
    budget = st.number_input("Estimated Budget ($ USD)", min_value=10000, max_value=250000000, value=750000, step=50000)
    run_button = st.button("Run Multi-Agent Analysis", type="primary")

if run_button and script_text:
    with st.spinner("Executing Agent Pipeline: Parsing narrative structure & generating forecasts..."):
        # Agent 1
        analysis = analyze_script(script_text)
        
        # Agent 2
        stats = statistical_forecasting_engine(analysis, budget)
        
        # Agent 3
        memo = generate_studio_memo(analysis, stats)
        
    with col2:
        st.subheader("Statistical Projections")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("P10 Downside", f"${stats['projected_p10']:,.0f}")
        m_col2.metric("P50 Target", f"${stats['projected_p50']:,.0f}")
        m_col3.metric("P90 Upside", f"${stats['projected_p90']:,.0f}")
        
        st.info(f"**Genre:** {analysis.genre} | **Target Audience:** {analysis.estimated_target_audience} | **Pacing σ:** {stats['pacing_volatility_std']}")
        
        if analysis.scenes:
            chart_data = pd.DataFrame({
                "Scene": [f"Scene {s.scene_number}" for s in analysis.scenes],
                "Pacing Intensity": [s.pacing_intensity for s in analysis.scenes]
            })
            st.line_chart(chart_data.set_index("Scene"))
            
    st.markdown("---")
    st.subheader("Executive Greenlight Memo")
    st.markdown(memo)
