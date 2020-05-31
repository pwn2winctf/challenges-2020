# Lost qKeys

## quantum/crypto

**TL;DR:** the algorithm is not really an implementation of the quantum one-time pad and
the reply leaks information about the plaintext. You can extract the message by querying
the server multiple times with the same password.


A description of what is happening:
  - Each bit we want to send is transfered to a quantum register;
  - The quantum register is expanded 9-fold implementing a Shor's error-correcting code;
  - The message passes through a noisy channel (not implemented);
  - On the receiver end, the message is recovered correcting any transmission errors (again, no real noise was added);
  - The recovered message is used as a decryption key for the flag, that was encrypted with a truly random key;
  - We receive the result of a measurement after the decryption attempt.

The messages are encoded/decoded to/from strings, numbers, hexadecimal, and to their
binary representations, but are not changed at any point. Also, Shor's code
is applied to a noiseless message, so we don't have to worry about it.

The most important thing to notice is how the quantum encryption key is generated
and used to encrypt the flag on the server.

```python
...
    self.key = self.decode(self.encode(bytes_to_long(os.urandom(self.nbytes)))) # Key generation
...

def encrypt_flag(self, circ):
    self.qbuffer = qiskit.QuantumRegister(self.nbits)
    circ.add_register(self.qbuffer)

    for i, c in enumerate(self.encoded_flag):
        if c=='1':
            circ.x(self.qbuffer[i])

    for i in range(len(self.key)):
        if self.key[i]=='1':
            circ.h(self.qbuffer[i]) # Encryption happens here
    return circ
```

The key is truly random, so not our point of attack, but there is a big issue: it has the same length
as the plaintext. This is ok for a classical one time pad, but to implement the quantum version
of the one time pad we must have a key twice as long as the message.
So that's not really a quantum OTP, which would be unbreakable in this context.

Note that the bits are encrypted using the Hadamard operator *only if* the corresponding
key bit is one. This means that if we use an all-zeros key, we would recover the flag bits
where the corresponding key bit is zero, but would get a random bit where the corresponding key
bit is one.

Finally, we are encrypting the same message multiple times with different keys.
As the keys are randomly generated, each bit has a 50% chance of yielding the
true flag bit as a result, and a 50% chance of generating a random bit, which itself
will be right 50% of the time. Overall, this means that each received bit will be the true flag
bit 75% of the time!
So, collecting ~20 responses from the server we can simply use the most frequent state of each
bit. One final thing to notice is the bits will be reversed in the response
because the highest bit of the flag gets mapped to the lowest qbit in the register.

