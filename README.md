# HR Document Generator

An AI-powered HR document generation system that creates personalized employment contracts, job descriptions, and confirmation letters using templates and OpenAI integration.

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/hr-document-generator.git
cd hr-document-generator

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Start the web interface
python start_hr_interface.py
```

Then open http://localhost:5001 in your browser.

### Option 2: Command Line
```bash
# Interactive mode
python scripts/generate-documents.py --interactive

# Quick generation
python scripts/generate-documents.py --employee "John Doe" --role "Marketing Associate" --salary "RM 5000"

# Batch processing
python scripts/generate-documents.py --batch sample_employees.csv
```

## 📁 Project Structure

```
HRTemplate/
├── templates/                 # Template files
│   ├── contract.md           # Employment contract template
│   ├── roles-responsibilities.md  # Job description template
│   └── confirmation.md        # Confirmation letter template
├── config/                    # Configuration files
│   ├── company-info.json     # Company details
│   ├── job-roles.json        # Predefined job roles and KPIs
│   └── ai-prompts.json       # AI generation prompts
├── scripts/                   # Automation scripts
│   ├── generate-documents.py # Main document generator
│   ├── ai-helper.py          # OpenAI API integration
│   └── pdf-converter.py      # Markdown to PDF conversion
├── output/                    # Generated documents
│   └── [employee-name]/      # Individual employee folders
├── sample/                    # Original sample documents
├── app.py                     # Flask web application
├── start_hr_interface.py     # Startup script
└── requirements.txt           # Python dependencies
```

## 🛠️ Features

- **🤖 AI-Powered Generation**: Uses OpenAI API to dynamically generate personalized content
- **📝 Template System**: Reusable templates with variable substitution
- **📄 Multi-Format Output**: Generates both Markdown and PDF formats
- **✅ Validation**: AI-powered content review and verification
- **📊 Batch Processing**: Generate documents for multiple employees at once
- **🌐 Web Interface**: User-friendly Flask-based web application
- **🔧 CLI Tools**: Command-line interface for automation

## ⚙️ Configuration

### 1. OpenAI API Key
Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

### 2. Company Information
Edit `config/company-info.json` with your company details:
```json
{
  "company_name": "Your Company Name",
  "registration_number": "123456789",
  "address": "Your Company Address",
  "contact_email": "hr@yourcompany.com"
}
```

### 3. Job Roles
Configure predefined roles in `config/job-roles.json`:
```json
{
  "Marketing Associate": {
    "department": "Marketing",
    "level": "Entry",
    "kpis": ["Lead Generation", "Campaign Performance"]
  }
}
```

## 📋 Usage Examples

### Web Interface
1. Start the application: `python start_hr_interface.py`
2. Open http://localhost:5001
3. Fill in employee details
4. Generate and download documents

### Command Line
```bash
# Generate documents for a single employee
python scripts/generate-documents.py \
  --employee "Jane Smith" \
  --role "Software Engineer" \
  --salary "RM 8000" \
  --start_date "2024-01-15"

# Interactive mode for guided input
python scripts/generate-documents.py --interactive

# Batch processing from CSV
python scripts/generate-documents.py --batch employees.csv
```

### PDF Conversion
```bash
# Convert generated documents to PDF
python scripts/pdf-converter.py output/Jane_Smith/
```

## 📄 Input Requirements

For each employee, you'll need:
- **Personal Information**: Name, NRIC/Passport, contact details
- **Job Details**: Title, team, career level, start date
- **Compensation**: Salary, benefits
- **Reporting Structure**: Manager, work location
- **Role Description**: Brief description or job posting content

## 🔒 Security & Privacy

- All personal information is processed locally
- API calls are logged for audit purposes
- Generated documents are stored securely
- Templates can be version controlled
- No sensitive data is sent to external services except OpenAI API

## 🧪 Testing

Run the smoke test to verify everything works:
```bash
python test_system.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly: `python test_system.py`
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues or questions:
1. Check the configuration files
2. Verify API key setup
3. Review generated logs
4. Open an issue on GitHub

## 🔄 Updates

To update the project:
```bash
git pull origin main
pip install -r requirements.txt
```

---

**Note**: This system is designed for internal HR use. Ensure compliance with local labor laws and company policies when generating employment documents.
