# CineMetrics: Agentic Pre-Production & Probabilistic Risk Engine

> Submission for the Agentic Cinema Hackathon (Replit Partner Track)

## Live Deployment
- **Hosted App:** https://energetic-ripe-files--murtazakamal478.replit.app

## The Problem
Film pre-production historically relies on subjective creative feedback and isolated financial estimates. Creative decisions are rarely modeled against budget exposure prior to principal photography.

## The Multi-Agent Architecture
CineMetrics implements an automated three-tier pipeline:
1. **Screenplay Parsing Agent (Gemini 3.6 Flash):** Parses raw screenplay text into structured schemas (scene settings, pacing vectors, operational complexity scores) using structured outputs.
2. **Quantitative Risk Forecaster (NumPy Engine):** Ingests narrative parameters and computes pacing standard deviation ($\sigma$) alongside a parametric box office distribution ($P_{10}$ downside floor, $P_{50}$ median target, $P_{90}$ upside ceiling).
3. **Studio Greenlight Coordinator (Gemini 3.6 Flash):** Ingests both narrative structure and statistical forecasts to author an Executive Studio Greenlight Memo with budget caps and production safeguards.

## Tech Stack
- **AI / LLM:** Google GenAI SDK (`gemini-3.6-flash`)
- **Hosting & Infrastructure:** Replit Cloud Run
- **Web Interface:** Streamlit
- **Modeling:** NumPy, Pydantic v2

## License
MIT License
