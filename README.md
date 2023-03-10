# using ssl client authentication 

## Create CA-key
```
openssl genrsa 2048 > ca-key.pem
```

## Create CA-cert
```
openssl req -new -x509 -nodes -days 365000 \
   -key ca-key.pem \
   -out ca-cert.pem \
   -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=example.com"
```
## Create server key & cert signing request
```
openssl req -newkey rsa:2048 -nodes -days 365000 \
   -keyout server-key.pem \
   -out server-req.pem \
   -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"  
```

## Generate Server certificate
```
openssl x509 -req -days 365000 -set_serial 01 \
   -in server-req.pem \
   -out server-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem
```
## Create client key & cert signing request
```
openssl req -newkey rsa:2048 -nodes -days 365000 \
   -keyout client-key.pem \
   -out client-req.pem \
   -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=client.example.com" 
```
## Generate Client certificate
```
openssl x509 -req -days 365000 -set_serial 01 \
   -in client-req.pem \
   -out client-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem
```
## verify
```
openssl verify -CAfile ca-cert.pem \
   ca-cert.pem \
   server-cert.pem

openssl verify -CAfile ca-cert.pem \
   ca-cert.pem \
   client-cert.pem
```
# curl test 
```
curl --request GET \
     --url     https://localhost:8080/ \
     --cert    client-cert.pem \
     --key     client-key.pem \
     --cacert  ca-cert.pem 
```