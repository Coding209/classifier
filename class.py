import streamlit as st
import pandas as pd
from datetime import datetime
import io
import base64

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
    def generate_pdf(self, form_data):
        if not REPORTLAB_INSTALLED:
            st.error("Cannot generate PDF: ReportLab is not installed")
            return None
            
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Common header for all forms
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 750, "Tax Forms")
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

def main():
    st.title("Tax Forms PDF Generator")
    
    if not REPORTLAB_INSTALLED:
        st.stop()
    
    generator = PDFGenerator()
    
    # Form Fields
    with st.form(key='form_generator'):
        # Form 1040 Fields
        first_name = st.text_input("First Name", "John")
        last_name = st.text_input("Last Name", "Doe")
        ssn_last4 = st.text_input("Last 4 of SSN", "1234")
        wages = st.number_input("Wages", value=50000.0)
        interest = st.number_input("Interest Income", value=1000.0)

        # Schedule 1 Fields
        business_income = st.number_input("Business Income", value=10000.0)
        rental_income = st.number_input("Rental Income", value=5000.0)

        # Schedule 2 Fields
        self_employment_tax = st.number_input("Self-Employment Tax", value=2000.0)
        medicare_tax = st.number_input("Medicare Tax", value=1000.0)
        
        generate_button = st.form_submit_button("Generate PDF")

    if generate_button:
        # Organize data into a dictionary
        form_data = {
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

        with st.spinner("Generating PDF..."):
            try:
                pdf_buffer = generator.generate_pdf(form_data)
                if pdf_buffer:
                    # Create download button
                    b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
                    filename = f"tax_forms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}">Download PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("PDF generated successfully!")
                    
                    # Save metadata
                    metadata = {
                        "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "filename": filename
                    }
                    st.json(metadata)
                    
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    main()
