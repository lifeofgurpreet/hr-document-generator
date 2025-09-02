from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import openai
from datetime import datetime
import tempfile
from pathlib import Path
import re

app = Flask(__name__)

# Load configuration
with open('config/ai-prompts.json', 'r') as f:
    AI_PROMPTS = json.load(f)

# Load templates
def load_template(template_name):
    # Map document types to actual template filenames
    template_mapping = {
        'contract': 'contract.md',
        'confirmation': 'confirmation.md',
        'roles': 'roles-responsibilities.md'
    }
    
    template_filename = template_mapping.get(template_name, f'{template_name}.md')
    template_path = f'templates/{template_filename}'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

# Initialize OpenAI client (you'll need to set OPENAI_API_KEY environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Demo mode - if no API key, use sample data
DEMO_MODE = not bool(os.getenv('OPENAI_API_KEY'))

def generate_document_content(template_content, employee_data, document_type):
    """Generate document content using OpenAI API or demo mode"""
    
    # If in demo mode, use sample data instead of OpenAI API
    if DEMO_MODE:
        return generate_demo_content(template_content, employee_data, document_type)
    
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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

def generate_demo_content(template_content, employee_data, document_type):
    """Generate demo content without OpenAI API"""
    # Fill basic placeholders
    content = fill_template_placeholders(template_content, employee_data)
    
    # Add some demo-specific content based on document type
    if document_type == 'contract':
        content += f"""

## Demo Mode Notice
This document was generated in demo mode without AI enhancement.
For full AI-powered document generation, please set your OpenAI API key.

Employee: {employee_data['employeeName']}
Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
    elif document_type == 'confirmation':
        content += f"""

---
*This confirmation letter was generated in demo mode. For AI-enhanced content, please set your OpenAI API key.*
"""
    elif document_type == 'roles':
        content += f"""

---
*Demo Mode: This document shows basic template filling. Enable AI enhancement by setting your OpenAI API key.*
"""
    
    return content

def fill_template_placeholders(template_content, employee_data):
    """Fill basic placeholders in the template"""
    # Basic placeholder replacement
    replacements = {
        '{{ employee_name }}': employee_data['employeeName'],
        '{{ job_title }}': employee_data['jobTitle'],
        '{{ team }}': employee_data['team'],
        '{{ career_level }}': employee_data['careerLevel'],
        '{{ salary }}': employee_data['salary'],
        '{{ start_date }}': employee_data['startDate'],
        '{{ reporting_to }}': employee_data['reportingTo'],
        '{{ work_location }}': employee_data['workLocation'],
        '{{ employee_id }}': employee_data['employeeId'],
        '{{ job_description }}': employee_data['jobDescription'],
        '{{ contract_date }}': datetime.now().strftime('%d/%m/%Y'),
        '{{ company.name }}': 'Mereka',
        '{{ company.registration_number }}': '202001012345'
    }
    
    content = template_content
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, str(value))
    
    return content

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
                # Load template
                template_content = load_template(doc_type)
                
                # Generate content using OpenAI
                generated_content = generate_document_content(template_content, data, doc_type)
                
                if generated_content:
                    # Fill any remaining placeholders
                    final_content = fill_template_placeholders(generated_content, data)
                    
                    # Create temporary file
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{data['employeeName'].replace(' ', '_')}_{doc_type}_{timestamp}.md"
                    
                    # Ensure output directory exists
                    os.makedirs('output', exist_ok=True)
                    filepath = os.path.join('output', filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    
                    generated_documents.append({
                        'type': doc_type.title(),
                        'filename': filename,
                        'url': f'/download/{filename}'
                    })
                else:
                    return jsonify({'error': f'Failed to generate {doc_type} document'}), 500
                    
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
        filepath = os.path.join('output', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key before running the application.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
