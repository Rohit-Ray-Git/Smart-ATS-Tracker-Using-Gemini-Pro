import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def calculate_ats_score(resume_text, jd, missing_keywords):
    # Weight definitions
    weights = {
        "keyword_match": 0.4,
        "skills_alignment": 0.3,
        "formatting": 0.2,
        "profile_strength": 0.1,
    }

    # Keyword Match
    keywords_provided = jd.lower().split()  # Simplified splitting; consider advanced keyword extraction
    keywords_in_resume = resume_text.lower().split()
    keyword_match_score = 100 * (1 - len(missing_keywords) / len(keywords_provided)) if keywords_provided else 0

    # Extract skills dynamically from the job description using the model
    skills_prompt = f"""
    Extract a list of required skills from the following job description:
    {jd}

    Provide the response in the format:
    ["skill1", "skill2", "skill3", ...]
    """
    skills_response = get_gemini_response(skills_prompt)

    try:
        # Parse the skills extracted by the model
        skills_in_jd = eval(skills_response)
        if not isinstance(skills_in_jd, list):
            raise ValueError("Skills extraction failed.")
    except Exception as e:
        st.warning("Could not extract skills dynamically. Falling back to default skills.")
        skills_in_jd = ["python", "sql", "data analysis", "machine learning", "communication"]  # Default example skills

    # Compare extracted skills with those in the resume
    matched_skills = [skill for skill in skills_in_jd if skill.lower() in resume_text.lower()]
    skills_alignment_score = 100 * len(matched_skills) / len(skills_in_jd) if skills_in_jd else 0

    # 3. Formatting (check for ATS issues like tables or images)
    formatting_issues = ["table", "graphic", "image"]  # Example of forbidden formatting keywords
    formatting_score = 100 if all(item not in resume_text.lower() for item in formatting_issues) else 50

    # 4. Profile Strength (evaluate profile summary length and relevance)
    profile_length = len(resume_text.split())
    profile_strength_score = 100 if 50 <= profile_length <= 200 else 70 if profile_length > 200 else 50

    # Calculate the overall score
    overall_score = (
        weights["keyword_match"] * keyword_match_score
        + weights["skills_alignment"] * skills_alignment_score
        + weights["formatting"] * formatting_score
        + weights["profile_strength"] * profile_strength_score
    )   

    return round(overall_score, 2), {
        "Keyword Match": round(keyword_match_score, 2),
        "Skills Alignment": round(skills_alignment_score, 2),
        "Formatting": round(formatting_score, 2),
        "Profile Strength": round(profile_strength_score, 2),
    }

def suggest_keywords(missing_keywords):
    suggestions = [kw + " (consider related terms)" for kw in missing_keywords]
    return suggestions

def plot_score(jd_match):
    data = {"Match": jd_match, "Missing": 100 - jd_match}
    fig = px.pie(
        values=data.values(), 
        names=data.keys(), 
        title="JD Match Breakdown",
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig)

def generate_word_cloud(keywords):
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(keywords))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

def generate_pdf(jd_match, missing_keywords, profile_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"JD Match: {jd_match}", ln=True)
    pdf.cell(200, 10, txt="Missing Keywords:", ln=True)
    for kw in missing_keywords:
        pdf.cell(200, 10, txt=f"- {kw}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Profile Summary:", ln=True)
    pdf.multi_cell(0, 10, profile_summary)
    file_path = "resume_analysis_report.pdf"
    pdf.output(file_path)
    return file_path

def calculate_similarity(jd, resume):
    vectorizer = TfidfVectorizer().fit_transform([jd, resume])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100

# Function to read and encode the image file
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Set the background image using CSS
def set_background(image_base64):
    page_bg_img = f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }}
    .css-1g8v9l0 {{
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
    }}
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        color: white;
    }}
    .stButton > button {{
        background-color: #4C4C6D;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }}
    .stButton > button:hover {{
        background-color: #6A5ACD;
    }}
    .stSlider > div {{
        background-color: transparent;
    }}
    /* Center title and sub-heading */
    .stTitle {{
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }}
    .stSubheader {{
        text-align: center;
        font-size: 24px;
        margin-top: 10px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit App UI
st.set_page_config(page_title="Smart ATS Tracker", layout="wide")
st.markdown("<h1 class='stTitle'>Smart ATS Tracker - Gemini Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='stSubheader'>Improve Your Resume's ATS Compatibility</h3>", unsafe_allow_html=True)

# Set background image
image_base64 = get_base64_image("img5.jpg")  # Replace with your image path
set_background(image_base64)

# Input Sections
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type='pdf', help='Please upload your resume in PDF format.')
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = f"""
        Hey Act Like a skilled or very experience ATS(Application Tracking System)
        with a deep understanding of tech field,software engineering,data science ,data analyst
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide 
        best assistance for improving thr resumes. Assign the percentage Matching based 
        on Jd and
        the missing keywords with high accuracy
        resume:{resume_text}
        description:{jd}

        Provide the response in the format:
        {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
        """

        response_text = get_gemini_response(input_prompt)
        response = eval(response_text)  # Parse the response as a dictionary

        # Define missing_keywords
        missing_keywords = response["MissingKeywords"]

        # Tabs for Display
        tabs = st.tabs(["Analysis", "Keyword Suggestions", "Resume Tips", "Word Cloud", "Overall ATS Score Analysis"])

        with tabs[0]:
            st.header("Job Description Analysis")
            jd_match = int(response["JD Match"].strip('%'))
            st.write(f"**JD Match Percentage:** {jd_match}%")
            plot_score(jd_match)

        with tabs[1]:
            st.header("Keyword Suggestions")
            suggestions = suggest_keywords(response["MissingKeywords"])
            st.write("**Missing Keywords:**", response["MissingKeywords"])
            st.write("**Suggestions:**", suggestions)

        with tabs[2]:
            st.header("Resume Tips")
            tips_prompt = f"""
            Act like a resume improvement expert. Based on the provided job description and resume, suggest 3 to 5 tips to improve the resume for better ATS compatibility.
            Resume: {resume_text}
            Job Description: {jd}
            Provide the response as a bullet-point list.
            """
            tips_response = get_gemini_response(tips_prompt)
            st.write(tips_response)

        with tabs[3]:
            st.header("Word Cloud")
            generate_word_cloud(response["MissingKeywords"])

        with tabs[4]:  # Add a new tab for ATS Score
            st.header("ATS Score Analysis")
            
            if resume_text and jd:
                st.info("Calculating your ATS score...")
                
                # Calculate ATS score
                ats_score, score_breakdown = calculate_ats_score(resume_text, jd, missing_keywords)

                # Display Overall Score
                st.metric(label="Overall ATS Score", value=f"{ats_score}%", delta=None)

                # Display Breakdown
                st.markdown("### Score Breakdown:")
                for component, score in score_breakdown.items():
                    st.write(f"**{component}:** {score}%")

                # Visualize Weighted Pie Chart
                weights = {
                    "keyword_match": 0.4,
                    "skills_alignment": 0.3,
                    "formatting": 0.2,
                    "profile_strength": 0.1,
                }

                weighted_scores = {
                    "Keyword Match": weights["keyword_match"] * score_breakdown["Keyword Match"],
                    "Skills Alignment": weights["skills_alignment"] * score_breakdown["Skills Alignment"],
                    "Formatting": weights["formatting"] * score_breakdown["Formatting"],
                    "Profile Strength": weights["profile_strength"] * score_breakdown["Profile Strength"],
                }

                # Normalize scores
                total_weighted_score = sum(weighted_scores.values())
                normalized_scores = {k: (v / total_weighted_score) * 100 for k, v in weighted_scores.items()}

                fig = px.pie(
                    names=normalized_scores.keys(),
                    values=normalized_scores.values(),
                    title="ATS Score Breakdown (Weighted)",
                    hole=0.3,
                )
                fig.update_traces(textinfo='percent+label')
                st.plotly_chart(fig)

                # Summary Explanation
                st.sidebar.title("Understanding the Scores")
                st.sidebar.write("### Keyword Match")
                st.sidebar.write("Measures how well your resume matches the job description's keywords. A higher percentage indicates fewer missing keywords.")
                st.sidebar.write("### Skills Alignment")
                st.sidebar.write("Reflects the match between the required skills in the job description and those listed in your resume. Aim for higher alignment.")
                st.sidebar.write("### Formatting")
                st.sidebar.write("Ensures your resume is ATS-friendly (e.g., no images, tables, or unusual formatting issues).")
                st.sidebar.write("### Profile Strength")
                st.sidebar.write("Evaluates the overall quality and relevance of your resume, including its length and the presence of key sections like a summary.")
    

            else:
                st.warning("Please upload your resume and provide a job description to calculate the ATS score.")
