"""
OUVC - Over/Under Value Checker
Streamlit Web Application

A web interface for analyzing cryptocurrency and Dubai real estate valuations.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from crypto_module.undervalued_test import run_undervalued_test
from crypto_module.data_fetcher import CryptoDataFetcher
from dubai_property_module.property_analyzer import analyze_dubai_property
from shared_utils.secrets_manager import load_secrets, get_secret


# Page configuration
st.set_page_config(
    page_title="OUVC - Over/Under Value Checker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables"""
    if 'api_keys_loaded' not in st.session_state:
        st.session_state.api_keys_loaded = False
        try:
            load_secrets()
            st.session_state.api_keys_loaded = True
        except Exception:
            st.session_state.api_keys_loaded = False


def display_header():
    """Display application header"""
    st.title(" OUVC - Over/Under Value Checker")
    st.markdown("""
    Analyze valuations using data-driven algorithms.
    """)
    st.divider()


def crypto_analysis_page():
    """Cryptocurrency analysis interface"""
    st.header("🪙 Cryptocurrency Valuation Analysis")

    st.markdown("""
    This tool uses the **60-Second Undervalued Test** to determine if a cryptocurrency
    is undervalued, fairly valued, or overvalued based on fundamental metrics.
    """)

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Crypto Selection")

        # Supported cryptocurrencies
        supported_cryptos = [
            "Bitcoin", "Ethereum", "Zcash", "Monero", "Cardano", "Solana",
            "Polkadot", "Chainlink", "Avalanche", "Polygon", "Algorand",
            "Cosmos", "Tezos", "VeChain", "Hedera", "NEAR Protocol",
            "Fantom", "Harmony", "Elrond", "Zilliqa", "Theta"
        ]

        crypto_name = st.selectbox(
            "Select Cryptocurrency",
            options=supported_cryptos,
            help="Choose a cryptocurrency to analyze"
        )

        use_api = st.checkbox(
            "Fetch live data from CoinGecko API",
            value=st.session_state.api_keys_loaded,
            help="If unchecked, you'll need to enter data manually"
        )

    with col2:
        st.subheader("Manual Data Entry")
        st.markdown("*Required if API is not used*")

        new_coins_per_year = st.number_input(
            "New Coins Created Per Year",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Annual inflation in number of new coins",
            disabled=use_api
        )

        value_locked = st.number_input(
            "Total Value Locked (USD)",
            min_value=0.0,
            value=0.0,
            step=1000000.0,
            help="Total value locked in protocols/DeFi",
            disabled=use_api
        )

    st.divider()

    # Analysis button
    if st.button("🔍 Analyze Cryptocurrency", type="primary", use_container_width=True):
        with st.spinner(f"Analyzing {crypto_name}..."):
            try:
                if use_api:
                    # Fetch data from API
                    fetcher = CryptoDataFetcher()
                    coin_data = fetcher.get_coin_data(crypto_name)

                    if coin_data:
                        result = run_undervalued_test(
                            crypto_name=crypto_name,
                            new_coins_per_year=coin_data.get('new_coins_per_year', 0),
                            value_locked=coin_data.get('value_locked', 0),
                            coin_data=coin_data
                        )
                    else:
                        st.error(f"Could not fetch data for {crypto_name}. Please try manual entry.")
                        result = None
                else:
                    # Use manual data
                    if new_coins_per_year == 0 and value_locked == 0:
                        st.warning("⚠️ Please enter values for manual data entry or enable API fetching.")
                        result = None
                    else:
                        result = run_undervalued_test(
                            crypto_name=crypto_name,
                            new_coins_per_year=new_coins_per_year,
                            value_locked=value_locked
                        )

                # Display results
                if result:
                    st.success("✅ Analysis Complete!")

                    # Display verdict with color coding
                    verdict = result.get('verdict', 'UNKNOWN')
                    if verdict == "STRONG BUY":
                        st.success(f"## 🎯 Verdict: {verdict}")
                    elif verdict == "BUY":
                        st.info(f"## 📈 Verdict: {verdict}")
                    elif verdict == "HOLD":
                        st.warning(f"## ⏸️ Verdict: {verdict}")
                    else:
                        st.error(f"## ⛔ Verdict: {verdict}")

                    # Display metrics
                    st.subheader("Key Metrics")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)

                    with metric_col1:
                        st.metric(
                            "Inflation Rate",
                            f"{result.get('inflation_rate', 0):.2f}%"
                        )

                    with metric_col2:
                        st.metric(
                            "Market Cap (FDV)",
                            f"${result.get('fdmc', 0):,.0f}"
                        )

                    with metric_col3:
                        if result.get('fdmc_to_value_locked'):
                            st.metric(
                                "FDMC/Value Locked Ratio",
                                f"{result.get('fdmc_to_value_locked', 0):.2f}x"
                            )
                        else:
                            st.metric("Value Locked", f"${result.get('value_locked', 0):,.0f}")

                    # Display reasoning
                    st.subheader("Analysis Reasoning")
                    reasoning = result.get('reasoning', [])
                    if reasoning:
                        for reason in reasoning:
                            st.markdown(f"- {reason}")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)


def property_analysis_page():
    """Dubai property valuation interface"""
    st.header("🏠 Dubai Property Valuation Analysis")

    st.markdown("""
    Analyze Dubai property valuations using comparable property data from Bayut.
    Get estimated values, confidence intervals, and rental yield analysis.
    """)

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Property Details")

        area = st.selectbox(
            "Area",
            options=[
                "Dubai Marina", "Downtown Dubai", "JBR", "Palm Jumeirah",
                "Business Bay", "DIFC", "JVC", "Sports City", "Discovery Gardens"
            ],
            help="Select the property area"
        )

        property_type = st.selectbox(
            "Property Type",
            options=["Apartment", "Villa", "Townhouse", "Penthouse", "Studio"],
            help="Select the property type"
        )

        bedrooms = st.number_input(
            "Number of Bedrooms",
            min_value=0,
            max_value=10,
            value=2,
            step=1,
            help="Number of bedrooms (0 for studio)"
        )

    with col2:
        st.subheader("Property Specifications")

        size_sqft = st.number_input(
            "Size (Square Feet)",
            min_value=100.0,
            max_value=50000.0,
            value=1000.0,
            step=50.0,
            help="Total property size in square feet"
        )

        asking_price = st.number_input(
            "Asking Price (AED)",
            min_value=0.0,
            value=1000000.0,
            step=50000.0,
            help="The asking price in AED"
        )

        use_api = st.checkbox(
            "Use Bayut API for live data",
            value=st.session_state.api_keys_loaded,
            help="Fetch comparable properties from Bayut"
        )

    st.divider()

    # Analysis button
    if st.button("🔍 Analyze Property", type="primary", use_container_width=True):
        with st.spinner("Analyzing property..."):
            try:
                result = analyze_dubai_property(
                    area=area,
                    property_type=property_type,
                    bedrooms=bedrooms,
                    size_sqft=size_sqft,
                    asking_price_aed=asking_price,
                    use_api=use_api
                )

                if result:
                    st.success("✅ Analysis Complete!")

                    # Display verdict
                    verdict = result.get('verdict', 'UNKNOWN')
                    if "Underpriced" in verdict or "Good Deal" in verdict:
                        st.success(f"## 🎯 {verdict}")
                    elif "Fairly Priced" in verdict or "Reasonable" in verdict:
                        st.info(f"## ✔️ {verdict}")
                    else:
                        st.warning(f"## ⚠️ {verdict}")

                    # Display metrics
                    st.subheader("Valuation Metrics")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        st.metric(
                            "Asking Price",
                            f"AED {asking_price:,.0f}"
                        )

                    with metric_col2:
                        estimated_value = result.get('estimated_value', 0)
                        st.metric(
                            "Estimated Value",
                            f"AED {estimated_value:,.0f}"
                        )

                    with metric_col3:
                        confidence_range = result.get('confidence_range', {})
                        low = confidence_range.get('low', 0)
                        high = confidence_range.get('high', 0)
                        st.metric(
                            "Value Range (±10%)",
                            f"AED {low:,.0f} - {high:,.0f}"
                        )

                    with metric_col4:
                        rental_yield = result.get('rental_yield', 0)
                        st.metric(
                            "Expected Rental Yield",
                            f"{rental_yield:.2f}%"
                        )

                    # Display reasoning
                    st.subheader("Analysis Details")

                    # Comparable properties count
                    comparable_count = result.get('comparable_properties_count', 0)
                    st.info(f"📊 Analysis based on **{comparable_count}** comparable properties")

                    # Display reasoning points
                    reasoning = result.get('reasoning', [])
                    if reasoning:
                        st.markdown("**Key Points:**")
                        for reason in reasoning:
                            st.markdown(f"- {reason}")

                    # Price per sqft comparison
                    if 'price_per_sqft' in result:
                        st.subheader("Price per Square Foot")
                        comp_col1, comp_col2 = st.columns(2)

                        with comp_col1:
                            asking_per_sqft = asking_price / size_sqft
                            st.metric("Asking Price per SqFt", f"AED {asking_per_sqft:.2f}")

                        with comp_col2:
                            market_per_sqft = result.get('price_per_sqft', 0)
                            st.metric("Market Average per SqFt", f"AED {market_per_sqft:.2f}")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)


def demo_mode_page():
    """Demo mode with sample data"""
    st.header("🎮 Demo Mode")

    st.markdown("""
    Try out the OUVC tool with pre-loaded sample data. No API keys required!
    """)

    # Demo selection
    demo_type = st.radio(
        "Select Demo",
        options=["Cryptocurrency Demo", "Property Demo"],
        horizontal=True
    )

    st.divider()

    if demo_type == "Cryptocurrency Demo":
        st.subheader("Demo: Zcash Analysis")
        st.info("""
        This demo analyzes **Zcash** using sample data:
        - New coins per year: ~1,200,000
        - Total Value Locked: $50,000,000
        """)

        if st.button("Run Crypto Demo", type="primary"):
            with st.spinner("Running demo..."):
                try:
                    result = run_undervalued_test(
                        crypto_name="Zcash",
                        new_coins_per_year=1200000,
                        value_locked=50000000
                    )

                    if result:
                        st.success("✅ Demo Complete!")

                        verdict = result.get('verdict', 'UNKNOWN')
                        if verdict == "STRONG BUY":
                            st.success(f"## 🎯 Verdict: {verdict}")
                        elif verdict == "BUY":
                            st.info(f"## 📈 Verdict: {verdict}")
                        else:
                            st.warning(f"## Verdict: {verdict}")

                        st.json(result)

                except Exception as e:
                    st.error(f"Demo error: {str(e)}")

    else:
        st.subheader("Demo: Dubai Marina Apartment")
        st.info("""
        This demo analyzes a **2-bedroom apartment in Dubai Marina**:
        - Size: 1,200 sq ft
        - Asking Price: AED 1,500,000
        """)

        if st.button("Run Property Demo", type="primary"):
            with st.spinner("Running demo..."):
                try:
                    result = analyze_dubai_property(
                        area="Dubai Marina",
                        property_type="Apartment",
                        bedrooms=2,
                        size_sqft=1200,
                        asking_price=1500000,
                        use_api=False
                    )

                    if result:
                        st.success("✅ Demo Complete!")

                        verdict = result.get('verdict', 'UNKNOWN')
                        st.info(f"## {verdict}")

                        st.json(result)

                except Exception as e:
                    st.error(f"Demo error: {str(e)}")


def about_page():
    """About page with information"""
    st.header("ℹ️ About OUVC")

    st.markdown("""
    ## Over/Under Value Checker

    OUVC is a dual-module valuation analysis tool designed to help investors make
    data-driven decisions in two different markets:

    ### 🪙 Cryptocurrency Module

    Uses the **60-Second Undervalued Test** algorithm to evaluate cryptocurrencies based on:
    - Inflation rate (new coin creation)
    - Fully Diluted Market Cap (FDMC)
    - Total Value Locked in protocols
    - FDMC/Value Locked ratio

    **Data Source:** CoinGecko API

    ### 🏠 Dubai Property Module

    Analyzes Dubai real estate properties using:
    - Comparable property analysis
    - Area-specific market data
    - Rental yield calculations
    - Confidence interval estimation (±10%)

    **Data Source:** Bayut API (via RapidAPI)

    ---

    ## Features

    - ✅ Real-time data fetching from APIs
    - ✅ Manual data entry option
    - ✅ Demo mode (no API keys required)
    - ✅ Detailed valuation reasoning
    - ✅ Investment verdict recommendations
    - ✅ Secure API key management

    ---

    ## Setup

    ### Requirements
    - Python 3.7+
    - API Keys (optional):
        - CoinGecko API (free tier available)
        - Bayut API via RapidAPI (free tier available)

    ### Configuration
    1. Install dependencies: `pip install -r requirements.txt`
    2. Add API keys to `secure_config/api_keys.env`
    3. Run: `streamlit run app.py`

    Or use **Demo Mode** to test without API keys!

    ---

    ## Technology Stack

    - **Framework:** Streamlit
    - **Data Processing:** Pandas, NumPy
    - **APIs:** CoinGecko, Bayut (RapidAPI)
    - **Analysis:** Scikit-learn, SciPy
    - **Visualization:** Plotly, Matplotlib

    ---

    ## Security

    - API keys stored in `secure_config/` (gitignored)
    - File permissions: 0o700 (directory), 0o600 (keys)
    - Comprehensive .gitignore prevents accidental commits
    - Environment variables for sensitive data

    ---

    **Version:** 1.0.0
    **License:** Private
    **Repository:** OUVC-valuation-of-crypto-and-real-estate-assets
    """)


def sidebar():
    """Application sidebar"""
    with st.sidebar:
        st.title("Navigation")

        # API Status indicator
        if st.session_state.api_keys_loaded:
            st.success("✅ API Keys Loaded")
        else:
            st.warning("⚠️ No API Keys (Demo Mode Available)")

        st.divider()

        # Page selection
        page = st.radio(
            "Select Module",
            options=[
                "🪙 Crypto Analysis",
                "🏠 Property Analysis",
                "🎮 Demo Mode",
                "ℹ️ About"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        # Footer
        st.markdown("---")
        st.caption("OUVC v1.0.0")
        st.caption("Over/Under Value Checker")

        return page


def main():
    """Main application entry point"""
    # Initialize
    init_session_state()

    # Display header
    display_header()

    # Sidebar navigation
    page = sidebar()

    # Route to appropriate page
    if page == "🪙 Crypto Analysis":
        crypto_analysis_page()
    elif page == "🏠 Property Analysis":
        property_analysis_page()
    elif page == "🎮 Demo Mode":
        demo_mode_page()
    else:
        about_page()


if __name__ == "__main__":
    main()
