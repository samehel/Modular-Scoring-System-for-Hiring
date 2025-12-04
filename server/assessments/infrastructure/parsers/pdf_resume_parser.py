
import io
import pdfplumber

from assessments.domain.interfaces.resume_parser import ResumeParser

class PDFResumeParser(ResumeParser):
    
    def parse(self, file: bytes) -> dict:
        
        # Our common headers we find in resumes
        SECTION_HEADERS = {
            "education": ["education", "educational background", "academics"],
            "experience": ["experience", "work experience", "professional experience"],
            "skills": ["skills", "technical skills", "skillset"],
            "projects": ["projects", "personal projects"],
            "certifications": ["certifications", "certificates"],
            "summary": ["summary", "profile", "about me"],
        }

        # Extract the lines from our file
        lines = []
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    for line in text.splitlines():
                        line = line.strip()
                        if line:
                            lines.append(line)

        ''' 
        Now we actually parse the sections and return a dict of the section header
        as our key, and the content under that header as our value

        OUTPUT EXAMPLE:
        {
            "education": "Harvard University\nBSc Computer Science, 2018–2022\n",
            "experience": "Software Engineer at X Corp, 2022–Present\n...",
            "skills": "Python, Django, React, AWS\n",
            "projects": "",
            "certifications": "",
            "summary": ""
        }
        '''
        parsed_resume = { key: "" for key in SECTION_HEADERS.keys() }
        current_section = None

        for line in lines:
            lower = line.lower()

            for section_key, header_variants in SECTION_HEADERS.items():
                if any(lower.startswith(h) for h in header_variants):
                    current_section = section_key
                    break
            else:
                if current_section:
                    parsed_resume[current_section] += line + "\n"
        
        return parsed_resume

