# Smart ATS Tracker - Gemini Pro

## Overview
Smart ATS Tracker is a cutting-edge web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). Built with advanced AI capabilities, this tool provides detailed insights into resume compatibility with job descriptions and offers actionable suggestions to improve your chances in the competitive job market.

## Features
- **Job Description (JD) Match Analysis**: Calculates the percentage match between your resume and the provided job description.
- **Keyword Suggestions**: Identifies missing keywords and provides recommendations to include them.
- **Resume Improvement Tips**: Offers actionable suggestions to enhance your resume's ATS compatibility.
- **Word Cloud Visualization**: Displays missing keywords in a visually appealing word cloud.
- **ATS Score Analysis**: Generates an overall ATS score with a detailed breakdown and weighted pie chart visualization.
- **PDF Report Generation**: Creates a downloadable PDF report summarizing the analysis.

## Tech Stack
- **Framework**: Streamlit
- **AI Model**: Google Generative AI (Gemini Pro)
- **Libraries**: PyPDF2, WordCloud, Plotly, Scikit-learn, FPDF
- **Styling**: Custom CSS for a professional UI

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-ats-tracker.git
   cd smart-ats-tracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root directory.
   - Add your Google Generative AI API key:
     ```env
     GOOGLE_API_KEY=your_api_key_here
     ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Input Job Description**: Copy and paste the job description into the provided text area.
2. **Upload Resume**: Upload your resume in PDF format.
3. **Analyze**: Click the **Submit** button to receive detailed insights:
   - ATS compatibility score
   - Missing keywords and suggestions
   - Resume improvement tips
   - Word cloud visualization
4. **Download Report**: Optionally, download a comprehensive PDF report summarizing the analysis.

## Screenshots

### Home Page
![Home Page](https://github.com/user-attachments/assets/a1acd3e1-1e3b-4b77-9387-97181d0de650)


### ATS Score Breakdown
![ATS Score](https://github.com/user-attachments/assets/48f86a3a-eb8c-41dd-9d52-95a191c11d8b)


### Word Cloud Visualization
![Word Cloud](https://github.com/user-attachments/assets/4263e8dd-24ec-4b98-b37a-cfad18e7e87c)

### ATS Score Plot
![Plot](https://github.com/user-attachments/assets/07c3c858-ee7e-4c97-a96b-808baa107c22)



## Contributing

We welcome contributions to make this project even better! Feel free to open issues or submit pull requests.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Generative AI (Gemini Pro)** for providing the powerful AI capabilities.
- Open-source contributors and libraries for making this project possible.

## Contact

For feedback or queries, feel free to reach out:
- **Email**: rayrohit685@gmail.com
- **LinkedIn**: [My LinkedIn](https://www.linkedin.com/in/rohit-ray-08634a216/)

---

Star this repo 🌟 if you find it useful and share it with your network!
