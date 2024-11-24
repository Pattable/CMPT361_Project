from Crypto.PublicKey import RSA

# Server Key Generation
# Generate private and public keys
key = RSA.generate(2048)
private_key = key.export_key(format='PEM')
public_key = key.publickey().export_key(format='PEM')

# File extension
private = '_private.pem'
public = '_public.pem'

# Add Keys to server folder
with open('./server/server' + private, 'wb') as f:
	f.write(private_key)

with open('./server/server' + public, 'wb') as f:
	f.write(public_key)

# Add Server Public Key to client folder
with open('./client/server' + public, 'wb') as f:
	f.write(public_key)

# Client Key Generation
for i in range(1, 6):
	
	# Generate private and public keys
	key = RSA.generate(2048)
	private_key = key.export_key(format='PEM')
	public_key = key.publickey().export_key(format='PEM')
	
	# Client path
	client = './client/client' + str(i)
	
	# Server path
	server = './server/client' + str(i)	
	
	# Add Keys to client folder
	with open(client + private, "wb") as f:
		f.write(private_key)
	
	with open(client + public, "wb") as f:
		f.write(public_key)
	
	# Add Client Public Key to server folder
	with open(server + public, "wb") as f:
		f.write(public_key)	