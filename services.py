"""Business logic for translation, vocabulary analysis, and AI processing."""

import os
import re
import logging
from typing import Any, Dict, List, Set
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator
import google.generativeai as genai
from dotenv import load_dotenv
from config import KNOWN_WORDS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
translator = GoogleTranslator(source='en', target='az')
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class TextAnalysisService:
    """Service for analyzing Security+ technical text."""
    
    def __init__(self):
        self.known_words: Set[str] = KNOWN_WORDS
        # Use gemini-2.5-flash - newest, fastest, and free
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    
    def translate_to_azerbaijani(self, text: str) -> str:
        """
        Translate English text to Azerbaijani using FREE deep-translator.
        
        Args:
            text: English text to translate
            
        Returns:
            Translated Azerbaijani text
            
        Raises:
            Exception: If translation fails
        """
        try:
            result = translator.translate(text)
            return result
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise Exception(f"Translation failed: {str(e)}")
    
    def extract_unknown_words(self, text: str) -> List[str]:
        """
        Extract words not in the known_words hashmap.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of unknown words (unique, lowercase)
        """
        # Clean and tokenize text
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter unknown words (not in hashmap) - now much fewer!
        unknown = [word for word in set(words) if word not in self.known_words]
        
        return sorted(unknown)
    
    def generate_ai_analysis(self, text: str, unknown_words: List[str]) -> Dict[str, Any]:
        """
        Use FREE Gemini API to generate definitions for unknown terms and summary.
        OPTIMIZED: Shorter prompt, only unknown terms
        
        Args:
            text: Original Security+ text
            unknown_words: List of unknown technical words (not in hashmap)
            
        Returns:
            Dictionary with vocabulary_list and mini_note
            
        Raises:
            Exception: If AI generation fails
        """
        try:
            # Shorter, optimized prompt for speed
            prompt = f"""Security+ text: {text}

Unknown terms: {', '.join(unknown_words[:10])}  

Provide ONLY valid JSON (no markdown, no explanation):
{{
    "vocabulary": [{{"word": "term", "definition": "Azərbaycan izahı"}}],
    "mini_note": "Qısa Azərbaycan xülasəsi"
}}"""
            
            # Call FREE Gemini API with optimized settings
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=800,
                )
            )
            
            response_text = response.text.strip()
            logger.info(f"Gemini raw response: {response_text[:200]}...")
            
            # Try to extract JSON from various formats
            json_text = response_text
            
            # Remove markdown code blocks if present
            if '```json' in response_text:
                json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1).strip()
            elif '```' in response_text:
                json_match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1).strip()
            
            # Find JSON object in text
            json_match = re.search(r'\{.*\}', json_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
            
            # Parse the response
            import json
            parsed_response = json.loads(json_text)
            
            return {
                "vocabulary_list": [
                    {"word": item.get("word", ""), "a2_definition": item.get("definition", "")}
                    for item in parsed_response.get("vocabulary", [])
                ],
                "mini_note": parsed_response.get("mini_note", "Texniki xülasə mövcud deyil")
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}. Response: {response_text[:500]}")
            # Return fallback response
            return {
                "vocabulary_list": [
                    {"word": word, "a2_definition": f"{word} - texniki termin"}
                    for word in unknown_words[:5]
                ],
                "mini_note": "Texniki mətn Security+ mövzusunda təhlükəsizlik konsepsiyalarını izah edir."
            }
        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Complete analysis pipeline for Security+ text.
        OPTIMIZED: Parallel execution for speed
        
        Args:
            text: Input Security+ technical text
            
        Returns:
            Complete analysis results
        """
        # Step 1 & 2: Run translation and word extraction in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            translation_future = executor.submit(self.translate_to_azerbaijani, text)
            words_future = executor.submit(self.extract_unknown_words, text)
            
            az_translation = translation_future.result()
            unknown_words = words_future.result()
        
        # Step 3: Generate AI analysis (only if there are unknown words)
        if unknown_words:
            ai_analysis = self.generate_ai_analysis(text, unknown_words)
        else:
            ai_analysis = {
                "vocabulary_list": [],
                "mini_note": "Bütün sözlər məlumdur. Əla!"
            }
        
        # Step 4: Compile results
        return {
            "original_text": text,
            "az_translation": az_translation,
            "vocabulary_list": ai_analysis["vocabulary_list"],
            "security_plus_mini_note": ai_analysis["mini_note"],
            "unknown_words_count": len(unknown_words)
        }


# Singleton instance
text_analysis_service = TextAnalysisService()
