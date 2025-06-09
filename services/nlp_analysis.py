import logging
from transformers import pipeline
import spacy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeverityAnalyzer:
    def __init__(self):
        self.nlp = None
        self.classifier = None

    def initialize_models(self):
        try:
            if self.nlp is None:
                self.nlp = spacy.load("en_core_web_sm")
            if self.classifier is None:
                self.classifier = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1  # CPU
                )
            logger.info("NLP models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def classify_severity(self, text):
        try:
            self.initialize_models()

            logger.info(f"Analyzing text: {text[:100]}...")  # limit log length

            system_prompt = (
                "You are an AI model trained to classify incidents related to women's safety based on the severity "
                "of the report. Your task is to analyze the provided text and assign an appropriate category and "
                "severity level. You should be able to identify incidents such as harassment, abuse, assault, "
                "and discrimination."
            )
            text_sys = f"{system_prompt} {text}"
            sentiment = self.classifier(text_sys)[0]

            logger.info(f"Sentiment result: {sentiment}")

            if sentiment['score'] > 0.75:
                return "HIGH"
            else:
                return "LOW"

        except Exception as e:
            logger.error(f"Error in severity classification: {e}")
            raise

# Instantiate only when needed in routes
analyzer = SeverityAnalyzer()
