#!/usr/bin/env python3
"""
Test Script for HR Automation System
Demonstrates the functionality without requiring OpenAI API
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.append('scripts')

def test_system_without_ai():
    """Test the system without AI integration"""
    print("🧪 Testing HR Automation System (Without AI)")
    print("=" * 50)
    
    # Test configuration loading
    print("\n1. Testing Configuration Loading...")
    try:
        with open('config/company-info.json', 'r') as f:
            company_info = json.load(f)
        print("✅ Company info loaded successfully")
        
        with open('config/job-roles.json', 'r') as f:
            job_roles = json.load(f)
        print("✅ Job roles loaded successfully")
        
    except Exception as e:
        print(f"❌ Error loading configurations: {e}")
        return False
    
    # Test template loading
    print("\n2. Testing Template Loading...")
    try:
        templates_dir = Path('templates')
        templates = list(templates_dir.glob('*.md'))
        
        for template in templates:
            with open(template, 'r') as f:
                content = f.read()
            print(f"✅ Template loaded: {template.name}")
        
    except Exception as e:
        print(f"❌ Error loading templates: {e}")
        return False
    
    # Test document generation (without AI)
    print("\n3. Testing Document Generation...")
    try:
        # Create a mock employee data
        employee_data = {
            'employee_name': 'Test Employee',
            'employee_id': 'TEST123',
            'job_title': 'Test Associate',
            'team': 'Mereka',
            'career_level': 'Associate',
            'salary': 'RM 5000',
            'start_date': '15/03/2025',
            'end_date': '14/03/2026',
            'contract_date': '15/03/2025',
            'reporting_to': 'Test Manager',
            'work_location': 'Mereka, PUBLIKA & Remotely',
            'contract_term': '1-year full time contract',
            'company': company_info['company'],
            'working_hours': company_info['working_hours'],
            'overtime_policy': company_info['overtime_policy'],
            'leave_entitlements': company_info['leave_entitlements'],
            'benefits': company_info['benefits'],
            'core_values': company_info['core_values'],
            'termination': company_info['termination'],
            'role_responsibilities': job_roles['career_levels']['Associate']['responsibilities'],
            'team_focus_areas': job_roles['teams']['Mereka']['focus_areas'],
            'job_description': 'Test job description for demonstration purposes.',
            'kpi_breakdown': job_roles['career_levels']['Associate']['kpi_breakdown'],
            'confirmation_date': datetime.now().strftime('%d/%m/%Y'),
            'effective_date': '15/03/2025',
            'next_review_date': '13/06/2025',
            'key_responsibilities': job_roles['career_levels']['Associate']['responsibilities'][:5],
            'hr_contact': {
                'name': 'Alan Roy Antony',
                'title': 'Human Resources, Senior Associate',
                'email': 'hr@mereka.my',
                'phone': '+60 3-1234 5678'
            }
        }
        
        # Test Jinja2 template rendering
        from jinja2 import Environment, FileSystemLoader
        
        env = Environment(loader=FileSystemLoader('templates'))
        
        # Test contract template
        contract_template = env.get_template('contract.md')
        contract_content = contract_template.render(**employee_data)
        print("✅ Contract template rendered successfully")
        
        # Test roles template
        roles_template = env.get_template('roles-responsibilities.md')
        roles_content = roles_template.render(**employee_data)
        print("✅ Roles & responsibilities template rendered successfully")
        
        # Test confirmation template
        confirmation_template = env.get_template('confirmation.md')
        confirmation_content = confirmation_template.render(**employee_data)
        print("✅ Confirmation letter template rendered successfully")
        
        # Save test documents
        output_dir = Path('output/test_employee')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / 'contract.md', 'w') as f:
            f.write(contract_content)
        with open(output_dir / 'roles-responsibilities.md', 'w') as f:
            f.write(roles_content)
        with open(output_dir / 'confirmation.md', 'w') as f:
            f.write(confirmation_content)
        
        print(f"✅ Test documents saved to: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error generating documents: {e}")
        return False
    
    # Test CSV processing
    print("\n4. Testing CSV Processing...")
    try:
        import pandas as pd
        
        df = pd.read_csv('sample_employees.csv')
        print(f"✅ CSV loaded successfully with {len(df)} employees")
        
        for index, row in df.iterrows():
            print(f"   - {row['name']}: {row['job_title']} ({row['career_level']})")
        
    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("\nNext steps:")
    print("1. Set up OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the system: python scripts/generate-documents.py --interactive")
    print("4. Or test with sample data: python scripts/generate-documents.py --batch sample_employees.csv")
    
    return True

def show_system_overview():
    """Show system overview and capabilities"""
    print("🚀 HR Automation System Overview")
    print("=" * 50)
    
    print("\n📋 Features:")
    print("• AI-powered document generation using OpenAI API")
    print("• Template-based system with Jinja2")
    print("• Support for multiple document types (Contract, Roles, Confirmation)")
    print("• Batch processing from CSV files")
    print("• Interactive mode for single employee")
    print("• PDF conversion capabilities")
    print("• Document validation and enhancement")
    
    print("\n📁 System Structure:")
    print("• templates/ - Document templates")
    print("• config/ - Configuration files")
    print("• scripts/ - Automation scripts")
    print("• output/ - Generated documents")
    print("• sample/ - Original sample documents")
    
    print("\n🔧 Usage Examples:")
    print("• Interactive mode: python scripts/generate-documents.py --interactive")
    print("• Quick generation: python scripts/generate-documents.py --employee 'John Doe' --role 'Marketing Associate'")
    print("• Batch processing: python scripts/generate-documents.py --batch sample_employees.csv")
    print("• PDF conversion: python scripts/pdf-converter.py output/employee_name/")
    
    print("\n🤖 AI Integration:")
    print("• Dynamic job description generation")
    print("• KPI activity suggestions")
    print("• Content enhancement and validation")
    print("• Personalized confirmation letters")
    print("• Professional tone improvement")

if __name__ == "__main__":
    show_system_overview()
    print("\n" + "=" * 50)
    test_system_without_ai()
