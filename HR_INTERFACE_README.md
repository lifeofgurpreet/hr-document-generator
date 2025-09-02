# HR Document Generator Interface

A simple web interface for HR personnel to generate employment documents using AI. This interface allows HR staff to input basic employee information and automatically generate professional documents like employment contracts, confirmation letters, and roles & responsibilities documents.

## Features

- 📝 **Simple Form Interface**: Easy-to-use form for entering employee information
- 🤖 **AI-Powered Generation**: Uses OpenAI GPT to generate professional documents
- 📄 **Multiple Document Types**: Generate employment contracts, confirmation letters, and roles & responsibilities
- 💾 **Instant Download**: Generated documents are immediately available for download
- 🎨 **Clean UI**: Modern, responsive design that works on desktop and mobile

## Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Setup

1. **Set your OpenAI API key**:
   ```bash
   # macOS/Linux
   export OPENAI_API_KEY='your-api-key-here'
   
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   ```

2. **Run the startup script**:
   ```bash
   python start_hr_interface.py
   ```

3. **Open your browser** and go to: `http://localhost:5000`

## Usage

1. **Fill in the form** with employee information:
   - Employee Name
   - Job Title
   - Team
   - Career Level
   - Salary
   - Start Date
   - Reporting To
   - Work Location
   - Employee ID
   - Job Description
   - Focus Areas (optional)

2. **Select document types** to generate:
   - Employment Contract
   - Confirmation Letter
   - Roles & Responsibilities

3. **Click "Generate Documents"** and wait for processing

4. **Download** the generated documents

## Document Types

### Employment Contract
- Professional employment contract with all legal requirements
- Includes job specifications, KPI breakdown, working hours, and termination clauses
- Automatically filled with employee-specific information

### Confirmation Letter
- Personalized confirmation letter for new employees
- Warm, professional tone with specific role mentions
- Expresses confidence in future contributions

### Roles & Responsibilities
- Comprehensive roles and responsibilities document
- Includes specific, measurable responsibilities
- Aligned with company strategic objectives

## Technical Details

### Architecture
- **Frontend**: HTML/CSS/JavaScript (single page application)
- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-3.5-turbo
- **Templates**: Markdown-based templates with placeholders

### File Structure
```
HRTemplate/
├── hr_interface.html      # Main interface
├── app.py                 # Flask backend
├── start_hr_interface.py  # Startup script
├── config/
│   └── ai-prompts.json    # AI prompt configurations
├── templates/
│   ├── contract.md        # Employment contract template
│   ├── confirmation.md    # Confirmation letter template
│   └── roles-responsibilities.md  # Roles template
└── output/                # Generated documents (created automatically)
```

### API Endpoints
- `GET /` - Serves the main interface
- `POST /generate-documents` - Generates documents from form data
- `GET /download/<filename>` - Downloads generated documents

## Customization

### Adding New Document Types
1. Create a new template in `templates/` directory
2. Add AI prompts in `config/ai-prompts.json`
3. Update the form in `hr_interface.html`
4. Add generation logic in `app.py`

### Modifying Templates
Edit the markdown files in the `templates/` directory. Use placeholders like `{{ employee_name }}` for dynamic content.

### Changing AI Prompts
Edit `config/ai-prompts.json` to modify how AI generates content for each document type.

## Troubleshooting

### Common Issues

1. **"OpenAI API key not set"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Restart your terminal after setting the variable

2. **"Failed to generate document"**
   - Check your internet connection
   - Verify your OpenAI API key is valid
   - Check OpenAI API usage limits

3. **"Port 5000 already in use"**
   - Change the port in `app.py` (line 150)
   - Or kill the process using port 5000

### Debug Mode
The application runs in debug mode by default. Check the terminal output for detailed error messages.

## Security Notes

- This is a demonstration interface
- In production, add proper authentication and validation
- Consider rate limiting for API calls
- Validate all user inputs
- Use HTTPS in production

## Support

For issues or questions:
1. Check the terminal output for error messages
2. Verify your OpenAI API key is working
3. Ensure all required fields are filled in the form

---

**Note**: This interface is designed for demonstration purposes. For production use, implement proper security measures and error handling.
