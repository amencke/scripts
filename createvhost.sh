#!/bin/bash

if [ $# -ne 3 ]; then
        echo "Usage: $0 <servername> <serveralias> [ssl | nossl]"
        exit 1
fi

SERVERNAME=$1
SERVERALIAS=$2

case $3 in 
        ssl)
                echo "***************************************************"
                echo "SSL specified - please run: genkey $SERVERNAME"
                echo "***************************************************"
                SSL=1
                ;;
        nossl)
                SSL=0
                ;;
        *)
                echo "You need to specify if you want SSL or not"
                exit 1
                ;;
esac

if [ -f /etc/httpd/conf.d/$SERVERNAME.conf ]; then
        echo "Configuration for $SERVERNAME already exists - exiting"
        exit 1
elif [ -d /web/$SERVERNAME ]; then
        echo "DocumentRoot for $SERVERNAME already exists, exiting"
        exit 1 
else
        cat <<EOF > /etc/httpd/conf.d/$SERVERNAME.conf
<Directory /web/$SERVERNAME>
        Require all granted
        AllowOverride none
</Directory>
EOF
        mkdir -p /web/$SERVERNAME
        echo "Welcome to the homepage of $SERVERNAME located at /web/$SERVERNAME" > /web/$SERVERNAME/index.html
fi

if [ $SSL -eq 0 ]; then
        echo "**********"
        echo "SSL -> off"
        echo "**********"
        cat <<EOF >> /etc/httpd/conf.d/$SERVERNAME.conf
<VirtualHost *:80>
        ServerName $SERVERNAME
        ServerAlias $SERVERALIAS
        DocumentRoot /web/$SERVERNAME
        ErrorLog logs/${SERVERNAME}_error_log
        CustomLog logs/${SERVERNAME}_access_log combined
</VirtualHost>
EOF
else
        echo "*********"
        echo "SSL -> on"
        echo "*********"
        cat <<EOF >> /etc/httpd/conf.d/$SERVERNAME.conf
<VirtualHost *:80>
        ServerName $SERVERNAME
        ServerAlias $SERVERALIAS
        RewriteEngine on
        RewriteRule ^(/.*)$ https://%{HTTP_HOST}$1 [redirect=301]
</VirtualHost>

<VirtualHost *:443>
        ServerName $SERVERNAME
        ServerAlias $SERVERALIAS
        DocumentRoot /web/$SERVERNAME
        ErrorLog logs/${SERVERNAME}_ssl_error_log
        CustomLog logs/${SERVERNAME}_ssl_access_log combined
        SSLEngine on
        SSLCipherSuite HIGH:MEDIUM:!aNull:!MD5
        SSLHonorCipherOrder on
        SSLCertificateFile /etc/pki/tls/certs/$SERVERNAME.crt
        SSLCertificateKeyFile /etc/pki/tls/private/$SERVERNAME.key
</VirtualHost>
EOF
fi

echo "Updating hosts file...."

grep $SERVERNAME /etc/hosts
if [ $? -ne 0 ]; then
        echo "192.168.122.210 $SERVERNAME $SERVERALIAS" >> /etc/hosts
        if [ $? -eq 0 ]; then
                echo "...done"
        else 
                echo "Failed to update the hosts file - investigate"
        fi
fi

echo "Updating permissions for apache"
chgrp -R apache /web
chmod -R 2775 /web; chmod -R 775 /web
echo "...done"


echo "Updating SELinux contexts"
semanage fcontext -a -t httpd_sys_content_t "/web/${SERVERNAME}(/.*)?"
restorecon -vvFR /web/$SERVERNAME
echo "...done"

echo "Setting up Apache web server..."
systemctl restart httpd; systemctl enable httpd
if [ $? -ne 0 ]; then
        echo "There was a problem restart Apache."
        echo "If this is an SSL server - its probably because the key/cert doesn't exist"
else:
        echo "done..."
fi


echo "Ready to go - Have a good day!"
