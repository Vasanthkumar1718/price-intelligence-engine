# ⚡ Automated Competitor Price Intelligence & Market Simulator

An end-to-end data pipeline and predictive analytics application that harvests live e-commerce catalog data, persists structured records into an SQL database, trains regression models on pricing drivers, and delivers an interactive decision-support dashboard for business stakeholders.

---

## 📌 Key Architectural Highlights
* **Automated Data Harvesting**: Crawls multi-page catalog listings from a live web application using `BeautifulSoup` and `requests`.
* **Structured Ingestion & Validation**: Cleans raw HTML text, strips currency notations via regex, imputes missing values, and loads normalized records into a relational `SQLite` database.
* **Predictive Pricing Engine**: Trains a `RandomForestRegressor` via `scikit-learn` to identify pricing elasticity based on product review scores and inventory availability.
* **Interactive Control Center**: Deploys an executive-ready `Streamlit` and `Plotly` dashboard featuring catalog KPIs, dynamic distribution charts, and a real-time price simulation engine.

---

## 🛠️ Tech Stack
* **Language**: Python 3.12
* **Web Scraping & Ingestion**: `requests`, `beautifulsoup4`
* **Data Processing & Database**: `pandas`, `sqlite3`
* **Machine Learning**: `scikit-learn` (Random Forest), `joblib`
* **Visualization & UI**: `streamlit`, `plotly`

---

## 🔄 End-to-End System Workflow

```
[ Live Web Source: books.toscrape.com ]
                 │
                 ▼ (requests + BeautifulSoup)
         [ pipeline.py ]  ──▶  Parses HTML, cleans text, validates types
                 │
                 ▼ (sqlite3)
      [ ecommerce_data.db ]  ──▶  Stores structured product records
                 │
                 ▼ (pandas + scikit-learn)
          [ model.py ]   ──▶  Trains Random Forest model & saves .pkl artifacts
                 │
                 ▼
       [ Streamlit (app.py) ]
       ├── Control Center: Multi-attribute sidebar filtering
       ├── Tab 1: Live Market Analytics & Plotly Visualizations
       └── Tab 2: Predictive Pricing Simulator with Confidence Corridors
```

---

## ⚙️ Local Installation & Execution

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Vasanthkumar1718/price-intelligence-engine.git](https://github.com/Vasanthkumar1718/price-intelligence-engine.git)
   cd price-intelligence-engine
   ```

2. **Set up virtual environment & install dependencies**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   # source .venv/bin/activate  # On macOS / Linux
   pip install -r requirements.txt
   ```

3. **Execute the pipeline in sequence**:
   ```bash
   python pipeline.py       # Scrapes live web listings & populates SQLite DB
   python model.py          # Trains pricing model & serializes model artifacts
   streamlit run app.py     # Launches the interactive web dashboard
   ```

---

## 📊 Live Application Features

* **Control Center**: Dynamic sidebar filtering by star rating and price thresholds with single-click pipeline synchronization.
* **Market Analytics Tab**: Executive KPI summary cards (Tracked Catalog, Average Price, Median Price, Stock Rate), dynamic price distribution histograms, and price-to-rating trends rendered via Plotly.
* **Predictive Pricing Simulator**: Live inference using the trained Random Forest model with dynamic confidence corridor bands.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).