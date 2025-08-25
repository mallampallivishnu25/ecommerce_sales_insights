import streamlit as st, duckdb, pandas as pd, plotly.express as px, os

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")
con = duckdb.connect(DB)

st.set_page_config(page_title="E-commerce Sales Insights", layout="wide")
st.title("📈 E-commerce Sales Insights")


@st.cache_data
def get_kpis():
    return con.sql(
        """
        SELECT
          COALESCE(SUM(gross_revenue),0) AS revenue,
          COALESCE(AVG(gross_revenue),0) AS aov,
          COALESCE(COUNT(DISTINCT order_id),0) AS orders,
          COALESCE(COUNT(DISTINCT customer_id),0) AS customers
        FROM fact_orders
        """
    ).df().iloc[0]


k = get_kpis()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${{k['revenue']:.0f}}")
c2.metric("AOV", f"${{k['aov']:.2f}}")
c3.metric("Orders", int(k['orders']))
c4.metric("Customers", int(k['customers']))


@st.cache_data
def revenue_ts():
    return con.sql(
        """
        SELECT order_date, SUM(gross_revenue) AS revenue
        FROM fact_orders GROUP BY 1 ORDER BY 1
        """
    ).df()


ts = revenue_ts()
if not ts.empty:
    st.plotly_chart(px.line(ts, x="order_date", y="revenue", title="Revenue over time"), use_container_width=True)
else:
    st.info("No data yet. Run ingest and transforms to populate fact tables.")


st.header("Customer Segmentation")
if os.path.exists("data/external/rfm.parquet"):
    rfm = pd.read_parquet("data/external/rfm.parquet")
    st.dataframe(rfm.head(50))
else:
    st.caption("Run `python src/features/rfm.py` to generate RFM segments.")


st.header("Forecast")
if os.path.exists("data/external/forecast.parquet"):
    f = pd.read_parquet("data/external/forecast.parquet")
    st.plotly_chart(px.line(f, x="ds", y=["yhat","yhat_lower","yhat_upper"], title="90-day Forecast"), use_container_width=True)
else:
    st.caption("Run `python src/models/forecast_prophet.py` to generate forecast.")
