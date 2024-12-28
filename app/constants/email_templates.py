# email_templates.py

# Template dictionary for different use cases
EMAIL_TEMPLATES = {
    "complete_profile": {
        "subject": "Complete Your Profile on Project X",
        "body": (
            "Hi {name},\n\n"
            "Welcome to our platform! Please complete your profile by setting your password and selecting your role.\n\n"
            "Click the link below to complete your profile:\n"
            "{link}\n\n"
            "If you did not request this, please ignore this email.\n\n"
            "Best regards,\n"
            "Team Project X"
        ),
    },
}
