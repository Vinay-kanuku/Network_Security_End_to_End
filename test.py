from src.components.gemini import gemini_predict
from src.pipeline.prediction_pipeline import PredictionPipeline

url = input("Enter the URL to analyze: ")

# prediction = gemini_predict(url=url)
# print(f"Prediction for {url}: {prediction}")
ans = PredictionPipeline().run_prediction_pipeline(url=url)
print(ans)
