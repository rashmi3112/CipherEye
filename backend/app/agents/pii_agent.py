import logging
from typing import List, Dict, Any
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from app.models.schemas import DetectedPII
from app.core.config import settings

logger = logging.getLogger(__name__)

class PIIAgent:
    """
    The PII Agent is responsible for identifying and masking Personally Identifiable Information.
    Instead of calling an LLM (which is slow for simple PII and costs tokens), it uses
    Microsoft Presidio for fast, offline NLP-based PII detection.
    """
    def __init__(self):
        self.enabled = settings.enable_pii_detection
        if self.enabled:
            logger.info("Initializing Presidio Analyzer & Anonymizer...")
            # Note: In a production app, this loading step is heavy and should be done once
            # at startup rather than per-request. Since this is the agent init, we instantiate it once.
            try:
                # Self-healing: auto-download spaCy model if missing
                try:
                    import spacy
                    if not spacy.util.is_package("en_core_web_sm"):
                        logger.info("spaCy model 'en_core_web_sm' not found. Downloading...")
                        from spacy.cli import download
                        download("en_core_web_sm")
                except Exception as spacy_err:
                    logger.error(f"Error checking or downloading spaCy model: {spacy_err}")

                from presidio_analyzer.nlp_engine import NlpEngineProvider
                configuration = {
                    "nlp_engine_name": "spacy",
                    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
                }
                provider = NlpEngineProvider(nlp_configuration=configuration)
                nlp_engine = provider.create_engine()
                self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
                self.anonymizer = AnonymizerEngine()
            except Exception as e:
                logger.error(f"Failed to load Presidio engines. Disabling PII Agent. {e}")
                self.enabled = False
        
    def analyze_and_mask(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the text for PII and returns the masked text along with what was found.
        """
        if not self.enabled or not text:
            return {"masked_text": text, "detected_pii": []}
            
        try:
            # Detect PII
            results = self.analyzer.analyze(text=text, language='en')
            
            # Extract detected PII metadata
            detected_pii_list = []
            for result in results:
                detected_pii_list.append(
                    DetectedPII(
                        entity_type=result.entity_type,
                        start=result.start,
                        end=result.end,
                        replacement=f"<{result.entity_type}>"
                    )
                )
            
            # Anonymize (Mask)
            # By default, Presidio replaces with <ENTITY_TYPE>
            anonymized_result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=results
            )
            
            return {
                "masked_text": anonymized_result.text,
                "detected_pii": detected_pii_list
            }
        except Exception as e:
            logger.error(f"PII Analysis failed: {e}")
            # Failsafe: return original text if detection fails
            return {"masked_text": text, "detected_pii": []}
