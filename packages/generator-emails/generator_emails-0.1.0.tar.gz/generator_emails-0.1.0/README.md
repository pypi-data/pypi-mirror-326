# Generator emails 📧  

A Python module for generating unique email addresses with customizable options. Supports both public and anonymous email domains, keyword-based usernames, and history tracking to avoid duplicates.  

## Installation  
You can install the package via PyPi:  
```bash
pip install generator-emails
```

Or clone the repository:  
```bash
git clone https://github.com/Triram-2/generator-emails.git
cd generator-emails
pip install -r requirements.txt
```

## Usage  
Import the module and create an instance:  
```python
from generator_emails import GeneratorEmails

generator = GeneratorEmails()
email = generator.generate_email()
print(email)  # Example output: johndoe123@gmail.com
```

## Built-in Domain Databases

generator-emails includes two built-in lists of domains:

- **Public domains** – Popular email providers such as Gmail, Yahoo, Outlook, and Yandex.
- **Anonymous domains** – Temporary and privacy-focused email services like Guerrilla Mail, Mailinator, and 10MinuteMail.

These domains are used when selecting `'random'` (for public) or `'anonim'` (for anonymous) as the domain parameter.

## Parameters  

### `GeneratorEmails(save_history=True)`  
- `save_history` *(bool)* – Whether to store generated emails to prevent duplicates.  

### `generate_email(range_len=(10, 18), domain='gmail.com', keywords=None, format='{username}')`  
Generates a unique email address.  

#### **Arguments:**  
- `range_len` *(tuple, optional)* – Min and max length of the username.
- `domain` *(str or list, optional)* – Email domain. Can be a string, list of domains, `'random'` for a random public domain, or `'anonim'` for an anonymous domain.
- `keywords` *(str or list, optional)* – A keyword or list of keywords to include in the username.

#### **Returns:**  
- `str` – A generated unique email address.

## Example Usage
```python
email1 = generator.generate_email()
email2 = generator.generate_email(domain='yahoo.com', keywords='testuser')
email3 = generator.generate_email(range_len=(8, 12), keywords=['test', 'Mirukha'])

print(email1)
print(email2)
print(email3)
```

## License
This project is licensed under the MIT License.

