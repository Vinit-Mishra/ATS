# ATS Resume Expert

An AI-powered application that analyzes resumes against job descriptions using Google's Gemini AI. Get instant feedback on how well your resume matches a job posting.

## Features

- 📄 Resume analysis against job descriptions
- 📊 Percentage match calculation
- 🔍 Missing keywords identification
- 💡 Actionable improvement suggestions

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your Google API key in Streamlit secrets (for deployment)

## Deployment on Streamlit

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and connect your GitHub repository
4. Set up your secrets in Streamlit Cloud:
   - Go to your app settings → Secrets
   - Add your Google API key:
     ```
     GOOGLE_API_KEY = "your_actual_api_key_here"
     ```
5. Deploy!

## Local Development

1. Create a `.env` file in the root directory
2. Add your Google API key: