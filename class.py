import streamlit as st
import pandas as pd
from google.cloud import documentai_v1 as documentai
import os
from PIL import Image
import io
import fitz  # PyMuPDF
import tempfile

# Set page config
st.set_page_config(page_title="Tax Form Classifier", layout="wide")

class DocumentClassifier:
    def __init__(self, project_id, location, processor_id):
        self.client = documentai.DocumentProcessorServiceClient()
        self.name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    def process_document(self, content):
        document = {"content": content, "mime_type": "application/pdf"}
        request = documentai.ProcessRequest(
            name=self.name,
            document=document
        )
        result = self.client.process_document(request=request)
        return result.document

def convert_pdf_to_images(pdf_bytes):
    images = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        for page in pdf:
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            images.append(Image.open(io.BytesIO(img_bytes)))
    return images

def main():
    st.title("Tax Form Classifier")
    st.sidebar.header("Configuration")

    # Sidebar configuration
    project_id = st.sidebar.text_input("Project ID", "your-project-id")
    location = st.sidebar.text_input("Location", "us")
    processor_id = st.sidebar.text_input("Processor ID", "your-processor-id")

    # Initialize classifier
    classifier = DocumentClassifier(project_id, location, processor_id)

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
                    
                    # Create metrics
                    classification = result.entities[0].type_ if result.entities else "Unknown"
                    confidence = result.entities[0].confidence if result.entities else 0.0
                    
                    # Display metrics
                    col2_1, col2_2 = st.columns(2)
                    with col2_1:
                        st.metric("Document Type", classification)
                    with col2_2:
                        st.metric("Confidence", f"{confidence:.2%}")
                    
                    # Display detailed results
                    st.subheader("Detailed Analysis")
                    if result.entities:
                        df = pd.DataFrame([
                            {
                                "Type": entity.type_,
                                "Confidence": f"{entity.confidence:.2%}",
                                "Text": entity.text_anchor.content if entity.text_anchor else ""
                            }
                            for entity in result.entities
                        ])
                        st.dataframe(df)
                    
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

    # Display usage instructions
    if not uploaded_file:
        st.info("""
        👆 Upload a tax form PDF to get started!
        
        This application will:
        - Display a preview of the document
        - Classify the document type
        - Show confidence scores
        - Provide detailed analysis
        """)

    # Add footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        """
        This app uses Google Cloud Document AI to classify tax forms.
        
        Supported document types:
        - Form 1040
        - Schedule 1
        - Schedule 2
        - Other supporting documents
        """
    )

if __name__ == "__main__":
    main()
