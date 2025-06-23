#!/usr/bin/env python3
"""
Gemini API integration for scene content analysis.
"""

import json
import logging
import os
import requests
from typing import Dict, List, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini_integration")

class GeminiAnalyzer:
    """Class for analyzing scene content using Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        """Initialize the Gemini analyzer.
        
        Args:
            api_key: Gemini API key
            model: Gemini model to use
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("No Gemini API key provided. Set GEMINI_API_KEY env variable.")
        
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
        logger.info(f"Initialized Gemini analyzer with model: {model}")
    
    def analyze_dialogue_consistency(self, character: str, current_dialogue: str, 
                                   previous_dialogues: List[str]) -> Dict:
        """Analyze dialogue consistency for a character.
        
        Args:
            character: Character name
            current_dialogue: Current dialogue to analyze
            previous_dialogues: List of previous dialogues by the same character
            
        Returns:
            Dict containing analysis results
        """
        prompt = self._create_dialogue_prompt(character, current_dialogue, previous_dialogues)
        response = self._call_gemini_api(prompt)
        
        return self._parse_dialogue_analysis(response)
    
    def analyze_emotional_continuity(self, character: str, current_emotion: str,
                                   previous_emotions: List[Dict]) -> Dict:
        """Analyze emotional continuity for a character.
        
        Args:
            character: Character name
            current_emotion: Current emotion to analyze
            previous_emotions: List of previous emotions by the same character
            
        Returns:
            Dict containing analysis results
        """
        prompt = self._create_emotion_prompt(character, current_emotion, previous_emotions)
        response = self._call_gemini_api(prompt)
        
        return self._parse_emotion_analysis(response)
    
    def analyze_scene_narrative(self, scene_description: str, 
                              previous_scenes: List[Dict]) -> Dict:
        """Analyze narrative coherence of a scene.
        
        Args:
            scene_description: Current scene description
            previous_scenes: List of previous scene descriptions
            
        Returns:
            Dict containing analysis results
        """
        prompt = self._create_narrative_prompt(scene_description, previous_scenes)
        response = self._call_gemini_api(prompt)
        
        return self._parse_narrative_analysis(response)
    
    def _create_dialogue_prompt(self, character: str, current_dialogue: str,
                              previous_dialogues: List[str]) -> str:
        """Create prompt for dialogue consistency analysis.
        
        Args:
            character: Character name
            current_dialogue: Current dialogue to analyze
            previous_dialogues: List of previous dialogues by the same character
            
        Returns:
            Formatted prompt string
        """
        previous_samples = "\\n".join([f"- {d}" for d in previous_dialogues[-5:]])
        
        return f"""
        As an expert in screenplay analysis, assess the dialogue consistency for the character {character}.
        
        Previous dialogue examples:
        {previous_samples}
        
        Current dialogue:
        "{current_dialogue}"
        
        Please analyze if the current dialogue is consistent with the character's established voice, vocabulary, speech patterns, and personality traits.
        
        Provide your analysis in JSON format with the following structure:
        {{
            "is_consistent": true/false,
            "confidence_score": (float between 0-1),
            "inconsistency_reasons": ["reason1", "reason2"],
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
    
    def _create_emotion_prompt(self, character: str, current_emotion: str,
                             previous_emotions: List[Dict]) -> str:
        """Create prompt for emotional continuity analysis.
        
        Args:
            character: Character name
            current_emotion: Current emotion to analyze
            previous_emotions: List of previous emotions by the same character
            
        Returns:
            Formatted prompt string
        """
        emotion_history = "\\n".join([
            f"- Scene {e.get('scene_id', 'unknown')}: {e.get('emotion')} - Context: {e.get('context', 'N/A')}"
            for e in previous_emotions[-5:]
        ])
        
        return f"""
        As an expert in character psychology and narrative continuity, assess the emotional continuity for the character {character}.
        
        Previous emotional states:
        {emotion_history}
        
        Current emotional state:
        "{current_emotion}"
        
        Please analyze if the current emotional state is consistent with the character's emotional arc and if the transition from previous emotions is plausible.
        
        Provide your analysis in JSON format with the following structure:
        {{
            "is_consistent": true/false,
            "confidence_score": (float between 0-1),
            "inconsistency_reasons": ["reason1", "reason2"],
            "justification": "explanation of your reasoning",
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
    
    def _create_narrative_prompt(self, scene_description: str, 
                               previous_scenes: List[Dict]) -> str:
        """Create prompt for narrative coherence analysis.
        
        Args:
            scene_description: Current scene description
            previous_scenes: List of previous scene descriptions
            
        Returns:
            Formatted prompt string
        """
        scene_history = "\\n".join([
            f"- Scene {s.get('scene_id', 'unknown')}: {s.get('brief_description', 'N/A')}"
            for s in previous_scenes[-5:]
        ])
        
        return f"""
        As an expert in narrative structure and screenplay analysis, assess the narrative coherence of the following scene.
        
        Previous scenes:
        {scene_history}
        
        Current scene:
        "{scene_description}"
        
        Please analyze if the current scene maintains narrative coherence with the established story. Consider plot progression, character motivations, and logical continuity.
        
        Provide your analysis in JSON format with the following structure:
        {{
            "is_coherent": true/false,
            "confidence_score": (float between 0-1),
            "coherence_issues": ["issue1", "issue2"],
            "plot_continuity_score": (float between 0-1),
            "character_motivation_score": (float between 0-1),
            "logical_consistency_score": (float between 0-1),
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Call Gemini API with a prompt.
        
        Args:
            prompt: Prompt to send to the API
            
        Returns:
            Dict containing API response
        """
        if not self.api_key:
            logger.error("Cannot call Gemini API: No API key provided")
            return {"error": "No API key provided"}
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.8,
                "topK": 40,
                "maxOutputTokens": 1024
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}:generateContent?key={self.api_key}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Gemini API: {e}")
            return {"error": str(e)}
    
    def _parse_dialogue_analysis(self, response: Dict) -> Dict:
        """Parse dialogue analysis response from Gemini.
        
        Args:
            response: Raw API response
            
        Returns:
            Dict containing structured analysis
        """
        try:
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            content = response.get("candidates", [{}])[0].get("content", {})
            text = content.get("parts", [{}])[0].get("text", "")
            
            # Extract JSON from the response
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                analysis = json.loads(json_str)
                analysis["success"] = True
                return analysis
            else:
                return {
                    "success": False,
                    "error": "Could not extract JSON from response",
                    "raw_response": text
                }
        except Exception as e:
            logger.error(f"Error parsing dialogue analysis: {e}")
            return {"success": False, "error": str(e), "raw_response": response}
    
    def _parse_emotion_analysis(self, response: Dict) -> Dict:
        """Parse emotion analysis response from Gemini.
        
        Args:
            response: Raw API response
            
        Returns:
            Dict containing structured analysis
        """
        # Similar implementation to _parse_dialogue_analysis
        return self._parse_dialogue_analysis(response)
    
    def _parse_narrative_analysis(self, response: Dict) -> Dict:
        """Parse narrative analysis response from Gemini.
        
        Args:
            response: Raw API response
            
        Returns:
            Dict containing structured analysis
        """
        # Similar implementation to _parse_dialogue_analysis
        return self._parse_dialogue_analysis(response)


if __name__ == "__main__":
    # Example usage
    analyzer = GeminiAnalyzer()
    
    character = "John"
    current_dialogue = "I've never cared about the stock market before."
    previous_dialogues = [
        "Have you seen the news today?",
        "The stock market crashed overnight.",
        "This could affect our investment strategy."
    ]
    
    result = analyzer.analyze_dialogue_consistency(character, current_dialogue, previous_dialogues)
    print(json.dumps(result, indent=2))