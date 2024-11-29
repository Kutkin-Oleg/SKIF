from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
import qiskit_aer as Aer

qc = QuantumCircuit(2)

# готовим состояние beta_{00} из стартового состояния |00>:
qc.h(0)
qc.cx(0, 1)

# визуальный разделитель при отрисовке схемы:
qc.barrier()

# выбираем какое-либо сообщение из набора в assert-выражении ниже:
message = '11'

assert message in ('00', '01', '10', '11')


# Алиса выполняет кодирование сообщения:
if message[1] == "1":
    qc.x(0)
if message[0] == "1":
    qc.z(0)

qc.barrier()

# Боб декодирует сообщение:
qc.cx(0, 1)
qc.h(0)

# Боб измеряет двухкубитную систему целиком (в вычислительном базисе):
qc.measure_all()

qc.draw('mpl')
plt.show()



aer_sim = Aer.AerSimulator()
result = aer_sim.run(qc).result()
counts = result.get_counts(qc)

print(
    f"message was '{message}' -> the measurement result is {counts}"
    " (<- NOTE: the keys are little-endian!)"
)