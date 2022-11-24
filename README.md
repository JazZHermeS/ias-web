# ias-web
(I)AS web project

## Installation

### Requirements
```
pip install django-crispy-forms
pip install django-sslserver
pip install django-qr-code
pip install pyotp
pip install django-cryptography
python -m pip install Pillow
pip install django-axes
```

### HTTPS setup
Install [mkcert](https://github.com/FiloSottile/mkcert) for a zero-config HTTPS setup.

Install a local certificate authority with:
```
mkcert -install
```

Generate a certificate and key for the website:
```
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```

### django-cryptography setup
Replace the value of the `SECRET_KEY` setting inside `settings.py` with the appropriate key.

## Run
```
python manage.py runsslserver --certificate cert.pem --key key.pem
```

## Login attempts
```
python manage.py axes_list_attempts
python manage.py axes_reset
python manage.py axes_reset_username [username ...]
```
