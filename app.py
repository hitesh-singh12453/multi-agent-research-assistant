import streamlit as st
from pipeline import run_research_pipeline


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Research Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Custom styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #101827 45%, #0b1220 100%);
    }
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 2rem 2.1rem;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 22px;
        background: linear-gradient(125deg, rgba(30, 41, 59, .96), rgba(15, 23, 42, .88));
        margin-bottom: 1.5rem;
    }
    .eyebrow {
        color: #93c5fd;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .65rem;
    }
    .hero h1 {
        color: #f8fafc;
        font-size: clamp(2rem, 4vw, 3rem);
        line-height: 1.12;
        margin: 0 0 .7rem 0;
        font-weight: 750;
    }
    .hero p {
        color: #cbd5e1;
        font-size: 1.02rem;
        margin: 0;
        max-width: 760px;
    }
    .stage-card {
    border: 1px solid rgba(148, 163, 184, .2);
    background: rgba(30, 41, 59, .55);
    border-radius: 15px;
    padding: 1.1rem 1.15rem;
    height: 154px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    }
    .stage-number {
        color: #60a5fa;
        font-size: .75rem;
        font-weight: 800;
        letter-spacing: .12em;
    }
    .stage-title {
        color: #f8fafc;
        font-size: 1rem;
        font-weight: 700;
        margin: .35rem 0 .2rem 0;
    }
    .stage-desc {
        color: #94a3b8;
        font-size: .83rem;
    }
    .section-heading {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 700;
        margin: .3rem 0 1rem 0;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 12px;
    }
    div.stButton > button {
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 700;
    }
    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 650;
    }
    /* Improve text visibility throughout the application */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown strong,
    .stMarkdown em,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
    color: #e5e7eb !important;
    }

    /* Links */
    .stMarkdown a {
    color: #93c5fd !important;
    }

    /* Tables */
    .stMarkdown table,
    .stMarkdown th,
    .stMarkdown td {
    color: #e5e7eb !important;
    border-color: rgba(148, 163, 184, .3) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI-powered research workflow</div>
        <h1>Research Studio</h1>
        <p>
            Turn a research question into a structured report.
            Four components work together: web search, page reading,
            report writing, and critical review.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Show the four stages in the user's pipeline
# --------------------------------------------------
stage_columns = st.columns(4)
stages = [
    ("01", "Search Agent", "Finds relevant information and source URLs."),
    ("02", "Reader Agent", "Selects a source and extracts page content."),
    ("03", "Research Writer", "Creates a structured research report."),
    ("04", "Critic", "Reviews the report and provides feedback.")
]

for column, (number, title, description) in zip(stage_columns, stages):
    with column:
        st.markdown(
            f"""
            <div class="stage-card">
                <div class="stage-number">STAGE {number}</div>
                <div class="stage-title">{title}</div>
                <div class="stage-desc">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# --------------------------------------------------
# Research input
# --------------------------------------------------
st.markdown('<div class="section-heading">What would you like to research?</div>',
            unsafe_allow_html=True)

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder="Example: Impact of war on stock markets",
        height=90,
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button(
        "🚀  Start research",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not topic.strip():
        st.warning("Enter a research topic before starting.")
    else:
        try:
            with st.status(
                "Research pipeline is running...",
                expanded=True
            ) as status:
                st.write("Search Agent is gathering information.")
                st.write("Reader Agent is processing a relevant source.")
                st.write("Writer is preparing the research report.")
                st.write("Critic is reviewing the report.")

                # Run the exact pipeline supplied by the user.
                result = run_research_pipeline(topic.strip())

                status.update(
                    label="Research completed",
                    state="complete",
                    expanded=False
                )

            st.session_state["research_result"] = result
            st.session_state["research_topic"] = topic.strip()

        except Exception as error:
            st.error("The research pipeline failed.")
            st.exception(error)

# --------------------------------------------------
# Results
# --------------------------------------------------
if "research_result" in st.session_state:
    result = st.session_state["research_result"]
    saved_topic = st.session_state["research_topic"]

    st.divider()
    st.markdown('<div class="section-heading">Research workspace</div>',
                unsafe_allow_html=True)
    st.caption(f"Completed topic: {saved_topic}")

    report = result.get("report", "")
    search_results = result.get("search_results", "")
    scraped_content = result.get("scraped_content", "")
    feedback = result.get("feedback", "")

    # Main report
    st.markdown("### 📑 Final research report")
    if report:
        st.markdown(report)
        st.download_button(
            label="⬇️ Download research report",
            data=report,
            file_name="research_report.md",
            mime="text/markdown"
        )
    else:
        st.info("The pipeline did not return a report.")

    st.divider()

    # Supporting outputs
    st.markdown("### Agent details")
    search_tab, reader_tab, critic_tab = st.tabs(
        ["🔎 Search results", "📖 Scraped content", "🧪 Critic review"]
    )

    with search_tab:
        if search_results:
            st.markdown(search_results)
        else:
            st.info("No search results were returned.")

    with reader_tab:
        if scraped_content:
            st.markdown(scraped_content)
        else:
            st.info("No scraped content was returned.")

    with critic_tab:
        if feedback:
            st.markdown(feedback)
        else:
            st.info("No critic feedback was returned.")
