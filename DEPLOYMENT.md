# Deployment Guide

This guide covers different ways to deploy and use the HR Document Generator.

## 🚀 Quick Deployment Options

### Option 1: Local Development (Recommended for personal use)

1. **Clone the repository**
   ```bash
   git clone https://github.com/lifeofgurpreet/hr-document-generator.git
   cd hr-document-generator
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure your API key**
   ```bash
   # Edit the .env file
   nano .env
   # Add your OpenAI API key: OPENAI_API_KEY=your-key-here
   ```

4. **Start the application**
   ```bash
   python start_hr_interface.py
   ```

5. **Access the web interface**
   Open http://localhost:5001 in your browser

### Option 2: Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "start_hr_interface.py"]
```

Build and run:
```bash
docker build -t hr-document-generator .
docker run -p 5001:5001 -e OPENAI_API_KEY=your-key hr-document-generator
```

### Option 3: Cloud Deployment

#### Heroku
1. Create a `Procfile`:
   ```
   web: python start_hr_interface.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your-key
   git push heroku main
   ```

#### Railway
1. Connect your GitHub repository
2. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 5001
3. Deploy automatically

#### DigitalOcean App Platform
1. Connect your GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Configure run command: `python start_hr_interface.py`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes | None |
| `FLASK_ENV` | Flask environment | No | development |
| `FLASK_DEBUG` | Enable debug mode | No | True |
| `FLASK_PORT` | Port to run on | No | 5001 |

### Configuration Files

1. **Company Information** (`config/company-info.json`)
   - Update with your company details
   - Required for document generation

2. **Job Roles** (`config/job-roles.json`)
   - Predefined roles and KPIs
   - Customize for your organization

3. **AI Prompts** (`config/ai-prompts.json`)
   - Customize AI generation prompts
   - Adjust for your company culture

## 🔒 Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables or secure key management
- Rotate keys regularly

### Data Privacy
- Generated documents contain sensitive information
- Store securely and limit access
- Consider data retention policies

### Network Security
- Use HTTPS in production
- Implement proper authentication if needed
- Restrict access to authorized users

## 📊 Monitoring and Logging

### Application Logs
```bash
# View application logs
tail -f logs/app.log

# Monitor system resources
htop
```

### Health Checks
```bash
# Test the application
curl http://localhost:5001/

# Check API endpoints
curl -X POST http://localhost:5001/generate-documents \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart the application
pkill -f "python start_hr_interface.py"
python start_hr_interface.py
```

### Backup Strategy
1. **Configuration files**: Version control
2. **Generated documents**: Regular backups
3. **Database** (if added): Automated backups

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5001
   lsof -i :5001
   # Kill the process
   kill -9 <PID>
   ```

2. **API key not working**
   ```bash
   # Test API key
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
   ```

3. **Dependencies not installed**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Getting Help
- Check the logs for error messages
- Review the configuration files
- Open an issue on GitHub
- Check the README for common solutions

## 📈 Scaling Considerations

### For High Usage
- Use a production WSGI server (Gunicorn)
- Implement caching for templates
- Add database for document storage
- Use load balancers for multiple instances

### Performance Optimization
- Cache frequently used templates
- Optimize AI API calls
- Implement request queuing
- Monitor resource usage

## 🎯 Production Checklist

- [ ] Set up proper environment variables
- [ ] Configure HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Implement backup strategy
- [ ] Test disaster recovery
- [ ] Document deployment procedures
- [ ] Set up CI/CD pipeline
- [ ] Configure security headers
- [ ] Test load handling
- [ ] Plan for updates and maintenance
