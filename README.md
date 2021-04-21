# RexEncryptor

To generate an PEM use

openssl genrsa -out private.pem 512
openssl rsa -in private.pem -pubout -out public.pem

Send the public.pm to your Friends and install the public.pem from your Friend!