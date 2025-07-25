import openai
from config_api import apikey

openai.api_key = apikey


def generate_email(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that writes professional emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256
        )

        # Extract the email text from the response
        email_text = response["choices"][0]["message"]["content"].strip()
        print("Generated Email:\n")
        print(email_text)
        return email_text  # Optionally return the generated email text for further use
    except Exception as e:
        print(f"Error occurred while generating email: {e}")
        return None




