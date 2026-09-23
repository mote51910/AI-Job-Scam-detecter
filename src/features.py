import re

RED_FLAG_PATTERNS = {
    "asks_for_money": r"(registration fee|processing fee|deposit|pay.{0,15}(training|kit|uniform))",
    "too_good_salary": r"(\$\s?\d{4,}\s?/?\s?(week|day)|earn.{0,10}\d{3,}.{0,10}(day|week))",
    "urgent_hiring": r"(urgent(ly)? hiring|immediate joining|apply within \d+ hours|limited seats)",
    "vague_company": r"(confidential company|leading company|no experience.{0,10}high pay)",
    "personal_info_request": r"(bank account|aadhar|social security|passport number|credit card)",
    "generic_email_domain": r"@(gmail|yahoo|hotmail|outlook)\.com",
    "no_interview": r"(no interview required|instant hiring|hired without interview)",
}


def extract_red_flags(raw_text: str) -> dict:
    text = raw_text.lower()
    flags = {}
    for flag_name, pattern in RED_FLAG_PATTERNS.items():
        flags[flag_name] = bool(re.search(pattern, text))
    flags['red_flag_count'] = sum(flags.values())
    return flags


def get_triggered_reasons(raw_text: str) -> list:
    flags = extract_red_flags(raw_text)
    readable = {
        "asks_for_money": "Asks for upfront payment/fees",
        "too_good_salary": "Unrealistically high salary claim",
        "urgent_hiring": "Suspiciously urgent hiring language",
        "vague_company": "Vague or unnamed company details",
        "personal_info_request": "Requests sensitive personal/financial info",
        "generic_email_domain": "Uses generic free email domain instead of company domain",
        "no_interview": "Claims hiring without any interview",
    }
    return [readable[k] for k, v in flags.items() if v is True]
