const FIELD_MAP = {
  first_name: [
    "first_name",
    "firstname",
    "fname",
    "given_name",
    "givenname",
    "first name",
  ],
  last_name: [
    "last_name",
    "lastname",
    "lname",
    "family_name",
    "familyname",
    "surname",
    "last name",
  ],
  full_name: [
    "full_name",
    "fullname",
    "name",
    "candidate_name",
    "applicant_name",
    "full name",
  ],
  email: [
    "email",
    "e-mail",
    "mail",
    "candidate_email",
    "contact_email",
    "email_address",
  ],
  phone: [
    "phone",
    "tel",
    "telephone",
    "mobile",
    "phone_number",
    "contact_phone",
    "cell",
  ],
  location: [
    "location",
    "city",
    "city_location",
    "current_location",
    "address",
  ],
  linkedin_url: [
    "linkedin",
    "linkedin_url",
    "li_profile",
    "linkedin profile",
  ],
  github_url: [
    "github",
    "github_url",
    "gh_profile",
    "github profile",
  ],
  portfolio_url: [
    "portfolio",
    "portfolio_url",
    "portfolio_website",
    "website",
    "personal_website",
  ],
  university: [
    "university",
    "school",
    "school_name",
    "college",
    "institution",
    "alma_mater",
  ],
  degree: [
    "degree",
    "qualification",
    "education_level",
  ],
  field_of_study: [
    "field_of_study",
    "major",
    "major_field",
    "discipline",
  ],
  skills: [
    "skills",
    "tech_skills",
    "tech_stack",
    "technical_skills",
  ],
  summary: [
    "summary",
    "summary_bio",
    "bio",
    "about",
    "professional_summary",
  ],
  cover_letter: [
    "cover_letter",
    "coverletter",
    "motivation",
    "cover letter",
  ],
};

function getElementLabelText(el) {
  if (el.id) {
    const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
    if (label) {
      return label.textContent.trim();
    }
  }
  const parentLabel = el.closest("label");
  if (parentLabel) {
    return parentLabel.textContent.trim();
  }
  return el.getAttribute("aria-label") || "";
}

function normalizeText(value) {
  return (value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function matchFieldKey(el) {
  const candidates = [
    el.name,
    el.id,
    el.placeholder,
    getElementLabelText(el),
  ]
    .map(normalizeText)
    .filter(Boolean);

  for (const [profileKey, aliases] of Object.entries(FIELD_MAP)) {
    for (const candidate of candidates) {
      for (const alias of aliases) {
        const normalizedAlias = normalizeText(alias);
        if (candidate === normalizedAlias || candidate.includes(normalizedAlias)) {
          return profileKey;
        }
      }
    }
  }
  return null;
}

function flattenProfileData(profile) {
  const user = profile.user || {};
  const firstName = profile.first_name || user.first_name || "";
  const lastName = profile.last_name || user.last_name || "";
  const fullName = profile.full_name || `${firstName} ${lastName}`.trim();

  const educationList = Array.isArray(profile.educations) ? profile.educations : [];
  const primaryEdu = educationList[0] || {};

  const skillsList = Array.isArray(profile.skills) ? profile.skills : [];
  const skillsText = skillsList
    .map((s) => (typeof s === "string" ? s : s.skill_name || s.name || ""))
    .filter(Boolean)
    .join(", ");

  return {
    first_name: firstName,
    last_name: lastName,
    full_name: fullName,
    email: profile.email || user.email || "",
    phone: profile.phone || "",
    location: profile.location || "",
    linkedin_url: profile.linkedin_url || "",
    github_url: profile.github_url || "",
    portfolio_url: profile.portfolio_url || "",
    university: primaryEdu.institution || "",
    degree: primaryEdu.degree || "",
    field_of_study: primaryEdu.field_of_study || "",
    skills: skillsText,
    summary: profile.summary || "",
    cover_letter: profile.cover_letter || profile.summary || "",
  };
}
