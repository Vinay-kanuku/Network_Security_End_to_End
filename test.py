from src.components.gemini import gemini_predict
url = input("Enter the URL to analyze: ")

prediction = gemini_predict(url=url)
print(f"Prediction for {url}: {prediction}")
