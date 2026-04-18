import google.generativeai as genai
from config import GEMINI_API_KEY
from models.insight_model import Insight
import json
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

def generate_insights(prompt: str) -> list[Insight]:
    """Chama Gemini UMA ÚNICA VEZ e retorna insights"""
    try:
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
        response = model.generate_content(prompt)
        
        # Extrai o texto da resposta
        response_text = response.text.strip()
        
        # Tenta parsear como JSON
        try:
            # Remove possíveis markdown code blocks
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            insights_data = json.loads(response_text)
            
            # Converte para lista de Insight objects
            insights = []
            for item in insights_data:
                try:
                    insight = Insight(**item)
                    insights.append(insight)
                except Exception as e:
                    logger.warning(f"Erro validando insight: {e}")
                    continue
            
            return insights
        
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON da IA: {e}")
            logger.error(f"Resposta recebida: {response_text}")
            return []
    
    except Exception as e:
        logger.error(f"Erro chamando Gemini: {e}")
        return []
