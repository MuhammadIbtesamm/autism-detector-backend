import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")


def send_verification_email(to_email: str, code: str):
    if not resend.api_key:
        raise ValueError("RESEND_API_KEY is not set in environment variables.")

    try:
        response = resend.Emails.send({
            "from": "AutiSpectra <onboarding@resend.dev>",
            "to": [to_email],
            "subject": "Your AutiSpectra Password Reset Code",

            "text": f"Your password reset code is: {code}. It will expire soon. "
                    "If you didn’t request this, you can ignore this email.",

            "html": f"""
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Password Reset Request</h2>
                    <p>Your verification code is:</p>
                    <h1 style="color: #2563EB; letter-spacing: 2px;">{code}</h1>
                    <p>This code will expire soon.</p>
                    <p>If you did not request this, you can safely ignore this email.</p>
                </div>
            """
        })

        print(f"✅ Reset email successfully sent to {to_email}")
        return response

    except Exception as e:
        print(f"❌ Failed to send reset email to {to_email}: {str(e)}")
        raise
