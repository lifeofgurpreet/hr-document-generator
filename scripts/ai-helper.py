#!/usr/bin/env python3
"""
AI Helper for HR Document Generation
Integrates with OpenAI API to generate personalized content
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIHelper:
    """AI-powered content generation helper for HR documents"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI helper with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Load AI prompts configuration
        try:
            with open('config/ai-prompts.json', 'r') as f:
                self.prompts = json.load(f)
        except FileNotFoundError:
            # Fallback prompts if file not found
            self.prompts = {
                "contract_generation": {
                    "job_description": "Generate a detailed job description for a {role} position."
                },
                "roles_responsibilities": {
                    "kpi_breakdown": "Create KPI activities for {kpi_breakdown}."
                },
                "content_improvement": {
                    "professional_tone": "Improve the professional tone."
                },
                "validation": {
                    "legal_compliance": "Review for legal compliance."
                }
            }
    
    def generate_job_description(self, role: str, team: str, career_level: str, 
                                company_name: str, responsibilities: List[str]) -> str:
        """Generate a detailed job description using AI"""
        prompt = self.prompts['contract_generation']['job_description'].format(
            role=role,
            team=team,
            company_name=company_name,
            responsibilities=', '.join(responsibilities)
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an HR professional specializing in creating clear, professional job descriptions. Focus on practical, actionable responsibilities that align with the company's mission."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating job description: {e}")
            return self._get_fallback_job_description(role, team, career_level)
    
    def generate_kpi_activities(self, kpi_area: str, percentage: int, career_level: str) -> str:
        """Generate specific activities for KPI areas"""
        prompt = self.prompts['roles_responsibilities']['kpi_breakdown'].format(
            kpi_breakdown=f"{kpi_area}: {percentage}%"
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an HR professional creating specific, measurable KPI activities. Focus on actionable items that employees can track and achieve."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating KPI activities: {e}")
            return self._get_fallback_kpi_activities(kpi_area, percentage)
    
    def enhance_content(self, content: str, enhancement_type: str = "professional_tone") -> str:
        """Enhance existing content using AI"""
        if enhancement_type not in self.prompts['content_improvement']:
            return content
        
        prompt = self.prompts['content_improvement'][enhancement_type]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional document editor. Improve the given content while maintaining its formal and legal nature."},
                    {"role": "user", "content": f"{prompt}\n\nContent to enhance:\n{content}"}
                ],
                max_tokens=1000,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error enhancing content: {e}")
            return content
    
    def validate_document(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Validate document completeness and compliance"""
        if document_type not in self.prompts['validation']:
            return {"valid": True, "issues": [], "suggestions": []}
        
        prompt = self.prompts['validation'][document_type]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a legal and HR compliance expert. Review documents for completeness, clarity, and legal compliance."},
                    {"role": "user", "content": f"{prompt}\n\nDocument to review:\n{document_content}"}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            # Parse the response to extract validation results
            validation_text = response.choices[0].message.content.strip()
            
            # Simple parsing - in production, you might want more sophisticated parsing
            issues = []
            suggestions = []
            
            if "missing" in validation_text.lower() or "incomplete" in validation_text.lower():
                issues.append("Document may be incomplete")
            
            if "suggestion" in validation_text.lower():
                suggestions.append(validation_text)
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "suggestions": suggestions,
                "review_text": validation_text
            }
        except Exception as e:
            logger.error(f"Error validating document: {e}")
            return {"valid": True, "issues": [], "suggestions": [], "error": str(e)}
    
    def generate_personalized_content(self, template_content: str, employee_data: Dict[str, Any]) -> str:
        """Generate personalized content based on employee data"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an HR professional creating personalized content. Adapt the template content to be specific to the employee while maintaining professionalism."},
                    {"role": "user", "content": f"Personalize this content for {employee_data.get('name', 'the employee')}:\n\n{template_content}"}
                ],
                max_tokens=1000,
                temperature=0.6
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating personalized content: {e}")
            return template_content
    
    def _get_fallback_job_description(self, role: str, team: str, career_level: str) -> str:
        """Fallback job description when AI generation fails"""
        return f"The Employee will perform duties as a {role} in the {team} team at the {career_level} level. Responsibilities include supporting team objectives, contributing to project delivery, and maintaining professional standards."
    
    def _get_fallback_kpi_activities(self, kpi_area: str, percentage: int) -> str:
        """Fallback KPI activities when AI generation fails"""
        activities = {
            "Vision (VIS)": [
                "Participate in strategic planning sessions",
                "Contribute to business model development",
                "Engage in industry networking activities"
            ],
            "Delivery & Impact Creation (DEL)": [
                "Execute assigned projects and deliverables",
                "Manage project communications and coordination",
                "Support community engagement initiatives"
            ],
            "Financial (FIN)": [
                "Assist in business development activities",
                "Support proposal writing and funding efforts",
                "Contribute to financial planning processes"
            ],
            "Quality (QUA)": [
                "Conduct quality checks and reviews",
                "Collect and analyze feedback data",
                "Generate performance reports"
            ],
            "Learning Development & Personal Career Growth (LnD)": [
                "Attend training sessions and workshops",
                "Participate in professional development programs",
                "Engage in team feedback and review sessions"
            ],
            "Internal Communication & Management (ICO)": [
                "Utilize project management tools effectively",
                "Maintain clear communication channels",
                "Support team coordination and planning"
            ]
        }
        
        return "\n".join([f"- {activity}" for activity in activities.get(kpi_area, ["Perform assigned duties"])])
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        try:
            # This would require additional API calls to get usage data
            # For now, return basic structure
            return {
                "total_requests": 0,
                "tokens_used": 0,
                "cost_estimate": 0.0
            }
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            return {"error": str(e)}

def main():
    """Test the AI helper functionality"""
    try:
        ai_helper = AIHelper()
        
        # Test job description generation
        job_desc = ai_helper.generate_job_description(
            role="Marketing Associate",
            team="Marketing",
            career_level="Associate",
            company_name="MEREKA INNOVATIVE EDUCATION SDN BHD",
            responsibilities=["Content creation", "Social media management", "Campaign coordination"]
        )
        
        print("Generated Job Description:")
        print(job_desc)
        print("\n" + "="*50 + "\n")
        
        # Test KPI activities generation
        kpi_activities = ai_helper.generate_kpi_activities("Delivery & Impact Creation (DEL)", 55, "Associate")
        
        print("Generated KPI Activities:")
        print(kpi_activities)
        
    except Exception as e:
        print(f"Error testing AI helper: {e}")

if __name__ == "__main__":
    main()
