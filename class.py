import streamlit as st
import random
import pandas as pd
from datetime import datetime
import io
import base64
import zipfile
from PyPDF2 import PdfMerger  # Ensure PyPDF2 is installed
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
    def generate_pdf(self, form_data, form_number, form_type, year):
        if not REPORTLAB_INSTALLED:
            st.error("Cannot generate PDF: ReportLab is not installed")
            return None
            
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Common header for all forms
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 750, f"Tax Form {form_type} - {form_number}")
        c.setFont("Helvetica", 10)

        # Generate Form 1040
        if form_type == "1040":
            self._generate_1040(c, form_data, year)
        
        # Generate Schedule 1
        elif form_type == "schedule1":
            self._generate_schedule1(c, form_data, year)
        
        # Generate Schedule 2
        elif form_type == "schedule2":
            self._generate_schedule2(c, form_data, year)
        
        c.save()
        buffer.seek(0)
        return buffer
        
    def _generate_1040(self, c, data, year):
        # Header Section
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 730, f"Form 1040 - U.S. Individual Income Tax Return")
        
        # Tax Year Field
        c.setFont("Helvetica", 10)
        c.drawString(50, 710, f"Tax Year: {year}")
        
        # Filing Status Section
        c.setFont("Helvetica", 10)
        c.drawString(50, 690, "Filing Status:")
        c.drawString(150, 690, f"Single: {random.choice([True, False])}")
        c.drawString(150, 670, f"Married: {random.choice([True, False])}")
        
        # Personal Information Section
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 650, "Personal Information")
        c.setFont("Helvetica", 10)
        c.drawString(50, 630, f"First Name: {data['first_name']}")
        c.drawString(50, 610, f"Last Name: {data['last_name']}")
        c.drawString(50, 590, f"SSN: XXX-XX-{data['ssn_last4']}")
        
        # Income Section
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 570, "Income")
        c.setFont("Helvetica", 10)
        c.drawString(50, 550, f"Wages: ${data['wages']:,.2f}")
        c.drawString(50, 530, f"Interest: ${data['interest']:,.2f}")

        # Deductions Section
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 510, "Deductions")
        c.setFont("Helvetica", 10)

        # Set standard deduction for each year
        if year == 2023:
            standard_deduction = 12950
        elif year == 2024:
            standard_deduction = 13000  # Hypothetical increase for 2024
        else:
            # Default value or handle for other years
            standard_deduction = 12500  # Example default value

        c.drawString(50, 490, f"Standard Deduction for {year}: ${standard_deduction}")
        
        # Taxes and Credits Section
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 470, "Taxes and Credits")
        c.setFont("Helvetica", 10)
        c.drawString(50, 450, f"Taxable Income: ${data['wages'] + data['interest']:,.2f}")
        
        # Signature Section
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 430, "Signature")
        c.setFont("Helvetica", 10)
        c.drawString(50, 410, f"Signature: ______________________")
        c.drawString(50, 390, f"Date: {datetime.now().strftime('%m/%d/%Y')}")
        
    def _generate_schedule1(self, c, data, year):
        y = 700
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Schedule 1: Additional Income and Adjustments to Income ({year})")
        
        # Business Income
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Business Income: ${data['business_income']:,.2f}")
        
        # Rental Income
        y -= 20
        c.drawString(50, y, f"Rental Income: ${data['rental_income']:,.2f}")
        
    def _generate_schedule2(self, c, data, year):
        y = 700
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Schedule 2: Additional Taxes ({year})")
        
        # Self-Employment Tax
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Self-Employment Tax: ${data['self_employment_tax']:,.2f}")
        
        # Medicare Tax
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
    st.title("Generate 50 Separate Tax Forms PDFs (Form 1040, Schedule 1, and Schedule 2 per Case)")
    
    if not REPORTLAB_INSTALLED:
        st.stop()
    
    generator = PDFGenerator()

    # Button to generate 50 PDFs for each form for three years
    if st.button("Generate 50 PDFs for Each Year"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for year in range(2022, 2025):  # Loop for the past 3 years (2022, 2023, 2024)
                for i in range(1, 51):  # Generate 50 PDFs for each year
                    form_data = generate_random_data()  # Generate random data for each form
                    
                    # Generate Form 1040 PDF
                    pdf_buffer_1040 = generator.generate_pdf(form_data["1040"], i, "1040", year)
                    zip_file.writestr(f"form_1040_{year}_{i}.pdf", pdf_buffer_1040.getvalue())
                    
                    # Generate Schedule 1 PDF
                    pdf_buffer_schedule1 = generator.generate_pdf(form_data["schedule1"], i, "schedule1", year)
                    zip_file.writestr(f"schedule1_{year}_{i}.pdf", pdf_buffer_schedule1.getvalue())
                    
                    # Generate Schedule 2 PDF
                    pdf_buffer_schedule2 = generator.generate_pdf(form_data["schedule2"], i, "schedule2", year)
                    zip_file.writestr(f"schedule2_{year}_{i}.pdf", pdf_buffer_schedule2.getvalue())

        zip_buffer.seek(0)
        b64_zip = base64.b64encode(zip_buffer.read()).decode("utf-8")
        zip_filename = f"tax_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

        # Create download link for the ZIP file
        href = f'<a href="data:application/zip;base64,{b64_zip}" download="{zip_filename}">Download 150 PDFs</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("50 PDFs for each form, for the past 3 years, generated successfully!")

if __name__ == "__main__":
    main()

