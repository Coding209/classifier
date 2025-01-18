import streamlit as st
import pandas as pd
from PIL import Image
import io
import fitz  # PyMuPDF
import tempfile
import os

# Set page config
st.set_page_config(page_title="Tax Form Classifier", layout="wide")

class MockClassifier:
    """Mock classifier for testing without Document AI"""
    def process_document(self, content):
        # Return mock classification results
        return {
            "type": "Form 1040",
            "confidence": 0.95,
            "details": [
                {"type": "Form 1040", "confidence": 0.95},
                {"type": "Schedule 1", "confidence": 0.03},
                {"type": "Schedule 2", "confidence": 0.02}
            ]
        }

def convert_pdf_to_images(pdf_bytes):
    """Convert PDF bytes to list of PIL Images"""
    images = []
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            for page in pdf:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                images.append(Image.open(io.BytesIO(img_bytes)))
    except Exception as e:
        st.error(f"Error converting PDF: {str(e)}")
    return images

def main():
    st.title("Tax Form Classifier")
    
    # Initialize mock classifier
    classifier = MockClassifier()

    # Add tabs
    tab1, tab2 = st.tabs(["Single Document", "Batch Processing"])

    with tab1:
        # File upload
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file:
            # Create columns for display
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Document Preview")
                pdf_bytes = uploaded_file.read()
                images = convert_pdf_to_images(pdf_bytes)
                
                # Display first page
                if images:
                    st.image(images[0], use_column_width=True)
                    
                    if len(images) > 1:
                        st.info(f"Document has {len(images)} pages. Showing first page.")

            with col2:
                st.subheader("Classification Results")
                
                with st.spinner("Processing document..."):
                    try:
                        # Process document
                        result = classifier.process_document(pdf_bytes)
                        
                        # Display classification results
                        st.success("Document processed successfully!")
                        
                        # Display metrics
                        col2_1, col2_2 = st.columns(2)
                        with col2_1:
                            st.metric("Document Type", result["type"])
                        with col2_2:
                            st.metric("Confidence", f"{result['confidence']:.2%}")
                        
                        # Display detailed results
                        st.subheader("Detailed Analysis")
                        df = pd.DataFrame(result["details"])
                        df["confidence"] = df["confidence"].apply(lambda x: f"{x:.2%}")
                        st.dataframe(df)
                        
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")

    with tab2:
        st.subheader("Batch Processing")
        uploaded_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)
        
        if uploaded_files:
            st.write(f"Processing {len(uploaded_files)} files...")
            
            # Create summary table
            results = []
            for file in uploaded_files:
                result = classifier.process_document(file.read())
                results.append({
                    "Filename": file.name,
                    "Type": result["type"],
                    "Confidence": f"{result['confidence']:.2%}"
                })
            
            df = pd.DataFrame(results)
            st.dataframe(df)
            
            # Add download button
            csv = df.to_csv(index=False)
            st.download_button(
                "Download Results",
                csv,
                "classification_results.csv",
                "text/csv",
                key='download-csv'
            )

    # Display usage instructions
    if not uploaded_file and not uploaded_files:
        st.info("""
        👆 Upload a tax form PDF to get started!
        
        This application will:
        - Display a preview of the document
        - Classify the document type
        - Show confidence scores
        - Provide detailed analysis
        
        You can use either:
        - Single Document mode for individual files
        - Batch Processing for multiple files
        """)

    # Add footer
    st.sidebar.markdown("### About")
    st.sidebar.info(
        """
        This app classifies tax forms into categories:
        - Form 1040
        - Schedule 1
        - Schedule 2
        - Other supporting documents
        """
    )

if __name__ == "__main__":
    main()
