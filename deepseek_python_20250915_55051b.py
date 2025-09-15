import streamlit as st
import os
import base64
import io

# Try to import required packages with error handling
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("python-dotenv not installed. Using environment variables directly.")

try:
    import google.generativeai as genai
    from PIL import Image 
    import pdf2image
    
    # Configure Gemini AI if API key is available
    if os.getenv("GOOGLE_API_KEY"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    elif 'GOOGLE_API_KEY' in st.secrets:
        genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    else:
        st.warning("Google API key not found. Please set GOOGLE_API_KEY in secrets or environment variables.")
        
except ImportError as e:
    st.error(f"Missing required package: {e}. Please check your requirements.txt file.")
    st.stop()

def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error getting response from Gemini: {str(e)}"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Convert the PDF to image
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            first_page = images[0]

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
            return pdf_parts
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None
    else:
        st.error("No file uploaded")
        return None

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.header("📄 ATS Resume Tracking System")
st.write("Analyze how well your resume matches a job description using AI")

# Initialize session state
if 'resume_uploaded' not in st.session_state:
    st.session_state.resume_uploaded = False

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Job Description")
    input_text = st.text_area("Paste the job description here:", height=200, key="input")
    
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.session_state.resume_uploaded = True
        st.success("✅ PDF Uploaded Successfully")

with col2:
    st.subheader("Analysis Options")
    
    if st.session_state.resume_uploaded:
        submit1 = st.button("📋 Tell Me About the Resume", use_container_width=True)
        submit3 = st.button("📊 Percentage Match Analysis", use_container_width=True)
        
        input_prompt1 = """
        You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        Be specific and provide actionable feedback.
        """
        
        input_prompt3 = """
        You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of data science and ATS functionality. 
        Your task is to evaluate the resume against the provided job description. 
        Provide:
        1. Percentage match between resume and job description
        2. Missing keywords from the job description
        3. Final thoughts and recommendations for improvement
        
        Format your response clearly with sections for each part.
        """
        
        if submit1:
            with st.spinner("Analyzing resume..."):
                pdf_content = input_pdf_setup(uploaded_file)
                if pdf_content:
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                    st.subheader("Analysis Results")
                    st.write(response)
        
        elif submit3:
            with st.spinner("Calculating match percentage..."):
                pdf_content = input_pdf_setup(uploaded_file)
                if pdf_content:
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                    st.subheader("Match Analysis")
                    st.write(response)
    else:
        st.info("👆 Upload a resume PDF to get started with analysis")

st.markdown("---")
st.markdown("### 💡 Tips")
st.markdown("""
- Upload a PDF version of your resume
- Copy and paste the complete job description for accurate analysis
- Use both analysis options for comprehensive feedback
""")