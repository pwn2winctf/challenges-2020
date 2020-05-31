import qiskit
import os
from Crypto.Util.number import bytes_to_long
from secrets import flag

class IQuantumComputer:
    def __init__(self, nbits):
        self.nbits = nbits
        self.nbytes = (self.nbits - 1)//8 + 1

    def string_to_bits(self, m):
        if isinstance(m, str):
            m = m.encode()
        return self.decode(self.encode(bytes_to_long(m)))

    def encode(self, m):
        return '{:0{}x}'.format(m, self.nbytes)

    def decode(self, m):
        return '{:0{}b}'.format(int(m, 16), self.nbits)[-self.nbits:]

    def send_qubits(self, msg, dest):
        qbit_config = self.decode(msg)
        q = qiskit.QuantumRegister(9*len(qbit_config))
        circ = qiskit.QuantumCircuit(q)
        for j, c in enumerate(qbit_config):
            if c=='1':
                circ.x(q[9*j])
            circ.cx(q[9*j],q[9*j+3])
            circ.cx(q[9*j],q[9*j+6])
            circ.h(q[9*j])
            circ.h(q[9*j+3])
            circ.h(q[9*j+6])
            circ.cx(q[9*j],q[9*j+1])
            circ.cx(q[9*j],q[9*j+2])
            circ.cx(q[9*j+3],q[9*j+4])
            circ.cx(q[9*j+3],q[9*j+5])
            circ.cx(q[9*j+6],q[9*j+7])
            circ.cx(q[9*j+6],q[9*j+8])

        return quantum_channel(circ, dest)

    def read_qubits(self, circ):
        raise NotImplemented('read_qubits')

    @staticmethod
    def send_message(message, dest):
        classical_channel(message, dest)

    @staticmethod
    def read_message(message):
        raise NotImplemented('read_message')


class LocalQuantumComputer(IQuantumComputer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def read_message(message):
        print(message)


class RemoteQuantumComputer(IQuantumComputer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = self.decode(self.encode(bytes_to_long(os.urandom(self.nbytes))))
        self.encoded_flag = self.string_to_bits(flag)

    def encrypt_flag(self, circ):
        self.qbuffer = qiskit.QuantumRegister(self.nbits)
        circ.add_register(self.qbuffer)

        for i, c in enumerate(self.encoded_flag):
            if c=='1':
                circ.x(self.qbuffer[i])

        for i in range(len(self.key)):
            if self.key[i]=='1':
                circ.h(self.qbuffer[i])
        return circ

    def decrypt_flag(self, circ):
        for i in range(self.nbits):
            circ.ch(self.received_qubits[9*i], self.qbuffer[i])

        output = qiskit.ClassicalRegister(self.nbits)
        circ.add_register(output)
        circ.measure(self.qbuffer, output)

        bk = qiskit.Aer.get_backend('qasm_simulator')
        job = qiskit.execute(circ, bk, shots=1)
        res = job.result()
        if not res.success:
            raise MemoryError('You should use a real quantum computer...')
        res = res.get_counts(circ)
        self.res = [self.encode(int(k,2)) for k in res.keys()]

    def read_qubits(self, circ):
        self.received_qubits = circ.qubits
        for i in range(0, len(self.received_qubits), 9):
            circ.cx(self.received_qubits[i], self.received_qubits[i+1])
            circ.cx(self.received_qubits[i], self.received_qubits[i+2])
            circ.ccx(self.received_qubits[i+1], self.received_qubits[i+2], self.received_qubits[i])
            circ.h(self.received_qubits[i])
            circ.cx(self.received_qubits[i+3], self.received_qubits[i+4])
            circ.cx(self.received_qubits[i+3], self.received_qubits[i+5])
            circ.ccx(self.received_qubits[i+4], self.received_qubits[i+5], self.received_qubits[i+3])
            circ.h(self.received_qubits[i+3])
            circ.cx(self.received_qubits[i+6], self.received_qubits[i+7])
            circ.cx(self.received_qubits[i+6], self.received_qubits[i+8])
            circ.ccx(self.received_qubits[i+7], self.received_qubits[i+8], self.received_qubits[i+6])
            circ.h(self.received_qubits[i+6])
            circ.cx(self.received_qubits[i], self.received_qubits[i+3])
            circ.cx(self.received_qubits[i], self.received_qubits[i+6])
            circ.ccx(self.received_qubits[i+3], self.received_qubits[i+6], self.received_qubits[i])

        circ = self.encrypt_flag(circ)
        self.decrypt_flag(circ)


def classical_channel(message, dest):
    dest.read_message(message)


def quantum_channel(qcirc, dest):
    # noise
    dest.read_qubits(qcirc)


def connect(local, remote):
    remote.send_message('passwd:', local)
    pwd = input()
    local.send_qubits(pwd, remote)
    remote.send_message(', '.join(remote.res), local)


def main(nbits):
    local = LocalQuantumComputer(nbits)
    remote = RemoteQuantumComputer(nbits)
    connect(local, remote)


if __name__=='__main__':
    nbits = 8*len(flag)
    main(nbits=nbits)

