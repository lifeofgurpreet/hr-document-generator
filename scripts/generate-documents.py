#!/usr/bin/env python3
"""
HR Document Generator
Main script for generating employment contracts, roles & responsibilities, and confirmation letters
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the scripts directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_helper import AIHelper
except ImportError:
    # If ai_helper is not available, create a dummy class
    class AIHelper:
        def __init__(self):
            pass
        def generate_job_description(self, *args, **kwargs):
            return "The Employee will perform duties as a Software Developer Intern, supporting the development team in creating innovative educational technology solutions."
        def generate_kpi_activities(self, *args, **kwargs):
            return "- Participate in development activities\n- Learn modern development practices\n- Contribute to real projects"
        def enhance_content(self, content, *args, **kwargs):
            return content
        def validate_document(self, *args, **kwargs):
            return {"valid": True, "issues": [], "suggestions": []}
        def generate_personalized_content(self, content, *args, **kwargs):
            return content

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

class HRDocumentGenerator:
    """Main class for generating HR documents"""
    
    def __init__(self, config_dir: str = "config", templates_dir: str = "templates", output_dir: str = "output"):
        """Initialize the document generator"""
        self.config_dir = Path(config_dir)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        
        # Load configurations
        self.company_info = self._load_config("company-info.json")
        self.job_roles = self._load_config("job-roles.json")
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Initialize AI helper
        try:
            self.ai_helper = AIHelper()
            self.ai_enabled = True
        except Exception as e:
            logger.warning(f"AI helper initialization failed: {e}")
            self.ai_helper = None
            self.ai_enabled = False
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration file"""
        config_path = self.config_dir / filename
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config {filename}: {e}")
            return {}
    
    def generate_employee_data(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete employee data structure for templates"""
        # Extract basic info
        employee_name = employee_info.get('name', 'Employee Name')
        job_title = employee_info.get('job_title', 'Job Title')
        team = employee_info.get('team', 'Mereka')
        career_level = employee_info.get('career_level', 'Associate')
        salary = employee_info.get('salary', 'RM 0')
        start_date = employee_info.get('start_date', datetime.now().strftime('%d/%m/%Y'))
        reporting_to = employee_info.get('reporting_to', 'Manager')
        work_location = employee_info.get('work_location', 'Mereka, PUBLIKA & Remotely')
        employee_id = employee_info.get('employee_id', 'ID Number')
        
        # Calculate contract dates
        start_date_obj = datetime.strptime(start_date, '%d/%m/%Y')
        end_date_obj = start_date_obj + timedelta(days=365)
        end_date = end_date_obj.strftime('%d/%m/%Y')
        
        # Get role-specific data
        role_data = self.job_roles.get('career_levels', {}).get(career_level, {})
        team_data = self.job_roles.get('teams', {}).get(team, {})
        
        # Generate KPI breakdown
        kpi_breakdown = role_data.get('kpi_breakdown', {})
        
        # Generate AI-enhanced content if available
        job_description = employee_info.get('job_description', '')
        if not job_description and self.ai_enabled:
            responsibilities = role_data.get('responsibilities', [])
            job_description = self.ai_helper.generate_job_description(
                job_title, team, career_level, 
                self.company_info['company']['name'], responsibilities
            )
        
        # Generate KPI activities
        kpi_activities = {}
        if self.ai_enabled:
            for area, percentage in kpi_breakdown.items():
                activities = self.ai_helper.generate_kpi_activities(area, percentage, career_level)
                kpi_activities[area] = activities
        
        # Build complete data structure
        data = {
            # Employee information
            'employee_name': employee_name,
            'employee_id': employee_id,
            'job_title': job_title,
            'team': team,
            'career_level': career_level,
            'salary': salary,
            'start_date': start_date,
            'end_date': end_date,
            'contract_date': start_date,
            'reporting_to': reporting_to,
            'work_location': work_location,
            'contract_term': self.company_info.get('contract_terms', {}).get('default_duration', '1-year full time contract'),
            
            # Company information
            'company': self.company_info['company'],
            'working_hours': self.company_info['working_hours'],
            'overtime_policy': self.company_info['overtime_policy'],
            'leave_entitlements': self.company_info['leave_entitlements'],
            'benefits': self.company_info['benefits'],
            'core_values': self.company_info['core_values'],
            'termination': self.company_info['termination'],
            
            # Role-specific information
            'role_responsibilities': role_data.get('responsibilities', []),
            'team_focus_areas': team_data.get('focus_areas', []),
            'job_description': job_description,
            'kpi_breakdown': kpi_breakdown,
            'kpi_activities': kpi_activities,
            
            # Confirmation letter specific
            'confirmation_date': datetime.now().strftime('%d/%m/%Y'),
            'effective_date': start_date,
            'next_review_date': (start_date_obj + timedelta(days=90)).strftime('%d/%m/%Y'),
            'key_responsibilities': role_data.get('responsibilities', [])[:5],  # Top 5 responsibilities
            'hr_contact': {
                'name': 'Alan Roy Antony',
                'title': 'Human Resources, Senior Associate',
                'email': 'hr@mereka.my',
                'phone': '+60 3-1234 5678'
            }
        }
        
        return data
    
    def generate_contract(self, employee_data: Dict[str, Any]) -> str:
        """Generate employment contract"""
        template = self.jinja_env.get_template('contract.md')
        content = template.render(**employee_data)
        
        # Enhance with AI if available
        if self.ai_enabled:
            content = self.ai_helper.enhance_content(content, "professional_tone")
        
        return content
    
    def generate_roles_responsibilities(self, employee_data: Dict[str, Any]) -> str:
        """Generate roles and responsibilities document"""
        template = self.jinja_env.get_template('roles-responsibilities.md')
        content = template.render(**employee_data)
        
        # Enhance with AI if available
        if self.ai_enabled:
            content = self.ai_helper.enhance_content(content, "clarity_check")
        
        return content
    
    def generate_confirmation_letter(self, employee_data: Dict[str, Any]) -> str:
        """Generate confirmation letter"""
        template = self.jinja_env.get_template('confirmation.md')
        content = template.render(**employee_data)
        
        # Personalize with AI if available
        if self.ai_enabled:
            content = self.ai_helper.generate_personalized_content(content, employee_data)
        
        return content
    
    def save_documents(self, employee_name: str, documents: Dict[str, str]) -> str:
        """Save generated documents to output directory"""
        # Create employee-specific output directory
        employee_dir = self.output_dir / employee_name.replace(' ', '_')
        employee_dir.mkdir(parents=True, exist_ok=True)
        
        # Save each document
        saved_files = []
        for doc_type, content in documents.items():
            filename = f"{doc_type}.md"
            filepath = employee_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files.append(str(filepath))
        
        return str(employee_dir)
    
    def validate_documents(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """Validate generated documents"""
        validation_results = {}
        
        if self.ai_enabled:
            for doc_type, content in documents.items():
                validation_results[doc_type] = self.ai_helper.validate_document(content, doc_type)
        else:
            # Basic validation without AI
            for doc_type, content in documents.items():
                validation_results[doc_type] = {
                    "valid": len(content.strip()) > 100,  # Basic length check
                    "issues": [],
                    "suggestions": []
                }
        
        return validation_results
    
    def generate_for_employee(self, employee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate all documents for a single employee"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Generate employee data
            task = progress.add_task("Preparing employee data...", total=None)
            employee_data = self.generate_employee_data(employee_info)
            progress.update(task, description="Employee data prepared")
            
            # Generate documents
            task = progress.add_task("Generating documents...", total=3)
            
            # Contract
            progress.update(task, description="Generating employment contract...")
            contract = self.generate_contract(employee_data)
            progress.advance(task)
            
            # Roles & Responsibilities
            progress.update(task, description="Generating roles & responsibilities...")
            roles_resp = self.generate_roles_responsibilities(employee_data)
            progress.advance(task)
            
            # Confirmation Letter
            progress.update(task, description="Generating confirmation letter...")
            confirmation = self.generate_confirmation_letter(employee_data)
            progress.advance(task)
            
            # Validate documents
            task = progress.add_task("Validating documents...", total=None)
            documents = {
                'contract': contract,
                'roles-responsibilities': roles_resp,
                'confirmation': confirmation
            }
            validation_results = self.validate_documents(documents)
            progress.update(task, description="Documents validated")
            
            # Save documents
            task = progress.add_task("Saving documents...", total=None)
            output_dir = self.save_documents(employee_info['name'], documents)
            progress.update(task, description="Documents saved")
        
        return {
            'employee_data': employee_data,
            'documents': documents,
            'validation_results': validation_results,
            'output_directory': output_dir
        }
    
    def generate_batch(self, csv_file: str) -> List[Dict[str, Any]]:
        """Generate documents for multiple employees from CSV file"""
        try:
            df = pd.read_csv(csv_file)
            results = []
            
            console.print(f"[bold blue]Processing {len(df)} employees from {csv_file}[/bold blue]")
            
            for index, row in df.iterrows():
                employee_info = row.to_dict()
                console.print(f"\n[bold green]Processing: {employee_info.get('name', 'Unknown')}[/bold green]")
                
                try:
                    result = self.generate_for_employee(employee_info)
                    results.append(result)
                    console.print(f"[green]✓ Completed[/green]")
                except Exception as e:
                    console.print(f"[red]✗ Error: {e}[/red]")
                    results.append({'error': str(e), 'employee_info': employee_info})
            
            return results
        except Exception as e:
            logger.error(f"Error processing batch file: {e}")
            raise

def interactive_input() -> Dict[str, Any]:
    """Get employee information interactively"""
    console.print("[bold blue]Enter Employee Information[/bold blue]")
    
    employee_info = {}
    
    employee_info['name'] = console.input("Employee Name: ")
    employee_info['job_title'] = console.input("Job Title: ")
    employee_info['team'] = console.input("Team (Mereka/Marketing/Operations): ") or "Mereka"
    employee_info['career_level'] = console.input("Career Level (Manager/Associate/Senior Associate/Junior Associate): ") or "Associate"
    employee_info['salary'] = console.input("Salary (e.g., RM 5000): ") or "RM 5000"
    employee_info['start_date'] = console.input("Start Date (DD/MM/YYYY): ") or datetime.now().strftime('%d/%m/%Y')
    employee_info['reporting_to'] = console.input("Reporting To: ") or "Manager"
    employee_info['work_location'] = console.input("Work Location: ") or "Mereka, PUBLIKA & Remotely"
    employee_info['employee_id'] = console.input("Employee ID/NRIC: ") or "ID123456"
    
    return employee_info

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate HR documents for new employees')
    parser.add_argument('--employee', help='Employee name for quick generation')
    parser.add_argument('--role', help='Job role/title')
    parser.add_argument('--salary', help='Salary amount')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--batch', help='CSV file for batch processing')
    parser.add_argument('--output', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = HRDocumentGenerator(output_dir=args.output)
        
        if args.batch:
            # Batch processing
            results = generator.generate_batch(args.batch)
            
            # Display summary
            table = Table(title="Batch Processing Results")
            table.add_column("Employee", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Output Directory", style="blue")
            
            for result in results:
                if 'error' in result:
                    table.add_row(
                        result['employee_info'].get('name', 'Unknown'),
                        "Error",
                        str(result['error'])
                    )
                else:
                    table.add_row(
                        result['employee_data']['employee_name'],
                        "Success",
                        result['output_directory']
                    )
            
            console.print(table)
            
        elif args.interactive:
            # Interactive mode
            employee_info = interactive_input()
            result = generator.generate_for_employee(employee_info)
            
            console.print(f"\n[bold green]Documents generated successfully![/bold green]")
            console.print(f"Output directory: {result['output_directory']}")
            
        elif args.employee:
            # Quick generation with minimal info
            employee_info = {
                'name': args.employee,
                'job_title': args.role or 'Employee',
                'salary': args.salary or 'RM 5000',
                'career_level': 'Associate',
                'team': 'Mereka'
            }
            
            result = generator.generate_for_employee(employee_info)
            
            console.print(f"\n[bold green]Documents generated for {args.employee}![/bold green]")
            console.print(f"Output directory: {result['output_directory']}")
            
        else:
            # Show help
            parser.print_help()
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
