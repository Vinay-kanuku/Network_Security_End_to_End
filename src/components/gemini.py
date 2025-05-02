import google.generativeai as genai 
from utils.phishing_features import get_features
import os 
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
 
def gemini_predict(url: str):
    """
    Gemini model returns 1 for legitimate, 0 for phishing — raw binary output only.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = (
        f"Classify the following URL strictly as phishing or legitimate.\n"
        f"Return only one number: 0 (phishing) or 1 (legitimate).\n"
        f"No explanation, no punctuation, no extra words.\n\n"
        f"URL: {url}"
    )
    res = model.generate_content(prompt)
    return res.text.strip()[0]
 


if __name__ == "__main__":
    url = input("Enter the URL to analyze: ")
    prediction = gemini_predict(url)
    print(f"Prediction for {url}: {prediction}")

