from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import Dict, Any
try:
    import openai
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception:
    openai_client = None
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Load configuration
with open('config/ai-prompts.json', 'r') as f:
    AI_PROMPTS = json.load(f)
with open('config/company-info.json', 'r') as f:
    COMPANY_INFO = json.load(f)
with open('config/job-roles.json', 'r') as f:
    JOB_ROLES = json.load(f)

# Jinja environment for fallback rendering
jinja_env = Environment(loader=FileSystemLoader('templates'), autoescape=False, trim_blocks=True, lstrip_blocks=True)

# Load templates
def load_template(template_name):
    # Map document types to actual template filenames
    template_mapping = {
        'contract': 'contract.md',
        'confirmation': 'confirmation.md',
        'roles': 'roles-responsibilities.md',
        'roles-responsibilities': 'roles-responsibilities.md'
    }

    template_filename = template_mapping.get(template_name, f'{template_name}.md')
    template_path = f'templates/{template_filename}'

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

DEMO_MODE = openai_client is None

def generate_document_content(template_content, employee_data, document_type):
    """Generate document content using OpenAI API or demo mode"""
    # If in demo mode, we won't use AI here (return None to trigger fallback)
    if DEMO_MODE:
        return None
    
    # Prepare the prompt based on document type
    if document_type == 'contract':
        prompt = AI_PROMPTS['contract_generation']['job_description'].format(
            role=employee_data['jobTitle'],
            company_name="Mereka",  # You can make this configurable
            team=employee_data['team'],
            responsibilities=employee_data['jobDescription']
        )
    elif document_type == 'confirmation':
        prompt = AI_PROMPTS['confirmation_letter']['personalized'].format(
            employee_name=employee_data['employeeName'],
            role=employee_data['jobTitle'],
            company_name="Mereka"
        )
    elif document_type == 'roles':
        prompt = AI_PROMPTS['roles_responsibilities']['main_description'].format(
            career_level=employee_data['careerLevel'],
            team=employee_data['team'],
            focus_areas=employee_data.get('focusAreas', 'various areas')
        )
    
    # Add template context to the prompt
    full_prompt = f"""
    {prompt}
    
    Please use the following template structure and fill in the placeholders with the provided employee data:
    
    {template_content}
    
    Employee Data:
    - Name: {employee_data['employeeName']}
    - Job Title: {employee_data['jobTitle']}
    - Team: {employee_data['team']}
    - Career Level: {employee_data['careerLevel']}
    - Salary: {employee_data['salary']}
    - Start Date: {employee_data['startDate']}
    - Reporting To: {employee_data['reportingTo']}
    - Work Location: {employee_data['workLocation']}
    - Employee ID: {employee_data['employeeId']}
    - Job Description: {employee_data['jobDescription']}
    - Focus Areas: {employee_data.get('focusAreas', 'Various areas')}
    
    Generate a complete, professional document that fills in all the template placeholders with the provided data.
    """
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an HR document generator. Generate professional, complete documents based on the provided template and employee data."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def _normalize_kpis(kpi_breakdown: Dict[str, Any]) -> Dict[str, int]:
    mapping = {"Vision": 0, "Delivery": 0, "Financial": 0, "Quality": 0, "LnD": 0, "ICO": 0}
    for raw_key, val in (kpi_breakdown or {}).items():
        key = raw_key.lower()
        if "vision" in key:
            mapping["Vision"] = val
        elif "delivery" in key:
            mapping["Delivery"] = val
        elif "financial" in key or "fin" in key:
            mapping["Financial"] = val
        elif "quality" in key or "qua" in key:
            mapping["Quality"] = val
        elif "learning" in key or "lnd" in key:
            mapping["LnD"] = val
        elif "internal" in key or "ico" in key or "communications" in key:
            mapping["ICO"] = val
    return mapping

def _default_kpi_activities(area: str) -> str:
    fallback = {
        "Vision": [
            "Participate in strategic planning sessions",
            "Contribute to business model development",
            "Engage in industry networking activities"
        ],
        "Delivery": [
            "Execute assigned projects and deliverables",
            "Manage project communications and coordination",
            "Support community engagement initiatives"
        ],
        "Financial": [
            "Assist in business development activities",
            "Support proposal writing and funding efforts",
            "Contribute to financial planning processes"
        ],
        "Quality": [
            "Conduct quality checks and reviews",
            "Collect and analyze feedback data",
            "Generate performance reports"
        ],
        "LnD": [
            "Attend training sessions and workshops",
            "Participate in professional development programs",
            "Engage in team feedback and review sessions"
        ],
        "ICO": [
            "Utilize project management tools effectively",
            "Maintain clear communication channels",
            "Support team coordination and planning"
        ]
    }
    return "\n".join([f"- {a}" for a in fallback.get(area, ["Perform assigned duties"])])

def build_employee_context(data: Dict[str, Any]) -> Dict[str, Any]:
    # Convert date format
    start_date_iso = data['startDate']
    try:
        dt = datetime.strptime(start_date_iso, '%Y-%m-%d')
        start_date = dt.strftime('%d/%m/%Y')
    except Exception:
        start_date = data['startDate']
        dt = datetime.now()

    end_date = (dt + timedelta(days=365)).strftime('%d/%m/%Y')

    career_level = data['careerLevel']
    team = data['team']
    role_data = JOB_ROLES.get('career_levels', {}).get(career_level, JOB_ROLES.get('career_levels', {}).get('Associate', {}))
    team_data = JOB_ROLES.get('teams', {}).get(team, {})

    kpis = _normalize_kpis(role_data.get('kpi_breakdown', {}))
    activities = {k: _default_kpi_activities(k) for k in kpis.keys()}

    focus_areas = data.get('focusAreas') or ", ".join(team_data.get('focus_areas', []))
    if isinstance(focus_areas, str):
        focus_areas_list = [x.strip() for x in focus_areas.split(',') if x.strip()]
    else:
        focus_areas_list = team_data.get('focus_areas', [])

    return {
        'employee_name': data['employeeName'],
        'employee_id': data['employeeId'],
        'job_title': data['jobTitle'],
        'team': team,
        'career_level': career_level,
        'salary': data['salary'],
        'start_date': start_date,
        'end_date': end_date,
        'contract_date': start_date,
        'reporting_to': data['reportingTo'],
        'work_location': data['workLocation'],
        'contract_term': COMPANY_INFO.get('contract_terms', {}).get('default_duration', '1-year full time contract'),

        'company': COMPANY_INFO['company'],
        'working_hours': COMPANY_INFO['working_hours'],
        'overtime_policy': COMPANY_INFO['overtime_policy'],
        'leave_entitlements': COMPANY_INFO['leave_entitlements'],
        'benefits': COMPANY_INFO['benefits'],
        'core_values': COMPANY_INFO['core_values'],
        'termination': COMPANY_INFO['termination'],

        'role_responsibilities': role_data.get('responsibilities', []),
        'team_focus_areas': team_data.get('focus_areas', focus_areas_list),
        'job_description': data.get('jobDescription', ''),
        'kpi_breakdown': kpis,
        'vision_activities': activities.get('Vision', ''),
        'delivery_activities': activities.get('Delivery', ''),
        'financial_activities': activities.get('Financial', ''),
        'quality_activities': activities.get('Quality', ''),
        'lnd_activities': activities.get('LnD', ''),
        'ico_activities': activities.get('ICO', ''),

        'confirmation_date': datetime.now().strftime('%d/%m/%Y'),
        'effective_date': start_date,
        'next_review_date': (dt + timedelta(days=90)).strftime('%d/%m/%Y'),
        'key_responsibilities': role_data.get('responsibilities', [])[:5],
        'hr_contact': {
            'name': 'Alan Roy Antony',
            'title': 'Human Resources, Senior Associate',
            'email': 'hr@mereka.my',
            'phone': '+60 3-1234 5678'
        }
    }

def render_template_with_context(template_name: str, context: Dict[str, Any]) -> str:
    template = jinja_env.get_template(template_name)
    return template.render(**context)

@app.route('/')
def index():
    return send_file('hr_interface.html')

@app.route('/generate-documents', methods=['POST'])
def generate_documents():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['employeeName', 'jobTitle', 'team', 'careerLevel', 'salary', 
                         'startDate', 'reportingTo', 'workLocation', 'employeeId', 'jobDescription']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        if not data.get('documents'):
            return jsonify({'error': 'No document types selected'}), 400
        
        generated_documents = []
        
        for doc_type in data['documents']:
            try:
                # Determine actual template key/name
                template_key = 'roles-responsibilities' if doc_type == 'roles' else doc_type
                template_content = load_template(template_key)
                
                # Generate content using OpenAI
                generated_content = generate_document_content(template_content, data, template_key)

                # Build template context
                context = build_employee_context(data)

                if generated_content:
                    final_content = generated_content
                else:
                    final_content = render_template_with_context(f"{template_key}.md", context)

                # Create timestamp for filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{data['employeeName'].replace(' ', '_')}_{template_key}_{timestamp}.md"

                # For Vercel deployment, return content directly instead of saving files
                generated_documents.append({
                    'type': template_key.replace('-', ' ').title(),
                    'filename': filename,
                    'content': final_content,
                    'download_url': f'/download/{filename}'
                })
                    
            except Exception as e:
                print(f"Error generating {doc_type}: {e}")
                return jsonify({'error': f'Error generating {doc_type} document: {str(e)}'}), 500
        
        return jsonify({
            'success': True,
            'documents': generated_documents
        })
        
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # For Vercel deployment, we'll need to handle this differently
        # Since we can't save files, we'll return a message to use the content directly
        return jsonify({
            'message': 'For Vercel deployment, use the content field from the generate-documents response',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key before running the application.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
    
    # For Vercel deployment, use the PORT environment variable
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
