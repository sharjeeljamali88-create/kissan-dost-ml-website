# Kisan Dost — Complete ML Website Project

A responsive HTML/CSS/JavaScript website, reproducible Python machine learning training, real historical crop data, supplied expense and guide datasets, trained model coefficients, evaluation results, and an optional FastAPI backend. No React required.

## Run the website on Windows (easiest)

1. Extract the entire ZIP folder.
2. Install Python 3.11, 3.12 or 3.13 if necessary.
3. Double-click START_WINDOWS.bat. Keep the terminal open.
4. Open http://127.0.0.1:8000 if the browser does not open automatically.
5. Stop with Ctrl+C. No package installation is needed for this mode. Do not open index.html directly: the JSON files need a local server.

Or run `python server.py` in the project folder on Windows, macOS or Linux.

## Use the website

- Choose wheat, cotton, or sugarcane; enter acreage, farm label and district.
- Enter your local selling rate in PKR per 40 kg maund. Initial price is 0 deliberately; no current market rate is invented.
- Edit all cost items and select optional expenses. The cost reference includes some older or estimated values; verify locally.
- Enter your own expected yield, or apply the national ML forecast for wheat/sugarcane.
- Cotton ML data measures lint. The profit planner measures seed cotton, so applying a lint forecast to this plan is intentionally disabled.
- Save plans locally in the browser, reopen them, or export CSV. Saved plans are device/browser-specific; there are no cloud accounts.
- Read the Crop Guide; filter by crop and search for a topic.
- Open Yield Forecast and Model & Data for sources and actual backtest errors.

## What is actually machine learning?

`train.py` fits a scikit-learn StandardScaler + Ridge(alpha=10) pipeline independently for each crop. Features are fiscal end-year (minus 2010) and previous year's observed yield. The target is next annual national crop yield in kg/ha. The final models train on 14 transitions each. `dist/model.json` contains their fitted parameters and full evaluation history. `dist/engine.js` runs the exact learned linear model in the browser, so the hosted static website needs no separate Python server and is not a random simulator.

Five expanding-window, one-step backtests use FY 2020–21 through 2024–25. Each model and standardiser is fit using earlier years only. Alpha is fixed, not selected on test results. Baseline: predict the previous observed yield. The final model then refits using all available data. No weather/soil/management effects or district effects are claimed.

## Real data and limits

`data/pakistan_yield_history.csv`: 45 observations (15 years × 3 crops), transcribed from the official Pakistan Economic Survey 2024–25, Agriculture, Table 2.5 (printed p. 33), source Pakistan Bureau of Statistics:
https://finance.gov.pk/survey/chapter_25/2_Agriculture.pdf

This is a deliberately fixed 2024–25 data vintage. FY 2024–25 is provisional. The single forecast is FY 2025–26 (fiscal end-year 2026), not a claim to use the latest available statistics. No synthetic observations were created. Cotton is kg of lint/ha; wheat and sugarcane are harvested crop kg/ha. Unit conversion: 1 acre = 0.40468564224 ha; 1 maund = 40 kg.

The supplied 81 expense rows and 37 crop guide rows are preserved in backend CSVs and website reference.json. These are reference assumptions, not independent farm observations, and are never used as yield training labels. Their links and statuses come from the supplied files and have not all been independently verified.

Small-data educational model: it is not validated for Sindh districts or individual farms, does not forecast prices or costs, and has no guaranteed accuracy. Wheat ML has higher backtest error than the naive baseline; this is displayed honestly. Profit is transparent arithmetic using the chosen yield and user-entered prices/costs, not a separate ML target. No calibrated confidence interval is presented.

## Retrain

Use a virtual environment if desired:

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python train.py
```

On macOS/Linux use `source .venv/bin/activate`. Or double-click RETRAIN_WINDOWS.bat with Python available as `python`. The models and metrics are regenerated in dist/model.json and backend/model.json. Keep this benchmark dataset's years 2011–2025; the training script intentionally forecasts 2026. For a newer vintage, update the forecast horizon and UI labels together. Record source provenance and validate new observations before extending the dataset.

## Optional Python API

The original FastAPI calculation, crop guide and weather routes are retained. New `/api/model` and `/api/predict?crop=Wheat` routes expose the trained model. To run:

```
python -m pip install -r requirements.txt
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 for the same website and http://127.0.0.1:8000/docs for the API. The original Flutter app can continue using `/api/crops`, `/api/crop/{crop}`, `/api/calculate`, and `/api/weather`. Weather requires internet; the website itself does not depend on weather service access. For Android emulator API access, bind to 0.0.0.0 in your trusted development network and use 10.0.2.2:8000 as the Flutter base URL. No Android APK is included.

`original_flutter/` retains the submitted Dart files and configuration for reference. The original archive did not include generated platform folders (android/web/ios); recreate them with `flutter create .` in a separate working copy if rebuilding the mobile app.

## Verify

```
node tests/engine.test.js
python tests/test_backend.py
```

Training dependencies are only needed for retraining; the normal website runs with Python's standard library. Optional Google Fonts need internet; system fonts are the fallback. All charts, forecasts and guides work with bundled data.

## Files

- dist/: complete deployable website and bundled model/data
- data/: historical national yield dataset
- train.py: model training and chronological evaluation
- backend/: original API extended with trained yield inference and website serving
- server.py / START_WINDOWS.bat: dependency-free website launch
- requirements.txt: training/API dependencies
- tests/: model consistency and API/calculation checks
- original_flutter/: supplied mobile project source
