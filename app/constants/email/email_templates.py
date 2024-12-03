# email_templates.py

# Template dictionary for different use cases
EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to Our Service",
        "body": "Hi {name},\n\nWelcome to our platform. We are excited to have you onboard!\n\nBest regards,\nTeam",
    },
    "password_reset": {
        "subject": "Password Reset Request",
        "body": "Hello {name},\n\nYou requested a password reset. Please use the following link to reset your password: {link}\n\nIf you did not make this request, please ignore this email.\n\nRegards,\nSupport Team",
    },
    "task_notification": {
        "subject": "New Task Assigned",
        "body": "Hi {name},\n\nYou have been assigned a new task: {task_name}. Please check your dashboard for more details.\n\nThanks,\nManagement",
    },
}
