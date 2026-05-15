"""
Pakistan Cyber Laws Database
Complete laws from Prevention of Electronic Crimes Act (PECA) 2016
with descriptions, punishments, and offense details.
"""

CYBER_LAWS = [
    {
        "section": "13",
        "title": "Unauthorized access to information system",
        "category": "Unauthorized Access",
        "description": "Whoever intentionally accesses or causes to be accessed any information system without lawful authority, or exceeding lawful authority, shall be guilty of an offense.",
        "details": "This includes hacking into systems, bypassing security measures, accessing restricted databases without permission, or using someone else's credentials.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 5 million or both",
        "applicable_to": ["Hacking", "Unauthorized Access"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 13"
    },
    {
        "section": "14",
        "title": "Unauthorized modification of information",
        "category": "Data Damage",
        "description": "Whoever intentionally alters, destroys, or causes loss to any information within an information system shall be guilty of an offense.",
        "details": "This covers changing data, deleting files, corrupting databases, modifying medical records, or tampering with official documents in electronic form.",
        "punishment": "Imprisonment up to 5 years or fine up to Rs. 10 million or both",
        "applicable_to": ["Data Tampering", "Data Damage", "System Sabotage"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 14"
    },
    {
        "section": "15",
        "title": "Introduction of computer virus or malicious code",
        "category": "Malware",
        "description": "Whoever intentionally introduces or causes to be introduced any computer virus or any other malicious code shall be guilty of an offense.",
        "details": "This includes creating malware, distributing viruses, ransomware attacks, worms, trojans, spyware, or any code designed to harm systems or steal information.",
        "punishment": "Imprisonment up to 10 years or fine up to Rs. 50 million or both",
        "applicable_to": ["Malware Distribution", "Ransomware", "Virus Attacks"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 15"
    },
    {
        "section": "16",
        "title": "Charge of offence of hacking with intent to cause damage",
        "category": "Hacking",
        "description": "Whoever commits an offence under section 13, 14 or 15 with intent to cause damage to any person shall be guilty of a more serious offence.",
        "details": "Intentional hacking to harm individuals, businesses, or government systems. This is an aggravated form of unauthorized access with malicious intent.",
        "punishment": "Imprisonment up to 14 years or fine up to Rs. 100 million or both",
        "applicable_to": ["Targeted Hacking", "Malicious Hacking", "System Sabotage"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 16"
    },
    {
        "section": "20",
        "title": "Cyberstalking",
        "category": "Cyberstalking",
        "description": "Whoever by means of electronic device or information system harasses, threatens or intimidates another person, knowing that such conduct is likely to cause emotional distress, fear or alarm to that person, shall be guilty of an offense.",
        "details": "Repeated unwanted contact online, tracking someone's location, surveillance through cameras/GPS, threatening messages, repeated calls/texts, creating fake profiles to harass, etc.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both",
        "applicable_to": ["Cyberstalking", "Online Harassment", "Surveillance"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 20"
    },
    {
        "section": "21",
        "title": "Fraudulent use of information system",
        "category": "Phishing",
        "description": "Whoever uses an information system or computer network service with intent to defraud or knowing that such person uses it to defraud any other person shall be guilty of an offense.",
        "details": "Phishing attacks, fake websites, false representations online, forged emails claiming to be from banks or institutions, social engineering to trick people into revealing information.",
        "punishment": "Imprisonment up to 5 years or fine up to Rs. 10 million or both",
        "applicable_to": ["Phishing", "Online Fraud", "Identity Theft"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 21"
    },
    {
        "section": "24",
        "title": "Offence relating to electronic records",
        "category": "Privacy Violation",
        "description": "Whoever without lawful authority gains access to, intercepts, uses or discloses any electronic record or personal data shall be guilty of an offense.",
        "details": "Accessing someone's private emails, messages, photos, health records, financial information without permission. Intercepting communications or selling personal data.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both",
        "applicable_to": ["Privacy Violation", "Data Breach", "Unauthorized Access"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 24"
    },
    {
        "section": "25",
        "title": "Child sexual abuse material",
        "category": "Child Exploitation",
        "description": "Whoever collects, produces, distributes, imports, exports or possesses any material in any form depicting a child engaged in sexually explicit conduct or simulated sexual conduct, shall be guilty of an offense.",
        "details": "Child pornography, exploitative images or videos of minors, grooming, child trafficking online, distributing CSAM material, possessing or sharing child sexual abuse material.",
        "punishment": "Imprisonment up to 10 years and fine up to Rs. 10 million. For subsequent offenses: imprisonment up to 14 years and fine up to Rs. 20 million",
        "applicable_to": ["Child Exploitation", "Child Pornography", "Online Grooming"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 25"
    },
    {
        "section": "26",
        "title": "Prevention of electronic transmission of obscene material",
        "category": "Obscene Material",
        "description": "Whoever electronically transmits, stores, or distributes any obscene material or content knowing that it is obscene shall be guilty of an offense.",
        "details": "Sharing pornographic content, uploading adult material to shared platforms, sending explicit images without consent, distributing objectionable content.",
        "punishment": "Imprisonment up to 5 years or fine up to Rs. 5 million or both",
        "applicable_to": ["Obscene Material", "Cybercrime"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 26"
    },
    {
        "section": "18",
        "title": "Identity theft",
        "category": "Identity Theft",
        "description": "Whoever fraudulently or dishonestly makes use of the electronic signature, password or any other unique identifier of any other person shall be guilty of an offense.",
        "details": "Using someone's identity online, creating fake accounts in someone's name, using stolen credentials, cloning someone's digital identity, unauthorized use of someone's information.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both",
        "applicable_to": ["Identity Theft", "Impersonation", "Unauthorized Access"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 18"
    },
    {
        "section": "19",
        "title": "Offences relating to digital signatures",
        "category": "Digital Signature Fraud",
        "description": "Whoever without lawful authority forges a digital signature shall be guilty of an offense.",
        "details": "Creating fake digital signatures, forging electronic signatures on documents, tampering with digital signature certificates, unauthorized use of someone's digital signature.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both",
        "applicable_to": ["Digital Signature Fraud", "Document Forgery"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 19"
    },
    {
        "section": "22",
        "title": "Online betting, gaming and gambling",
        "category": "Online Gambling",
        "description": "Whoever creates, operates, facilitates or promotes gambling or betting through an information system shall be guilty of an offense.",
        "details": "Running illegal online casinos, sports betting platforms, poker sites, or other gambling operations without license. Operating illegal gaming websites.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 5 million or both",
        "applicable_to": ["Online Gambling", "Illegal Betting"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 22"
    },
    {
        "section": "23",
        "title": "Offence relating to caller ID spoofing",
        "category": "Caller ID Spoofing",
        "description": "Whoever transmits messages with the intent to cause annoyance, inconvenience, danger, obstruction or insult with disguised electronic address or telephone number shall be guilty of an offense.",
        "details": "Spoofing caller ID to show fake numbers, sending messages with hidden identity, masking phone numbers to impersonate others, caller ID manipulation for fraud.",
        "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both",
        "applicable_to": ["Caller ID Spoofing", "Impersonation"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 23"
    },
    {
        "section": "27",
        "title": "Spamming",
        "category": "Spamming",
        "description": "Whoever transmits an unsolicited message through an information system knowing that such transmission is likely to cause inconvenience or annoyance shall be guilty of an offense.",
        "details": "Sending bulk unsolicited emails, SMS spam, push notifications spam, unwanted marketing messages, sending messages after being asked not to.",
        "punishment": "Imprisonment up to 1 year or fine up to Rs. 500,000 or both",
        "applicable_to": ["Spamming", "Harassment"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 27"
    },
    {
        "section": "28",
        "title": "Financial fraud",
        "category": "Financial Fraud",
        "description": "Whoever commits fraud using any information system or electronic means shall be guilty of an offense.",
        "details": "Online banking fraud, credit card fraud, online payment scams, fake investment schemes, advance-fee fraud, financial transaction manipulation.",
        "punishment": "Imprisonment up to 5 years or fine up to Rs. 10 million or both",
        "applicable_to": ["Financial Fraud", "Cybercrime", "Online Scams"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 28"
    },
    {
        "section": "29",
        "title": "Stealing trade secrets",
        "category": "Trade Secret Theft",
        "description": "Whoever without authority and with intent to cause loss to any person obtains or retains access to any trade secret shall be guilty of an offense.",
        "details": "Industrial espionage, stealing business secrets, unauthorized access to proprietary information, selling company secrets, corporate data theft.",
        "punishment": "Imprisonment up to 10 years or fine up to Rs. 50 million or both",
        "applicable_to": ["Trade Secret Theft", "Corporate Espionage"],
        "peca_reference": "Prevention of Electronic Crimes Act (PECA), 2016 - Section 29"
    }
]

def get_all_laws():
    """Get all cyber laws."""
    return CYBER_LAWS

def get_law_by_section(section):
    """Get a specific law by section number."""
    for law in CYBER_LAWS:
        if law["section"] == str(section):
            return law
    return None

def get_laws_by_category(category):
    """Get all laws in a specific category."""
    return [law for law in CYBER_LAWS if law["category"].lower() == category.lower()]

def get_laws_by_complaint_type(complaint_type):
    """Get applicable laws for a complaint type."""
    applicable_laws = []
    for law in CYBER_LAWS:
        if complaint_type in law["applicable_to"]:
            applicable_laws.append(law)
    return applicable_laws

def search_laws(query):
    """Search laws by title, description, or details."""
    query_lower = query.lower()
    results = []
    for law in CYBER_LAWS:
        if (query_lower in law["title"].lower() or
            query_lower in law["description"].lower() or
            query_lower in law["details"].lower()):
            results.append(law)
    return results

def get_categories():
    """Get all unique law categories."""
    categories = set()
    for law in CYBER_LAWS:
        categories.add(law["category"])
    return sorted(list(categories))
