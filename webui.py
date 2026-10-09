import os
import streamlit as st
from app.core.search import FreeResearcher
from app.core.outliner import FreeOutliner
from app.core.drafter import FreeDrafter
from app.core.media import FreeMediaFetcher
from app.core.blogger import BloggerPublisher
from app.core.trends import GoogleTrendsFetcher
from app.core.trends_generator import TrendingArticleEngine

st.set_page_config(
    page_title="ArticleGeneratorTurbo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E88E5; margin-bottom: 2px; }
    .sub-title { font-size: 1.0rem; color: #666; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ ArticleGeneratorTurbo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">100% Free SEO Engine & Google Trends Blogger Auto-Publisher</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📢 Blogger Auto-Publisher")
    blog_id_input = st.text_input("Blogger Blog ID", placeholder="e.g., 739281928374829102")
    publish_as_draft = st.checkbox("Save as Draft (Unchecked = Live)", value=False)
    has_secret = os.path.exists("client_secret.json")
    if not has_secret:
        st.warning("⚠️ Place `client_secret.json` in root directory to enable direct Blogger publishing.")
    st.divider()
    st.caption("Target Site: **Current Affairs Viva**\nRegion: **India / Gujarat Focus**")

tab1, tab2 = st.tabs(["🔥 Google Trends Mode", "⚡ Standard Article Generator"])

# --- TAB 1: GOOGLE TRENDS MODE ---
with tab1:
    st.subheader("🔥 Live Google Trends Explorer (India / Regional)")
    col_t1, col_t2 = st.columns([1, 2], gap="large")
    
    with col_t1:
        st.markdown("#### 1. Fetch Real-Time Trends")
        geo_select = st.selectbox("Region", ["IN (India)", "US (United States)", "GB (United Kingdom)"], index=0)
        geo_code = geo_select.split()[0]
        
        if st.button("🔄 Refresh Live Trends", use_container_width=True):
            with st.spinner("Fetching latest Google Trends RSS..."):
                fetcher = GoogleTrendsFetcher()
                st.session_state.trending_list = fetcher.fetch_trending_topics(geo=geo_code, limit=10)

        if "trending_list" not in st.session_state:
            fetcher = GoogleTrendsFetcher()
            st.session_state.trending_list = fetcher.fetch_trending_topics(geo="IN", limit=10)

        trend_titles = [f"{t['title']} ({t['traffic']})" for t in st.session_state.trending_list]
        selected_trend_label = st.selectbox("Select Trending Topic:", trend_titles)
        selected_index = trend_titles.index(selected_trend_label) if selected_trend_label else 0
        active_trend = st.session_state.trending_list[selected_index]

        custom_angle = st.text_input("Custom Focus / Angle:", value="Competitive Exams, Current Affairs & GK Notes")
        gen_trend_btn = st.button("🚀 Generate Trend Article", type="primary", use_container_width=True)

    with col_t2:
        st.markdown("#### 2. SEO Report & Blogger Article")
        if "trend_article_output" not in st.session_state:
            st.session_state.trend_article_output = ""

        if gen_trend_btn:
            with st.spinner(f"Synthesizing Google Trends SEO strategy for '{active_trend['title']}'..."):
                t_engine = TrendingArticleEngine()
                news_ctx = " | ".join([n['title'] for n in active_trend.get('news', [])])
                st.session_state.trend_article_output = t_engine.generate_trending_article(
                    topic=active_trend['title'],
                    target_market="India (Current Affairs Viva)",
                    extra_context=news_ctx
                )

        if st.session_state.trend_article_output:
            btn_t_col1, btn_t_col2 = st.columns(2)
            with btn_t_col1:
                st.download_button(
                    label="💾 Download Report (.md)",
                    data=st.session_state.trend_article_output,
                    file_name="trending_article_seo.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with btn_t_col2:
                if st.button("🌐 Publish Trend to Blogger", use_container_width=True):
                    if not blog_id_input:
                        st.error("Please enter your Blogger Blog ID in the sidebar first!")
                    elif not os.path.exists("client_secret.json"):
                        st.error("Please add `client_secret.json` to the root directory.")
                    else:
                        try:
                            with st.spinner("Publishing to Blogger..."):
                                publisher = BloggerPublisher()
                                publisher.publish_post(
                                    blog_id=blog_id_input.strip(),
                                    title=f"{active_trend['title']} - Latest Current Affairs & Updates",
                                    md_content=st.session_state.trend_article_output,
                                    tags=["Current Affairs 2026", "Google Trends", "GK Notes"],
                                    is_draft=publish_as_draft
                                )
                                st.success("🎉 Successfully published to Blogger!")
                        except Exception as e:
                            st.error(f"Publish error: {e}")

            st.text_area("Full SEO Report & Blogger HTML", st.session_state.trend_article_output, height=520)
        else:
            st.info("Select a trending topic on the left and click **'Generate Trend Article'**.")

# --- TAB 2: STANDARD GENERATOR ---
with tab2:
    st.subheader("⚡ Long-Form Article Generator")
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        topic_input = st.text_input("Article Topic", value="How Agentic AI Workflows Are Replacing Traditional RPA")
        audience_input = st.text_input("Target Audience", value="Software Engineers & Tech Leaders")
        num_sources = st.slider("Max Search Sources", min_value=2, max_value=6, value=4)
        generate_btn = st.button("🚀 Generate Standard Article", type="primary", use_container_width=True)

    if "full_markdown" not in st.session_state:
        st.session_state.full_markdown = ""
    if "plan_data" not in st.session_state:
        st.session_state.plan_data = None

    if generate_btn and topic_input:
        status_box = st.status("🚀 Launching Pipeline...", expanded=True)
        progress_bar = st.progress(0.0)

        status_box.write("🔍 Running live research...")
        researcher = FreeResearcher(max_results=num_sources)
        sources = researcher.search_topic(topic_input)
        research_text = researcher.format_sources_for_prompt(sources)
        progress_bar.progress(0.3)

        status_box.write("🧠 Structuring SEO blueprint...")
        outliner = FreeOutliner()
        plan = outliner.generate_plan(topic_input, audience_input, sources, research_text)
        st.session_state.plan_data = plan
        progress_bar.progress(0.6)

        status_box.write("✍️ Drafting sections & media...")
        drafter = FreeDrafter()
        media = FreeMediaFetcher()

        markdown_parts = [
            f"# {plan.seo_title}\n\n",
            f"> **Meta Description:** {plan.meta_description}\n\n---\n\n"
        ]

        for sec in plan.sections:
            img_url = media.get_image_url(sec.image_prompt)
            sec_text = drafter.draft_section(sec, "", research_text)
            markdown_parts.append(f"## {sec.heading}\n\n![{sec.heading}]({img_url})\n\n{sec_text}\n\n---\n\n")

        markdown_parts.append("## References\n\n")
        for s in plan.sources:
            markdown_parts.append(f"- [{s.title}]({s.url})\n")

        st.session_state.full_markdown = "".join(markdown_parts)
        progress_bar.progress(1.0)
        status_box.update(label="✅ Complete!", state="complete", expanded=False)

    if st.session_state.full_markdown:
        with col_left:
            st.download_button(
                label="💾 Download Article (.md)",
                data=st.session_state.full_markdown,
                file_name="article.md",
                mime="text/markdown",
                use_container_width=True
            )
            st.text_area("Markdown Code", st.session_state.full_markdown, height=450)
        with col_right:
            st.markdown(st.session_state.full_markdown)
