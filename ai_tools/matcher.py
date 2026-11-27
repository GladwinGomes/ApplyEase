"""
AI Resume-to-Job Matcher Service (implemented in Weeks 7-8).

Will compute TF-IDF / cosine similarity and skill overlap between a user's
parsed resume text and a target job description, returning a 0-100 score
along with missing keywords.
"""


def calculate_match_score(resume, job):
    """
    Calculate the match score and missing keywords between a Resume and a Job.

    Returns:
        dict: {'score': float, 'missing_keywords': list[str]}
    """
    # TODO: Implement TF-IDF + skill matching pipeline
    pass
