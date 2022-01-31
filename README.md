# Cardan grille v1.0

Encryption with latin squares and Cardan grille.

## How to use

### Setup

Before use install python 3: https://www.python.org/downloads/
(Check the 'Add Python 3.x to PATH' box)

1. https://rapidapi.com/peterhege/api/laquare/pricing
2. Select a Plan
3. https://rapidapi.com/peterhege/api/laquare/
4. Copy the 'x-rapidapi-key' value
5. Replace [x-rapidapi-key] to 'x-rapidapi-key' value in this command and run:

`py main.py config --key=[x-rapidapi-key]`

### Encrypt

`py main.py encode --input=[file_path] --output=[encrypted_file_path] --progress`

The program will print the key needed to decrypt it 'Key: [decrypt_key]'

### Decrypt

`py main.py decode --input=[encrypted_file_path] --output=[decrypted_file_path] --key=[decrypt_key] --progress`

## Changelog

### 2022.01.31

Release

### 2022.01.05

Use Laquare API

### 2019.11.13

- init

<a href="https://www.paypal.com/donate/?hosted_button_id=DEXRZ9EPTEC68">
  <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" />
</a>
