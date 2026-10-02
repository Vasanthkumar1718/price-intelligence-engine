import sqlite3
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def train_pricing_model():
    print("Step 1: Reading scraped records from SQLite...")
    conn = sqlite3.connect("ecommerce_data.db")
    df = pd.read_sql("SELECT rating, in_stock, price FROM products", conn)
    conn.close()

    # Features (X) and Target (y)
    X = df[["rating", "in_stock"]]
    y = df["price"]

    # Split: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Step 2: Training Random Forest Regressor on {len(X_train)} samples...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate predictions
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    print("Step 3: Model Evaluation:")
    print(f" - R² Score: {r2:.3f}")
    print(f" - Mean Absolute Error (MAE): £{mae:.2f}")

    # Save model and column features
    joblib.dump(model, "price_model.pkl")
    joblib.dump(list(X.columns), "model_columns.pkl")
    print("Saved 'price_model.pkl' and 'model_columns.pkl' successfully!")

if __name__ == "__main__":
    train_pricing_model()