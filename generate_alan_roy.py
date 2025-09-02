#!/usr/bin/env python3
"""
Generate documents for Alan Roy - Software Developer Intern
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append('scripts')

# Import the document generator
from generate_documents import HRDocumentGenerator

def main():
    """Generate documents for Alan Roy"""
    print("🚀 Generating documents for Alan Roy - Software Developer Intern")
    print("=" * 60)
    
    # Load Alan Roy's data
    with open('alan_roy_data.json', 'r') as f:
        alan_data = json.load(f)
    
    print(f"📋 Employee: {alan_data['name']}")
    print(f"🎯 Position: {alan_data['job_title']}")
    print(f"🏢 Team: {alan_data['team']}")
    print(f"📊 Level: {alan_data['career_level']}")
    print(f"💰 Salary: {alan_data['salary']}")
    print(f"📅 Start Date: {alan_data['start_date']}")
    print()
    
    # Initialize the document generator
    generator = HRDocumentGenerator()
    
    # Generate documents
    print("🔄 Generating documents...")
    result = generator.generate_for_employee(alan_data)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print("✅ Documents generated successfully!")
    print(f"📁 Output directory: {result['output_directory']}")
    
    # Show what was generated
    print("\n📄 Generated Documents:")
    for doc_type, content in result['documents'].items():
        print(f"   • {doc_type}.md")
    
    # Show validation results
    print("\n🔍 Validation Results:")
    for doc_type, validation in result['validation_results'].items():
        status = "✅ Valid" if validation.get('valid', False) else "❌ Issues Found"
        print(f"   • {doc_type}: {status}")
        if validation.get('issues'):
            for issue in validation['issues']:
                print(f"     - {issue}")
    
    print("\n🎉 Alan Roy's documents are ready!")
    print(f"📂 Check the folder: {result['output_directory']}")

if __name__ == "__main__":
    main()
