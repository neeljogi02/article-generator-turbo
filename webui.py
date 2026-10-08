import os
import streamlit as st
from app.core.search import FreeResearcher
from app.core.outliner import FreeOutliner
from app.core.drafter import FreeDrafter
from app.core.media import FreeMediaFetcher

st.set_page_config(
    page_title="ArticleGeneratorTurbo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E88E5; margin-bottom: 0px; }
    .sub-title { font-size: 1.05rem; color: #666; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ ArticleGeneratorTurbo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">100% Free, Zero-API-Key Automated Article Engine</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Generation Settings")
    topic_input = st.text_input("Article Topic", value="How Agentic AI Workflows Are Replacing Traditional RPA")
    audience_input = st.text_input("Target Audience", value="Software Engineers & Tech Leaders")
    num_sources = st.slider("Max Search Sources", min_value=2, max_value=6, value=4)
    generate_btn = st.button("🚀 Generate Article", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("### 🛠️ Architecture")
    st.caption("- **Research:** DuckDuckGo / OpenSearch\n- **LLM Engine:** Free Inference Gateways\n- **Media:** Free Stock / AI Image Endpoints\n- **Cost:** $0.00 / Free Tier")

# Session state initialization
if "full_markdown" not in st.session_state:
    st.session_state.full_markdown = ""
if "plan_data" not in st.session_state:
    st.session_state.plan_data = None

# --- Main Interface ---
col_left, col_right = st.columns([1, 1], gap="large")

if generate_btn and topic_input:
    col_left.empty()
    col_right.empty()
    
    status_box = st.status("🚀 Initializing Pipeline...", expanded=True)
    progress_bar = st.progress(0.0)

    # 1. Research Stage
    status_box.write("🔍 Step 1: Performing live web research...")
    researcher = FreeResearcher(max_results=num_sources)
    sources = researcher.search_topic(topic_input)
    research_text = researcher.format_sources_for_prompt(sources)
    progress_bar.progress(0.2)

    # 2. Outline & SEO Blueprint Stage
    status_box.write("🧠 Step 2: Generating structured SEO blueprint...")
    outliner = FreeOutliner()
    plan = outliner.generate_plan(topic_input, audience_input, sources, research_text)
    st.session_state.plan_data = plan
    progress_bar.progress(0.4)

    # 3. Drafting & Media Synthesis
    status_box.write("✍️ Step 3: Drafting sections & fetching visuals...")
    drafter = FreeDrafter()
    media = FreeMediaFetcher()

    markdown_parts = [
        f"# {plan.seo_title}\n\n",
        f"> **Meta Description:** {plan.meta_description}\n\n",
        f"**Target Audience:** `{plan.target_audience}` | **Primary Keywords:** `{', '.join(plan.primary_keywords)}`\n\n---\n\n"
    ]

    total_secs = len(plan.sections)
    context_accumulator = []

    for idx, sec in enumerate(plan.sections, 1):
        status_box.write(f"📝 Writing section {idx}/{total_secs}: *{sec.heading}*...")
        
        # Free image URL
        img_url = media.get_image_url(sec.image_prompt)
        
        # Section drafting
        summary_context = " ".join(context_accumulator[-2:])
        section_content = drafter.draft_section(sec, summary_context, research_text)
        context_accumulator.append(sec.heading)

        markdown_parts.append(f"## {sec.heading}\n\n")
        markdown_parts.append(f"![{sec.heading}]({img_url})\n\n")
        markdown_parts.append(f"{section_content}\n\n---\n\n")
        
        progress_bar.progress(0.4 + (0.5 * (idx / total_secs)))

    # 4. Citations & References
    markdown_parts.append("## References & Sources\n\n")
    for s in plan.sources:
        markdown_parts.append(f"- [{s.title}]({s.url})\n")

    st.session_state.full_markdown = "".join(markdown_parts)
    progress_bar.progress(1.0)
    status_box.update(label="✅ Article Generated Successfully!", state="complete", expanded=False)

# --- Live Display & Preview Pane ---
if st.session_state.full_markdown:
    with col_left:
        st.subheader("📋 Blueprint & Raw Markdown")
        
        if st.session_state.plan_data:
            with st.expander("📌 SEO Metadata", expanded=False):
                st.write(f"**Title:** {st.session_state.plan_data.seo_title}")
                st.write(f"**Description:** {st.session_state.plan_data.meta_description}")
                st.write(f"**Keywords:** {', '.join(st.session_state.plan_data.primary_keywords)}")

        st.download_button(
            label="💾 Download Article (.md)",
            data=st.session_state.full_markdown,
            file_name="article.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.text_area(
            "Raw Markdown Code",
            st.session_state.full_markdown,
            height=580
        )

    with col_right:
        st.subheader("👁️ Live Visual Preview")
        preview_container = st.container(height=650)
        with preview_container:
            st.markdown(st.session_state.full_markdown)
else:
    with col_left:
        st.info("👈 Enter a topic in the sidebar and click **'Generate Article'** to start.")
    with col_right:
        st.caption("Live article preview will render here once generated.")
