import sqlite3
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
import subprocess

# Page setup
st.set_page_config(
    page_title="Market Intelligence & Dynamic Pricing Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
    }
    /* Prediction Hero Card */
    .recommendation-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 24px;
        color: white;
        margin-top: 20px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    }
    .recommendation-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .recommendation-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 8px 0;
    }
    .recommendation-caption {
        color: #cbd5e1;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Data loader
def load_data():
    conn = sqlite3.connect("ecommerce_data.db")
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df

try:
    df = load_data()
    model = joblib.load("price_model.pkl")
    model_columns = joblib.load("model_columns.pkl")
except Exception as e:
    st.error(f"Error loading system artifacts: {e}")
    st.info("Make sure you've executed `pipeline.py` and `model.py` first.")
    st.stop()

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.title("⚡ Control Center")
    st.caption("Market Intelligence Pipeline")
    
    st.divider()
    st.subheader("Catalog Filters")
    rating_filter = st.multiselect(
        "Filter Star Ratings",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5]
    )
    
    min_catalog_price = float(df["price"].min())
    max_catalog_price = float(df["price"].max())
    price_range = st.slider(
        "Price Threshold (£)",
        min_value=min_catalog_price,
        max_value=max_catalog_price,
        value=(min_catalog_price, max_catalog_price)
    )
    
    st.divider()
    st.subheader("Data Pipeline Operations")
    if st.button("🔄 Sync Live Pipeline", use_container_width=True):
        with st.spinner("Scraping real catalog and updating SQLite..."):
            subprocess.run(["python", "pipeline.py"])
            st.success("Pipeline refreshed successfully!")
            st.rerun()

# Apply Sidebar Filters
filtered_df = df[
    (df["rating"].isin(rating_filter)) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# ----------------- HEADER -----------------
st.title("Competitor Price Intelligence & Demand Engine")
st.markdown("Automated market extraction, competitor benchmarking, and machine learning price simulations.")
st.markdown("<br>", unsafe_allow_html=True)

# ----------------- KPI METRICS ROW -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Tracked Catalog</div>
        <div class="metric-value">{len(filtered_df):,} <span style="font-size:0.9rem; font-weight:400; color:#64748b;">items</span></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Market Price</div>
        <div class="metric-value">£{filtered_df['price'].mean():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Median Catalog Price</div>
        <div class="metric-value">£{filtered_df['price'].median():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    in_stock_pct = (filtered_df['in_stock'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Stock Availability Rate</div>
        <div class="metric-value">{in_stock_pct:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2 = st.tabs(["📊 Market Analytics & Insights", "🎯 Predictive Pricing Simulator"])

with tab1:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Price Distribution Across Catalog")
        fig_hist = px.histogram(
            filtered_df,
            x="price",
            nbins=15,
            color_discrete_sequence=["#2563eb"],
            labels={"price": "Price (£)", "count": "Product Count"},
            template="plotly_white"
        )
        fig_hist.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
        st.plotly_chart(fig_hist, use_container_width=True)

    with chart_col2:
        st.subheader("Average Price by Star Rating")
        rating_summary = filtered_df.groupby("rating")["price"].mean().reset_index()
        fig_bar = px.bar(
            rating_summary,
            x="rating",
            y="price",
            color="price",
            color_continuous_scale="Blues",
            labels={"rating": "Star Rating (1-5)", "price": "Avg Price (£)"},
            template="plotly_white"
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Real-time Structured Records")
    st.dataframe(
        filtered_df[["title", "price", "rating", "in_stock"]].rename(columns={
            "title": "Product Title",
            "price": "Price (£)",
            "rating": "Star Rating",
            "in_stock": "In Stock Flag"
        }),
        use_container_width=True,
        height=320
    )

with tab2:
    st.subheader("Predictive Pricing Recommendation")
    st.markdown("Use the trained Random Forest model to calculate an optimal market entry price point based on product attributes.")

    sim_col1, sim_col2 = st.columns([1, 1.2])

    with sim_col1:
        st.markdown("#### Product Attributes")
        selected_rating = st.slider("Target Rating (Stars)", 1, 5, 4, 1)
        stock_status = st.radio("Inventory Status", ["In Stock", "Out of Stock"], horizontal=True)
        is_in_stock = 1 if stock_status == "In Stock" else 0
        
        sim_btn = st.button("Generate Optimal Price", type="primary", use_container_width=True)

    with sim_col2:
        if sim_btn:
            input_df = pd.DataFrame([{
                "rating": selected_rating,
                "in_stock": is_in_stock
            }])[model_columns]

            predicted_price = model.predict(input_df)[0]
            low_bound = predicted_price * 0.92
            high_bound = predicted_price * 1.08

            st.markdown(f"""
            <div class="recommendation-box">
                <div class="recommendation-title">Recommended Market Price</div>
                <div class="recommendation-value">£{predicted_price:.2f}</div>
                <div class="recommendation-caption">
                    Suggested dynamic corridor: <b>£{low_bound:.2f}</b> – <b>£{high_bound:.2f}</b><br>
                    Generated using a 100-estimator Random Forest trained on live SQLite records.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Select product parameters and click **Generate Optimal Price** to run inference.")