#!/usr/bin/env python3
"""
PDF Converter for HR Documents
Converts Markdown documents to PDF format
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional
import markdown
from weasyprint import HTML, CSS
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

class PDFConverter:
    """Convert Markdown documents to PDF"""
    
    def __init__(self):
        """Initialize the PDF converter"""
        self.css_styles = self._get_default_css()
    
    def _get_default_css(self) -> str:
        """Get default CSS styles for PDF generation"""
        return """
        @page {
            size: A4;
            margin: 2cm;
            @top-center {
                content: "HR Document";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Arial', sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }
        
        h1 {
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        h2 {
            font-size: 18pt;
            font-weight: bold;
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        
        h3 {
            font-size: 14pt;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        p {
            margin-bottom: 12px;
            text-align: justify;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }
        
        ul, ol {
            margin-bottom: 15px;
            padding-left: 20px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        .signature-section {
            margin-top: 40px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }
        
        .signature-line {
            border-bottom: 1px solid #333;
            display: inline-block;
            min-width: 200px;
            margin: 10px 0;
        }
        
        .company-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .company-name {
            font-size: 20pt;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .document-type {
            font-size: 16pt;
            color: #7f8c8d;
            margin-top: 10px;
        }
        """
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert Markdown content to HTML"""
        # Configure Markdown extensions
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=extensions)
        
        # Wrap in HTML document structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>HR Document</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        return full_html
    
    def html_to_pdf(self, html_content: str, output_path: str) -> bool:
        """Convert HTML content to PDF"""
        try:
            # Create HTML object
            html = HTML(string=html_content)
            
            # Create CSS object
            css = CSS(string=self.css_styles)
            
            # Generate PDF
            html.write_pdf(output_path, stylesheets=[css])
            
            return True
        except Exception as e:
            logger.error(f"Error converting HTML to PDF: {e}")
            return False
    
    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Convert a single Markdown file to PDF"""
        try:
            input_file = Path(input_path)
            
            if not input_file.exists():
                logger.error(f"Input file not found: {input_path}")
                return False
            
            # Read Markdown content
            with open(input_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Convert to HTML
            html_content = self.markdown_to_html(markdown_content)
            
            # Determine output path
            if output_path is None:
                output_path = input_file.with_suffix('.pdf')
            
            # Convert to PDF
            success = self.html_to_pdf(html_content, str(output_path))
            
            if success:
                console.print(f"[green]✓ Converted: {input_path} → {output_path}[/green]")
            else:
                console.print(f"[red]✗ Failed to convert: {input_path}[/red]")
            
            return success
            
        except Exception as e:
            logger.error(f"Error converting file {input_path}: {e}")
            return False
    
    def convert_directory(self, input_dir: str, output_dir: Optional[str] = None) -> List[str]:
        """Convert all Markdown files in a directory to PDF"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            logger.error(f"Input directory not found: {input_dir}")
            return []
        
        if output_dir is None:
            output_path = input_path
        else:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all Markdown files
        markdown_files = list(input_path.glob("*.md"))
        
        if not markdown_files:
            console.print(f"[yellow]No Markdown files found in {input_dir}[/yellow]")
            return []
        
        converted_files = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Converting files...", total=len(markdown_files))
            
            for md_file in markdown_files:
                progress.update(task, description=f"Converting {md_file.name}...")
                
                pdf_file = output_path / f"{md_file.stem}.pdf"
                
                if self.convert_file(str(md_file), str(pdf_file)):
                    converted_files.append(str(pdf_file))
                
                progress.advance(task)
        
        return converted_files
    
    def convert_employee_documents(self, employee_dir: str) -> bool:
        """Convert all documents for a specific employee"""
        employee_path = Path(employee_dir)
        
        if not employee_path.exists():
            logger.error(f"Employee directory not found: {employee_dir}")
            return False
        
        # Find all Markdown files
        markdown_files = list(employee_path.glob("*.md"))
        
        if not markdown_files:
            console.print(f"[yellow]No Markdown files found in {employee_dir}[/yellow]")
            return False
        
        success_count = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Converting employee documents...", total=len(markdown_files))
            
            for md_file in markdown_files:
                progress.update(task, description=f"Converting {md_file.name}...")
                
                pdf_file = md_file.with_suffix('.pdf')
                
                if self.convert_file(str(md_file), str(pdf_file)):
                    success_count += 1
                
                progress.advance(task)
        
        console.print(f"[green]✓ Converted {success_count}/{len(markdown_files)} documents for {employee_path.name}[/green]")
        return success_count == len(markdown_files)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Convert Markdown HR documents to PDF')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('--output', help='Output file or directory')
    parser.add_argument('--employee', help='Convert documents for specific employee directory')
    
    args = parser.parse_args()
    
    try:
        converter = PDFConverter()
        
        if args.employee:
            # Convert documents for specific employee
            success = converter.convert_employee_documents(args.employee)
            if not success:
                sys.exit(1)
        
        elif Path(args.input).is_file():
            # Convert single file
            success = converter.convert_file(args.input, args.output)
            if not success:
                sys.exit(1)
        
        elif Path(args.input).is_dir():
            # Convert directory
            converted_files = converter.convert_directory(args.input, args.output)
            if not converted_files:
                sys.exit(1)
            
            console.print(f"\n[bold green]Successfully converted {len(converted_files)} files![/bold green]")
        
        else:
            console.print(f"[red]Input path does not exist: {args.input}[/red]")
            sys.exit(1)
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
