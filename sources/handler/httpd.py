from pathlib import Path
import os
from datetime import date
import shutil
import subprocess


class HttpdHandler:
    @staticmethod
    def create(argc: int, argv: list) -> int:
        domains = argv[2:]

        primary_domain_parts = domains.pop(0).split('.')

        if len(primary_domain_parts) < 2:
            print('ERROR: invalid primary domain format')
            return 1

        tld = primary_domain_parts.pop()
        domain = primary_domain_parts.pop()
        sub_domain = 'www'
        if len(primary_domain_parts) == 1:
            sub_domain = primary_domain_parts.pop()

        server_name = domain + '.' + tld
        if sub_domain != "www":
            server_name = sub_domain + '.' + server_name
        else:
            domains.insert(0, 'www.' + server_name)

        domains = list(set(domains) - {server_name})
        #  domains = [x for x in domains if x != server_name]

        server_aliases = ''
        if len(domains) > 0:
            server_aliases = 'ServerAlias ' + (' '.join(domains))

        directory = '/var/www/{tld}.{domain}.{sub_domain}'.format(tld=tld, domain=domain, sub_domain=sub_domain)

        # setup web folder
        Path(directory + '/htdocs').mkdir(parents=True, exist_ok=True)
        Path(directory + '/logs').mkdir(parents=True, exist_ok=True)
        Path(directory + '/tls/well-known').mkdir(parents=True, exist_ok=True)

        link = Path(directory + '/htdocs/stage')
        if link.exists():
            link.unlink()
        link.symlink_to('0000-00-00--0', target_is_directory=True)

        link = Path(directory + '/htdocs/live')
        if link.exists():
            link.unlink()
        link.symlink_to('0000-00-00--0', target_is_directory=True)

        Path(directory + '/htdocs/0000-00-00--0/public').mkdir(parents=True, exist_ok=True)
        Path(directory + '/htdocs/0000-00-00--0/public/index.php').write_text('...')
        Path(directory + '/htdocs/0000-00-00--0/public/.htaccess').write_text("""
RewriteEngine On

# Reroute any incoming request that is not an existing file
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ index.php [QSA,L]
""".lstrip())

        Path(directory + '/htdocs/.htaccess').write_text("""
RewriteEngine on

# --- stage begin ---
RewriteCond %{HTTP_COOKIE} stage [NC]
RewriteRule (.*) 0000-00-00--0/public/$1 [L]
# --- stage end ---

# --- live begin ---
RewriteRule (.*) 0000-00-00--0/public/$1 [L]
# --- live end ---
""".lstrip())

        vhost = """
<VirtualHost *:80>
    ServerName {server_name}
    {server_aliases}

    Alias /.well-known/acme-challenge/ /var/www/{tld}.{domain}.{sub}/tls/well-known/
    <Directory /var/www/{tld}.{domain}.{sub}/tls/well-known/>
        AllowOverride None
        Require all granted
        Satisfy Any
    </Directory>

    DocumentRoot /var/www/{tld}.{domain}.{sub}/htdocs/
    <Directory /var/www/{tld}.{domain}.{sub}/htdocs/>
        Options FollowSymLinks
        AllowOverride All
        Order allow,deny
        allow from all
    </Directory>

    LogLevel warn
    ErrorLog /var/www/{tld}.{domain}.{sub}/logs/error.log
    CustomLog /var/www/{tld}.{domain}.{sub}/logs/access.log combined
</VirtualHost>

""".format(server_name=server_name, server_aliases=server_aliases, tld=tld, domain=domain, sub=sub_domain)

        Path('/etc/httpd/conf.d').mkdir(parents=True, exist_ok=True)
        Path('/etc/httpd/conf.d/{tld}.{domain}.{sub}.conf'.format(tld=tld, domain=domain, sub=sub_domain)) \
            .write_text(vhost.lstrip())

        os.popen('service httpd restart').read()

        dns_list = domains
        dns_list.append(domain + '.' + tld)
        dns = ['DNS:' + x for x in dns_list]
        dns = ",".join(dns)

        subprocess.Popen('openssl genrsa 4096 > ' + directory + '/tls/account.key', shell=True, executable='/bin/bash').read()
        os.popen('openssl genrsa 4096 > ' + directory + '/tls/domain.key').read()
        os.popen('openssl req -new -sha256 -key ' + directory + '/tls/domain.key -subj "/" -reqexts SAN -config <(cat /etc/pki/tls/openssl.cnf  <(printf "[SAN]\\nsubjectAltName=' + dns + '")) > ' + directory + '/tls/domain.csr').read()
        os.popen('python3 /root/bin/acme_tiny.py --account-key ' + directory + '/tls/account.key --csr ' + directory + '/tls/domain.csr --acme-dir ' + directory + '/tls/well-known/ > ' + directory + '/tls/signed.crt').read()
        os.popen('wget --quiet -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > ' + directory + '/tls/intermediate.pem').read()
        os.popen('cat ' + directory + '/tls/signed.crt ' + directory + '/tls/intermediate.pem > ' + directory + '/tls/chained.pem')

        vhost = """
<VirtualHost *:443>
    ServerName {server_name}
    {server_aliases}

    # TLS certs
    SSLEngine On
    SSLCertificateFile /var/www/{tld}.{domain}.{sub}/tls/signed.crt
    SSLCertificateKeyFile /var/www/{tld}.{domain}.{sub}/tls/domain.key
    SSLCertificateChainFile /var/www/{tld}.{domain}.{sub}/tls/chained.pem

    DocumentRoot /var/www/{tld}.{domain}.{sub}/htdocs/
    <Directory /var/www/{tld}.{domain}.{sub}/htdocs/>
        Options FollowSymLinks
        AllowOverride All
        Order allow,deny
        allow from all
    </Directory>

    LogLevel warn
    ErrorLog /var/www/{tld}.{domain}.{sub}/logs/error.log
    CustomLog /var/www/{tld}.{domain}.{sub}/logs/access.log combined
</VirtualHost>

""".format(server_name=server_name, server_aliases=server_aliases, tld=tld, domain=domain, sub=sub_domain)
        conf = Path('/etc/httpd/conf.d/{tld}.{domain}.{sub}.conf'.format(tld=tld, domain=domain, sub=sub_domain))
        with conf.open('a') as f:
            f.write(vhost.lstrip())

        os.popen('service httpd reload').read()

        return 0

    @staticmethod
    def refresh_tls(argc: int, argv: list) -> int:
        domains = argv[2:]

        primary_domain_parts = domains.pop(0).split('.')

        if len(primary_domain_parts) < 2:
            print('ERROR: invalid primary domain format')
            return 1

        tld = primary_domain_parts.pop()
        domain = primary_domain_parts.pop()
        sub_domain = 'www'
        if len(primary_domain_parts) == 1:
            sub_domain = primary_domain_parts.pop()

        directory = '/var/www/{tld}.{domain}.{sub_domain}'.format(tld=tld, domain=domain, sub_domain=sub_domain)
        directory_tls = directory + '/tls'
        directory_tls_backup = directory + '/tls/backups/' + date.today().strftime('%Y-%m-%d')

        if not Path(directory).is_dir():
            print('ERROR: Domain not found')
            return 1

        Path(directory_tls_backup + '/').mkdir(parents=True)
        shutil.copy(Path(directory_tls + '/account.key'), Path(directory_tls_backup + '/account.key'))
        shutil.copy(Path(directory_tls + '/chained.pem'), Path(directory_tls_backup + '/chained.pem'))
        shutil.copy(Path(directory_tls + '/domain.csr'), Path(directory_tls_backup + '/domain.csr'))
        shutil.copy(Path(directory_tls + '/domain.key'), Path(directory_tls_backup + '/domain.key'))
        shutil.copy(Path(directory_tls + '/intermediate.pem'), Path(directory_tls_backup + '/intermediate.pem'))
        shutil.copy(Path(directory_tls + '/signed.crt'), Path(directory_tls_backup + '/signed.crt'))

        os.popen('python3 /root/bin/acme_tiny.py --account-key ' + directory + '/tls/account.key --csr ' + directory + '/tls/domain.csr --acme-dir ' + directory + '/tls/well-known/ > ' + directory + '/tls/signed.crt').read()
        os.popen('wget --quiet -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > ' + directory + '/tls/intermediate.pem').read()
        os.popen('cat ' + directory + '/tls/signed.crt ' + directory + '/tls/intermediate.pem > ' + directory + '/tls/chained.pem')

        os.popen('service httpd reload').read()

        return 0
