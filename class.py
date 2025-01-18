import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import pandas as pd
from datetime import datetime
import io
import base64

class TaxFormGenerator:
    def generate_form(self, form_type, form_data):
        """Generate a tax form based on type and data"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        if form_type == "1040":
            c.drawString(250, 750, "Form 1040")
            c.setFont("Helvetica", 12)
            c.drawString(250, 730, "U.S. Individual Income Tax Return")
            self._add_1040_content(c, form_data)
        elif form_type == "schedule1":
            c.drawString(250, 750, "Schedule 1")
            c.setFont("Helvetica", 12)
            c.drawString(200, 730, "Additional Income and Adjustments to Income")
            self._add_schedule1_content(c, form_data)
        elif form_type == "schedule2":
            c.drawString(250, 750, "Schedule 2")
            c.setFont("Helvetica", 12)
            c.drawString(200, 730, "Additional Taxes")
            self._add_schedule2_content(c, form_data)
            
        c.save()
        buffer.seek(0)
        return buffer

    def _add_1040_content(self, c, data):
        """Add Form 1040 specific content"""
        c.setFont("Helvetica", 10)
        y_position = 700
        
        # Personal Information
        c.drawString(50, y_position, f"First Name: {data.get('first_name', '')}")
        c.drawString(300, y_position, f"Last Name: {data.get('last_name', '')}")
        
        y_position -= 20
        c.drawString(50, y_position, f"SSN: XXX-XX-{data.get('ssn_last4', '')}")
        
        # Financial Information
        y_position -= 40
        c.drawString(50, y_position, "Income")
        y_position -= 20
        c.drawString(70, y_position, f"Wages: ${data.get('wages', '0')}")
        y_position -= 20
        c.drawString(70, y_position, f"Interest: ${data.get('interest', '0')}")

    def _add_schedule1_content(self, c, data):
        """Add Schedule 1 specific content"""
        c.setFont("Helvetica", 10)
        y_position = 700
        
        # Additional Income
        c.drawString(50, y_position, "Additional Income")
        y_position -= 20
        c.drawString(70, y_position, f"Business Income: ${data.get('business_income', '0')}")
        y_position -= 20
        c.drawString(70, y_position, f"Rental Income: ${data.get('rental_income', '0')}")

    def _add_schedule2_content(self, c, data):
        """Add Schedule 2 specific content"""
        c.setFont("Helvetica", 10)
        y_position = 700
        
        # Additional Taxes
        c.drawString(50, y_position, "Additional Taxes")
        y_position -= 20
        c.drawString(70, y_position, f"Self-Employment Tax: ${data.get('self_employment_tax', '0')}")
        y_position -= 20
        c.drawString(70, y_position, f"Additional Medicare Tax: ${data.get('medicare_tax', '0')}")

def create_download_link(buffer, filename):
    """Create a download link for the PDF"""
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF</a>'

def main():
    st.set_page_config(page_title="Tax Form Generator", layout="wide")
    st.title("Tax Form Generator")

    # Initialize form generator
    generator = TaxFormGenerator()

    # Sidebar for batch generation
    st.sidebar.header("Batch Generation")
    num_forms = st.sidebar.number_input("Number of Forms", min_value=1, max_value=100, value=1)
    
    # Main content
    tab1, tab2 = st.tabs(["Single Form", "Batch Generation"])

    with tab1:
        st.header("Generate Single Form")
        
        # Form selection
        form_type = st.selectbox(
            "Select Form Type",
            ["1040", "schedule1", "schedule2"]
        )
        
        # Form data input
        with st.form("tax_form_data"):
            st.subheader("Form Information")
            
            if form_type == "1040":
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name", "John")
                    ssn_last4 = st.text_input("Last 4 SSN", "1234")
                    wages = st.number_input("Wages", 0, 1000000, 50000)
                with col2:
                    last_name = st.text_input("Last Name", "Doe")
                    interest = st.number_input("Interest Income", 0, 100000, 1000)
                
                form_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "ssn_last4": ssn_last4,
                    "wages": wages,
                    "interest": interest
                }
                
            elif form_type == "schedule1":
                business_income = st.number_input("Business Income", 0, 1000000, 10000)
                rental_income = st.number_input("Rental Income", 0, 1000000, 5000)
                
                form_data = {
                    "business_income": business_income,
                    "rental_income": rental_income
                }
                
            elif form_type == "schedule2":
                self_employment_tax = st.number_input("Self-Employment Tax", 0, 100000, 2000)
                medicare_tax = st.number_input("Additional Medicare Tax", 0, 50000, 1000)
                
                form_data = {
                    "self_employment_tax": self_employment_tax,
                    "medicare_tax": medicare_tax
                }

            submit_button = st.form_submit_button("Generate Form")

        if submit_button:
            # Generate PDF
            pdf_buffer = generator.generate_form(form_type, form_data)
            
            # Create download button
            filename = f"{form_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            st.markdown(create_download_link(pdf_buffer, filename), unsafe_allow_html=True)
            
            # Display success message
            st.success(f"{form_type.upper()} form generated successfully!")

    with tab2:
        st.header("Batch Generation")
        
        if st.button("Generate Batch"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create a DataFrame to store metadata
            metadata = []
            
            for i in range(num_forms):
                # Generate random data
                form_data = {
                    "first_name": f"User{i}",
                    "last_name": f"Sample{i}",
                    "ssn_last4": f"{i:04d}",
                    "wages": 50000 + i * 1000,
                    "interest": 1000 + i * 100
                }
                
                # Generate form
                form_type = ["1040", "schedule1", "schedule2"][i % 3]
                pdf_buffer = generator.generate_form(form_type, form_data)
                
                # Save metadata
                metadata.append({
                    "form_id": i + 1,
                    "form_type": form_type,
                    "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # Update progress
                progress = (i + 1) / num_forms
                progress_bar.progress(progress)
                status_text.text(f"Generated {i + 1} of {num_forms} forms...")
            
            # Create metadata DataFrame
            df = pd.DataFrame(metadata)
            
            # Display summary
            st.success(f"Generated {num_forms} forms successfully!")
            st.subheader("Generation Summary")
            st.dataframe(df)
            
            # Download metadata
            csv = df.to_csv(index=False)
            st.download_button(
                "Download Metadata",
                csv,
                "form_generation_metadata.csv",
                "text/csv",
                key='download-csv'
            )

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
