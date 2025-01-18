import streamlit as st
import pandas as pd
from datetime import datetime
import json

class SimpleFormGenerator:
    def generate_form_data(self, form_type, form_data):
        """Generate form data in JSON format"""
        data = {
            "form_type": form_type,
            "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": form_data
        }
        return json.dumps(data, indent=2)

def main():
    st.set_page_config(page_title="Tax Form Data Generator", layout="wide")
    st.title("Tax Form Data Generator")

    # Initialize generator
    generator = SimpleFormGenerator()

    # Sidebar for batch generation
    st.sidebar.header("Batch Generation")
    num_forms = st.sidebar.number_input("Number of Forms", min_value=1, max_value=100, value=1)
    
    # Main content
    tab1, tab2 = st.tabs(["Single Form", "Batch Generation"])

    with tab1:
        st.header("Generate Single Form Data")
        
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

            submit_button = st.form_submit_button("Generate Form Data")

        if submit_button:
            # Generate JSON data
            json_data = generator.generate_form_data(form_type, form_data)
            
            # Display generated data
            st.subheader("Generated Form Data")
            st.code(json_data, language='json')
            
            # Create download button for JSON
            st.download_button(
                "Download JSON",
                json_data,
                f"{form_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
            
            # Display success message
            st.success(f"{form_type.upper()} form data generated successfully!")

    with tab2:
        st.header("Batch Generation")
        
        if st.button("Generate Batch"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create a DataFrame to store metadata and generated data
            all_data = []
            
            for i in range(num_forms):
                # Generate random data
                form_type = ["1040", "schedule1", "schedule2"][i % 3]
                
                if form_type == "1040":
                    form_data = {
                        "first_name": f"User{i}",
                        "last_name": f"Sample{i}",
                        "ssn_last4": f"{i:04d}",
                        "wages": 50000 + i * 1000,
                        "interest": 1000 + i * 100
                    }
                elif form_type == "schedule1":
                    form_data = {
                        "business_income": 10000 + i * 500,
                        "rental_income": 5000 + i * 200
                    }
                else:
                    form_data = {
                        "self_employment_tax": 2000 + i * 100,
                        "medicare_tax": 1000 + i * 50
                    }
                
                # Generate form data
                json_data = generator.generate_form_data(form_type, form_data)
                
                # Save to list
                all_data.append({
                    "form_id": i + 1,
                    "form_type": form_type,
                    "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "data": json_data
                })
                
                # Update progress
                progress = (i + 1) / num_forms
                progress_bar.progress(progress)
                status_text.text(f"Generated {i + 1} of {num_forms} forms...")
            
            # Create DataFrame
            df = pd.DataFrame(all_data)
            
            # Display summary
            st.success(f"Generated {num_forms} forms successfully!")
            st.subheader("Generation Summary")
            st.dataframe(df[["form_id", "form_type", "generation_date"]])
            
            # Download options
            st.subheader("Download Options")
            
            # Download all data as JSON
            all_json = json.dumps(all_data, indent=2)
            st.download_button(
                "Download All Data (JSON)",
                all_json,
                "form_data_batch.json",
                "application/json"
            )
            
            # Download summary as CSV
            csv = df[["form_id", "form_type", "generation_date"]].to_csv(index=False)
            st.download_button(
                "Download Summary (CSV)",
                csv,
                "form_generation_summary.csv",
                "text/csv",
                key='download-csv'
            )

if __name__ == "__main__":
    main()
