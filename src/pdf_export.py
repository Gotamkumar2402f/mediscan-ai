"""Generate PDF report from chat history."""
from fpdf import FPDF
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(0, 150, 200)
        self.cell(0, 10, 'MediScan AI - Clinical Report', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Educational information only. Not a medical diagnosis.', 0, 0, 'C')

def generate_pdf(chat_history: list, out_path: str):
    """Generate PDF from chat list."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for turn in chat_history:
        # Question
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 8, f"Q: {turn['q']}")
        pdf.ln(2)
        
        # Answer (Strip markdown formatting for cleaner PDF)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        clean_answer = turn['a'].replace('**', '').replace('*', '')
        pdf.multi_cell(0, 6, f"A: {clean_answer}")
        pdf.ln(8)
        
    pdf.output(out_path)
    return out_path