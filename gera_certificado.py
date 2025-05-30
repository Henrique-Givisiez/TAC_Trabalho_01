from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# 1. Gera chave privada RSA
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# 2. Informações do certificado
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Distrito Federal"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Brasília"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MinhaOrganizacao"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

# 3. Cria o certificado
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .sign(key, hashes.SHA256())
)

# 4. Salva a chave privada
with open("chave.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# 5. Salva o certificado
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Arquivos 'cert.pem' e 'chave.pem' gerados com sucesso.")
