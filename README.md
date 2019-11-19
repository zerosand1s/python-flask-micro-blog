### Create Virtual Environment 

    python3 -m venv venv

### Use Virtual Environment

- Mac/Linux: `source venv/bin/activate`

- Windows: `venv\Scripts\activate`

### CLI command to extract text into .pot file (I18n, L10n)

     pybabel extract -F babel.cfg -k _l -o messages.pot .
     
### CLI command to generate translations(Spanish) for .pot file (I18n, L10n)

    pybabel init -i messages.pot -d app/translations -l es
    
### Compile translation files (I18n, L10n)

    pybabel compile -d app/translations