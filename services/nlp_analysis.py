import logging
from transformers import pipeline
import spacy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeverityAnalyzer:
    def __init__(self):
        self.nlp = None
        self.classifier = None
        self.initialize_models()

    def initialize_models(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                
                device=-1
            )
            logger.info("NLP models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def classify_severity(self, text):
        try:
            # print(text)
            logger.info(f"Analyzing text: {text}")  # Limit log length
            # print(text[:100])
            system="You are an AI model trained to classify incidents related to women's safety based on the severity of the report. Your task is to analyze the provided text and assign an appropriate category and severity level based on predefined criteria. You should be able to identify and categorize incidents such as harassment, abuse, assault, and discrimination. Your responses should be clear, concise, and empathetic, providing support and guidance to the user. If you are unsure about the severity level or category, you can ask for more information or escalate the issue to a human moderator for further review. Remember to maintain a professional and respectful tone in all interactions."
            text_sys=f"{system} {text}"
            sentiment = self.classifier(text_sys)[0]
            # print(sentiment)


            logger.info(f" Sentiment result:  {sentiment} ")

            
            
            text_lower = text.lower()
            # has_severity_terms = any(word in text_lower for word in severity_keywords)

            # logger.info(f"Severity Terms Found: {has_severity_terms}")

            if  (sentiment['score'] > 0.75):
                return "HIGH"
            else:
                return "LOW"

        except Exception as e:
            logger.error(f"Error in severity classification: {e}")
            raise

analyzer = SeverityAnalyzer()
