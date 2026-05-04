import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Medicare Claims Analytics",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Medicare Claims Analytics Dashboard")
st.caption("CMS Medicare Provider Utilization & Payment Data | Molina Healthcare Claims Analyst Portfolio")

# --- Snowflake connection ---
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        database=st.secrets["snowflake"]["database"],
        warehouse=st.secrets["snowflake"]["warehouse"],
    )

@st.cache_data(ttl=600)
def run_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=cols)

# --- Load data ---
with st.spinner("Loading data from Snowflake..."):
    fact = run_query("""
        SELECT
            f.npi,
            f.hcpcs_code,
            f.state,
            f.provider_type,
            f.place_of_service,
            f.total_beneficiaries,
            f.total_services,
            f.avg_submitted_charge,
            f.avg_medicare_allowed_amount,
            f.avg_medicare_payment_amount,
            f.payment_to_charge_ratio,
            f.avg_denied_amount,
            s.hcpcs_description,
            s.is_drug_service
        FROM CLAIMS_HEALTHCARE.STAGING_MART.fct_provider_services f
        LEFT JOIN CLAIMS_HEALTHCARE.STAGING_MART.dim_service s
            ON f.hcpcs_code = s.hcpcs_code
    """)

# Normalize column names
fact.columns = [c.lower() for c in fact.columns]
fact["total_services"] = pd.to_numeric(fact["total_services"], errors="coerce")
fact["total_beneficiaries"] = pd.to_numeric(fact["total_beneficiaries"], errors="coerce")
fact["avg_submitted_charge"] = pd.to_numeric(fact["avg_submitted_charge"], errors="coerce")
fact["avg_medicare_payment_amount"] = pd.to_numeric(fact["avg_medicare_payment_amount"], errors="coerce")
fact["avg_denied_amount"] = pd.to_numeric(fact["avg_denied_amount"], errors="coerce")
fact["payment_to_charge_ratio"] = pd.to_numeric(fact["payment_to_charge_ratio"], errors="coerce")

# --- Sidebar filters ---
st.sidebar.header("Filters")

states = sorted(fact["state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect("State", states, default=states[:10])

provider_types = sorted(fact["provider_type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Provider Type", ["All"] + provider_types)

filtered = fact[fact["state"].isin(selected_states)]
if selected_type != "All":
    filtered = filtered[filtered["provider_type"] == selected_type]

st.sidebar.markdown("---")
st.sidebar.metric("Records shown", f"{len(filtered):,}")
st.sidebar.metric("Unique providers", f"{filtered['npi'].nunique():,}")
st.sidebar.metric("Unique services", f"{filtered['hcpcs_code'].nunique():,}")

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Descriptive — What Happened?", "🔍 Diagnostic — Why Did It Happen?"])

# ── Tab 1: Descriptive ──────────────────────────────────────────────
with tab1:
    st.subheader("Medicare Service Volume & Payments by State")

    state_summary = (
        filtered.groupby("state")
        .agg(
            total_services=("total_services", "sum"),
            total_beneficiaries=("total_beneficiaries", "sum"),
            avg_payment=("avg_medicare_payment_amount", "mean"),
        )
        .reset_index()
        .sort_values("total_services", ascending=False)
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Services", f"{state_summary['total_services'].sum():,.0f}")
    col2.metric("Total Beneficiaries", f"{state_summary['total_beneficiaries'].sum():,.0f}")
    col3.metric("Avg Medicare Payment", f"${state_summary['avg_payment'].mean():,.2f}")

    fig_state = px.bar(
        state_summary.head(15),
        x="state",
        y="total_services",
        color="avg_payment",
        color_continuous_scale="Blues",
        title="Top States by Total Services (color = avg Medicare payment)",
        labels={"state": "State", "total_services": "Total Services", "avg_payment": "Avg Payment ($)"},
    )
    st.plotly_chart(fig_state, use_container_width=True)

    st.subheader("Top 10 Provider Types by Volume")
    type_summary = (
        filtered.groupby("provider_type")
        .agg(total_services=("total_services", "sum"))
        .reset_index()
        .sort_values("total_services", ascending=False)
        .head(10)
    )
    fig_type = px.bar(
        type_summary,
        x="total_services",
        y="provider_type",
        orientation="h",
        title="Total Services by Provider Type",
        labels={"total_services": "Total Services", "provider_type": "Provider Type"},
        color="total_services",
        color_continuous_scale="Teal",
    )
    fig_type.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_type, use_container_width=True)

# ── Tab 2: Diagnostic ───────────────────────────────────────────────
with tab2:
    st.subheader("Payment-to-Charge Ratio by Provider Type")
    st.caption(
        "A lower ratio means Medicare reimburses a smaller share of what was billed — "
        "a key indicator of claim underpayment risk."
    )

    ratio_summary = (
        filtered[filtered["payment_to_charge_ratio"].notna()]
        .groupby("provider_type")
        .agg(
            avg_ratio=("payment_to_charge_ratio", "mean"),
            avg_submitted=("avg_submitted_charge", "mean"),
            avg_paid=("avg_medicare_payment_amount", "mean"),
            record_count=("npi", "count"),
        )
        .reset_index()
        .sort_values("avg_ratio")
        .head(15)
    )

    fig_ratio = px.bar(
        ratio_summary,
        x="avg_ratio",
        y="provider_type",
        orientation="h",
        title="Avg Payment-to-Charge Ratio by Provider Type (lower = higher denial risk)",
        labels={"avg_ratio": "Payment / Submitted Charge", "provider_type": "Provider Type"},
        color="avg_ratio",
        color_continuous_scale="RdYlGn",
    )
    fig_ratio.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_ratio, use_container_width=True)

    st.subheader("Average Denied Amount by Place of Service")
    st.caption(
        "Denied amount = submitted charge minus Medicare payment. "
        "Higher values highlight where claim underpayment is concentrated."
    )

    place_summary = (
        filtered[filtered["avg_denied_amount"].notna()]
        .groupby("place_of_service")
        .agg(
            avg_denied=("avg_denied_amount", "mean"),
            total_services=("total_services", "sum"),
        )
        .reset_index()
        .sort_values("avg_denied", ascending=False)
    )
    place_summary["place_label"] = place_summary["place_of_service"].map(
        {"F": "Facility", "O": "Office"}
    ).fillna(place_summary["place_of_service"])

    fig_denied = px.bar(
        place_summary,
        x="place_label",
        y="avg_denied",
        color="total_services",
        color_continuous_scale="Oranges",
        title="Avg Denied Amount by Place of Service",
        labels={
            "place_label": "Place of Service",
            "avg_denied": "Avg Denied Amount ($)",
            "total_services": "Total Services",
        },
    )
    st.plotly_chart(fig_denied, use_container_width=True)

    st.subheader("Drug vs. Non-Drug Services: Payment Gap Analysis")
    drug_summary = (
        filtered.groupby("is_drug_service")
        .agg(
            avg_submitted=("avg_submitted_charge", "mean"),
            avg_paid=("avg_medicare_payment_amount", "mean"),
            avg_denied=("avg_denied_amount", "mean"),
            total_services=("total_services", "sum"),
        )
        .reset_index()
    )
    drug_summary["service_type"] = drug_summary["is_drug_service"].map(
        {"Y": "Drug Service", "N": "Non-Drug Service"}
    ).fillna("Unknown")

    fig_drug = px.bar(
        drug_summary.melt(
            id_vars="service_type",
            value_vars=["avg_submitted", "avg_paid", "avg_denied"],
            var_name="metric",
            value_name="amount",
        ),
        x="service_type",
        y="amount",
        color="metric",
        barmode="group",
        title="Drug vs. Non-Drug: Submitted vs. Paid vs. Denied (avg $)",
        labels={"amount": "Amount ($)", "service_type": "Service Type", "metric": "Metric"},
        color_discrete_map={
            "avg_submitted": "#4C8BE8",
            "avg_paid": "#2ECC71",
            "avg_denied": "#E74C3C",
        },
    )
    st.plotly_chart(fig_drug, use_container_width=True)
