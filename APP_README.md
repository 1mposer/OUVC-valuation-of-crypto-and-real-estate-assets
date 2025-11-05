# OUVC Streamlit Web Application

## Overview

This is the **Streamlit web interface** for the OUVC (Over/Under Value Checker) tool. It provides a user-friendly web-based interface for analyzing cryptocurrency and Dubai real estate valuations.

## Features

### 🪙 Cryptocurrency Analysis
- Interactive form for crypto selection
- Live data fetching from CoinGecko API (optional)
- Manual data entry option
- 60-Second Undervalued Test algorithm
- Investment verdicts (STRONG BUY, BUY, HOLD, AVOID)
- Detailed metrics and reasoning

### 🏠 Dubai Property Analysis
- Property search by area, type, bedrooms, size
- Live data from Bayut API (optional)
- Comparable property analysis
- Valuation estimates with ±10% confidence range
- Rental yield calculations
- Investment recommendations

### 🎮 Demo Mode
- Try the tool without API keys
- Pre-loaded sample data for both modules
- Great for testing and demonstrations

### ℹ️ About Page
- Complete documentation
- Setup instructions
- Technology stack information
- Security features

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)

Create `secure_config/api_keys.env` with your API keys:

```
COINGECKO_API_KEY=your_coingecko_key_here
BAYUT_API_KEY=your_bayut_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
```

**Note:** API keys are optional. You can use Demo Mode without them!

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### With API Keys
1. Configure your API keys in `secure_config/api_keys.env`
2. Run the app
3. Select "Crypto Analysis" or "Property Analysis"
4. Enable "Use API" checkbox
5. Fill in the form and click "Analyze"

### Without API Keys (Demo Mode)
1. Run the app
2. Select "Demo Mode"
3. Choose either Crypto or Property demo
4. Click the demo button to see results

### Manual Data Entry
1. Select "Crypto Analysis" or "Property Analysis"
2. Uncheck "Use API" checkbox
3. Enter all required data manually
4. Click "Analyze"

## Application Structure

```
app.py                          # Main Streamlit application
├── init_session_state()        # Initialize app state
├── display_header()            # App header
├── crypto_analysis_page()      # Crypto module UI
├── property_analysis_page()    # Property module UI
├── demo_mode_page()            # Demo mode UI
├── about_page()                # About/documentation
├── sidebar()                   # Navigation sidebar
└── main()                      # Entry point
```

## Navigation

Use the **sidebar** to navigate between:
- 🪙 Crypto Analysis
- 🏠 Property Analysis
- 🎮 Demo Mode
- ℹ️ About

## API Status

The sidebar shows your API key status:
- ✅ **API Keys Loaded** - API features available
- ⚠️ **No API Keys** - Demo Mode available

## Technology Stack

- **Framework:** Streamlit (web interface)
- **Backend:** Python 3.7+
- **Data Processing:** Pandas, NumPy
- **APIs:** CoinGecko, Bayut (RapidAPI)
- **Analysis:** Scikit-learn, SciPy
- **Visualization:** Plotly, Matplotlib

## Troubleshooting

### Import Errors
If you get import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Errors
- Check that your API keys are correctly configured
- Verify API key validity at provider websites
- Try Demo Mode as an alternative

### Module Not Found
Ensure you're running from the project root directory:
```bash
cd /path/to/OUVC-valuation-of-crypto-and-real-estate-assets
streamlit run app.py
```

## Comparison with CLI

| Feature | CLI (main.py) | Web App (app.py) |
|---------|---------------|------------------|
| Interface | Command-line | Web browser |
| Navigation | Menu-driven | Sidebar |
| Data Entry | Text input | Forms/widgets |
| Results Display | Text output | Formatted cards |
| Demo Mode | ✅ | ✅ |
| API Integration | ✅ | ✅ |
| Best For | Automation, scripts | Interactive use, demos |

## Security

- API keys stored in gitignored `secure_config/` directory
- File permissions: 0o700 (directory), 0o600 (keys)
- No API keys required for Demo Mode
- Environment variables for sensitive data

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. (Optional) Configure API keys
3. Run: `streamlit run app.py`
4. Try Demo Mode first
5. Then try live analysis with your data

## Support

For issues or questions:
- Check the **About** page in the app
- Review `QUICK_REFERENCE.md`
- Check `SECURITY_SETUP_COMPLETE.md`

---

**Version:** 1.0.0
**Created:** 2025-11-03
**Interface Type:** Streamlit Web Application
