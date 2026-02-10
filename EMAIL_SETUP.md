# Email Configuration Guide

## Setting up Email Functionality

The application now supports user-to-user messaging through email. To enable this functionality, you need to configure the email settings in `app.py`.

## Configuration Options

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to your Google Account settings
   - Navigate to Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

3. **Update `app.py`** with your credentials:
   ```python
   app.config['MAIL_SERVER'] = 'smtp.gmail.com'
   app.config['MAIL_PORT'] = 587
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your Gmail address
   app.config['MAIL_PASSWORD'] = 'your-app-password'     # 16-char app password
   app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
   ```

### Option 2: Other Email Services

#### Outlook/Hotmail
```python
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@outlook.com'
app.config['MAIL_PASSWORD'] = 'your-password'
```

#### Yahoo Mail
```python
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@yahoo.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### Option 3: Development/Testing (No Real Emails)

For testing without sending real emails, you can use a debugging mail server:

```python
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
```

Then run a debug SMTP server in a separate terminal:
```bash
python -m smtpd -n -c DebuggingServer localhost:1025
```

## Installation

Make sure Flask-Mail is installed:
```bash
pip install Flask-Mail
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Features

Once configured, users can:
- View the email address of users who submitted books
- Click on the email to send a direct email via their email client
- Use the "📧 Send Message" button to send a message through the app
- Messages include context about which book the inquiry is about
- Recipients can reply directly to the sender's email

## Security Notes

- Never commit your actual email credentials to version control
- Consider using environment variables for production:
  ```python
  import os
  app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
  app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
  ```
- Use app-specific passwords instead of your main account password
- For production, consider using a dedicated email service like SendGrid, Mailgun, or AWS SES

## Troubleshooting

**"Failed to send message" error:**
- Check your email credentials are correct
- Verify your email provider allows SMTP access
- Check if you need an app-specific password
- Ensure your firewall isn't blocking port 587
- Try enabling "Less secure app access" (Gmail) or app passwords

**Emails going to spam:**
- This is common with personal email accounts
- Recipients should check their spam folder
- For production, use a dedicated email service with proper SPF/DKIM setup
