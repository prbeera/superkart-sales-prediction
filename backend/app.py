
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

app = Flask(__name__)

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "SuperKart_prediction_model_v1_0.joblib"
)

model = joblib.load(MODEL_PATH)


categorical_features = [
    "Product_Sugar_Content",
    "Product_Type",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Store_Id"
]


def preprocess_input(input_df):

    input_df["Product_Sugar_Content"] = (
        input_df["Product_Sugar_Content"]
        .replace({"reg": "Regular"})
    )

    reference_year = 2025

    input_df["Store_Age"] = (
        reference_year -
        input_df["Store_Establishment_Year"]
    )

    input_df.drop(
        columns=["Store_Establishment_Year"],
        inplace=True
    )

    input_df = pd.get_dummies(
        input_df,
        columns=categorical_features,
        drop_first=True
    )

    if "Product_Id" in input_df.columns:
        input_df.drop(
            columns=["Product_Id"],
            inplace=True
        )

    model_features = model.feature_names_in_

    input_df = input_df.reindex(
        columns=model_features,
        fill_value=0
    )

    return input_df


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "SuperKart Sales Prediction API is running",
        "status": "healthy"
    })


@app.route("/v1/sales", methods=["POST"])
def predict_sales():

    try:

        data = request.get_json()

        if data is None:
            return jsonify({
                "error": "Request body must contain JSON data."
            }), 400

        input_df = pd.DataFrame([data])

        processed_input = preprocess_input(
            input_df
        )

        prediction = model.predict(
            processed_input
        )[0]

        return jsonify({
            "Predicted Sales": round(
                float(prediction), 2
            )
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/v1/salesbatch", methods=["POST"])
def predict_sales_batch():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "CSV file is required."
            }), 400

        file = request.files["file"]

        input_df = pd.read_csv(file)

        output_df = input_df.copy()

        processed_input = preprocess_input(
            input_df.copy()
        )

        predictions = model.predict(
            processed_input
        )

        output_df["Predicted Sales"] = np.round(
            predictions,
            2
        )

        return jsonify(
            output_df.to_dict(
                orient="records"
            )
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=7860
    )
