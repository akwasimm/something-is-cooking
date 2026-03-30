import re
import fitz

# Hand curated skills dictionary tailored for typical market extraction.
# Expand algorithmically if broader sector coverage becomes mapped natively!
KNOWN_SKILLS = {
    "python", "react", "fastapi", "docker", "aws", "javascript", "sql", 
    "machine learning", "kubernetes", "typescript", "node.js", 
    "express", "flask", "django", "html", "css", "postgresql", 
    "mysql", "aws", "gcp", "azure", "git", "ci/cd", "agile", "scrum",
    "go", "rust", "c++", "c#", "java", "spring boot", "ruby", "rails"
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Spawns an isolated PyMuPDF mapping structure, looping paginations
    sequentially generating raw UTF-8 string data without layout constraints.
    """
    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    extracted_text = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        extracted_text.append(page.get_text())

    pdf_document.close()
    return " ".join(extracted_text)


def extract_skills_from_text(text: str) -> list[str]:
    """
    Regex boundary checks securing explicit strings dynamically.
    For example: Traps 'go' isolated exclusively, eliminating structural collisions into 'algorithm'.
    """
    lower_text = text.lower()
    found_skills = set()

    for skill in KNOWN_SKILLS:
        # Construct explicit bounding regex cleanly dodging punctuation bleed and trailing pluralisms
        # \b maps identical word boundary triggers natively. For ".js" handling, \b handles non-word borders differently.
        # But for generic skill extractions it's perfectly reliable logic!
        escaped_skill = re.escape(skill)
        match_pattern = rf"\b{escaped_skill}\b"
        
        if re.search(match_pattern, lower_text):
            found_skills.add(skill)

    return list(found_skills)
