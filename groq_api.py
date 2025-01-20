from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv("api.env")
API_KEY = os.getenv("API_KEY_GROQ")

MODEL = "llama-3.3-70b-versatile"

class GroqClient:
    def __init__(self, api_key=API_KEY, model=MODEL):
        self.api_key = api_key
        self.MODEL = model
        self.client = Groq(api_key=self.api_key)
    
    def get_password_strength(self, password):
        message = f"Giving only a whole number, how would you rate the strength of the password '{password}' on a scale of 0 - 10."
        messages = [{"role": "system", "content": "you are a cybersecurity specialist"}, {"role": "user", "content": message}]

        groq_response = self.client.chat.completions.create(messages=messages, model=self.MODEL, temperature=0.1, stop=".")
        strength = float(groq_response.choices[0].message.content[-2::])
        return strength



    def create_new_password(self, password, iterations=1):
        message = f"Giving only the new passwords, generate {str(iterations)} that are similar but stronger than {password}, seperated by a commma and a space"
        messages = [{"role": "system", "content": "you are a cybersecurity specialist"}, {"role": "user", "content": message}]
        new_passwords = self.client.chat.completions.create(messages=messages, model=self.MODEL, temperature=0.3)
        new_passwords = new_passwords.choices[0].message.content.split(", ")

        return new_passwords
    
    def critique_password(self, password):
        message = f"In 15-20 words, why might the password '{password}' be insecure ?"
        messages = [{"role": "system", "content": "you are a cybersecurity specalist"}, {"role": "user", "content": message}]
        critique = self.client.chat.completions.create(messages=messages, model=self.MODEL, temperature=1.3)
        return critique.choices[0].message.content


if __name__ == "__main__":
    from password_strength_detector import get_password_strength
    client = GroqClient()

    while True:
        password = input("Enter a password: ")
        password_strength_rfc = get_password_strength(password)
        password_strength_groq = client.get_password_strength(password)
        print(f"Strength rating from 0 - 10 using RandomForestClassifier Machine Learning: {str(password_strength_rfc)}")
        print(f"Strength rating from 0 - 10 using LockSmith AI: {str(password_strength_groq)}")
        print ("\n")
        reason = client.critique_password(password)
        print ("Why this password might be bad: " + reason)
        print("\n")
        print("Three better passwords would be: ")
        new_password = client.create_new_password(password, iterations=3)
        for password in new_password:
            print(password)

        print ("\n") 