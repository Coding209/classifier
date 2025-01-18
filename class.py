import streamlit as st
import random
import pandas as pd
from datetime import datetime
import io
import base64
import zipfile
import os

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_INSTALLED = True
except ImportError:
    REPORTLAB_INSTALLED = False
    st.error("""
    ReportLab is not installed. Please install it using:
    ```
    pip install reportlab
    ```
    """)

class PDFGenerator:
    def generate_pdf(self, form_data, form_number):
        if not REPORTLAB_INSTALLED:
            st.error("Cannot generate PDF: ReportLab is not installed")
            return None
            
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Common header for all forms
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 750, f"Tax Form {form_number}")
        c.setFont("Helvetica", 12)

        # Generate Form 1040
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, 730, "Form 1040")
        c.setFont("Helvetica", 12)
        self._generate_1040(c, form_data['1040'])
        
        # Add page break
        c.showPage()

        # Generate Schedule 1
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, 730, "Schedule 1")
        c.setFont("Helvetica", 12)
        self._generate_schedule1(c, form_data['schedule1'])
        
        # Add page break
        c.showPage()

        # Generate Schedule 2
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, 730, "Schedule 2")
        c.setFont("Helvetica", 12)
        self._generate_schedule2(c, form_data['schedule2'])
        
        c.save()
        buffer.seek(0)
        return buffer
        
    def _generate_1040(self, c, data):
        # Personal Information
        y = 700
        c.drawString(50, y, "Personal Information")
        y -= 20
        c.drawString(50, y, f"First Name: {data['first_name']}")
        c.drawString(300, y, f"Last Name: {data['last_name']}")
        y -= 20
        c.drawString(50, y, f"SSN: XXX-XX-{data['ssn_last4']}")
        
        # Financial Information
        y -= 40
        c.drawString(50, y, "Financial Information")
        y -= 20
        c.drawString(50, y, f"Wages: ${data['wages']:,.2f}")
        y -= 20
        c.drawString(50, y, f"Interest: ${data['interest']:,.2f}")
        
    def _generate_schedule1(self, c, data):
        y = 700
        c.drawString(50, y, "Additional Income")
        y -= 20
        c.drawString(50, y, f"Business Income: ${data['business_income']:,.2f}")
        y -= 20
        c.drawString(50, y, f"Rental Income: ${data['rental_income']:,.2f}")
        
    def _generate_schedule2(self, c, data):
        y = 700
        c.drawString(50, y, "Additional Taxes")
        y -= 20
        c.drawString(50, y, f"Self-Employment Tax: ${data['self_employment_tax']:,.2f}")
        y -= 20
        c.drawString(50, y, f"Medicare Tax: ${data['medicare_tax']:,.2f}")

def generate_random_data():
    # Generate random data for each form
    first_name = random.choice(["John", "Jane", "Alex", "Chris", "Sam", "Taylor"])
    last_name = random.choice(["Doe", "Smith", "Johnson", "Williams", "Brown", "Davis"])
    ssn_last4 = random.randint(1000, 9999)
    wages = round(random.uniform(25000, 150000), 2)
    interest = round(random.uniform(500, 5000), 2)
    business_income = round(random.uniform(1000, 50000), 2)
    rental_income = round(random.uniform(1000, 20000), 2)
    self_employment_tax = round(random.uniform(1000, 5000), 2)
    medicare_tax = round(random.uniform(500, 2500), 2)

    return {
        "1040": {
            "first_name": first_name,
            "last_name": last_name,
            "ssn_last4": ssn_last4,
            "wages": wages,
            "interest": interest
        },
        "schedule1": {
            "business_income": business_income,
            "rental_income": rental_income
        },
        "schedule2": {
            "self_employment_tax": self_employment_tax,
            "medicare_tax": medicare_tax
        }
    }

def main():
    st.title("Generate 200 Tax Forms PDF")
    
    if not REPORTLAB_INSTALLED:
        st.stop()
    
    generator = PDFGenerator()

    # Button to generate 200 PDFs
    if st.button("Generate 200 PDFs"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(1, 201):
                form_data = generate_random_data()  # Generate random data for each form
                pdf_buffer = generator.generate_pdf(form_data, i)
                pdf_filename = f"tax_form_{i}.pdf"
                zip_file.writestr(pdf_filename, pdf_buffer.getvalue())

        zip_buffer.seek(0)
        b64_zip = base64.b64encode(zip_buffer.read()).decode("utf-8")
        zip_filename = f"tax_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

        # Create download link for the ZIP file
        href = f'<a href="data:application/zip;base64,{b64_zip}" download="{zip_filename}">Download 200 PDFs</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("200 PDFs generated successfully!")

if __name__ == "__main__":
    main()
