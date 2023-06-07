# How to Generate a SSH key

In order to access the VM it is necessary to create Secure Shell Protocol (SSH) keys more specifically a public key (shareable part) and a private key (kept safe locally).

## On Windows & Linux Systems

To generate your public key, find and open terminal and type: 



```R
# For linux only
sudo apt install openssh-client


# For both Windows & Linux
ssh-keygen

# Output: 
Generating public/private rsa key pair.
Enter file in which to save the key (C:\Users\user/.ssh/id_rsa): # press enter
Enter passphrase (empty for no passphrase):                         # press enter
Enter same passphrase again:                                        # press enter
Your identification has been saved in C:\Users\user/.ssh/id_rsa.
Your public key has been saved in C:\Users\user/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:V4jnGjEIpUYU4tghvdfdkJj+hnd8t/E70SNGdsdepmX7E ggs\use@CBSxxxx
The key's randomart image is:
+---[RSA 3072]----+
|o o.=o....       |
|+O++.o . .. .    |
|=+=*o .. + o .   |
|..oo.    = + .   |
| ..o . .S = o o  |
|  o . o .O o E   |
|       o= . + .  |
|   ..   .  = .   |
|         .. o    |
+----[SHA256]-----+

```


## Manually locate, open and copy our public key from id_rsa.pub file. 

### On Windows

the file might be here: "C:\Users\write_your_user_name\.ssh"

### On Linux

The generated SSH key will be by stored under ~/.ssh/id_rsa.pub by default.

More information can be found at https://genome.au.dk/docs/getting-started/#public-key-authentication 

