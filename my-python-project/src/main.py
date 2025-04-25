from CPU import CPU

def inicializarCpus(quantidade):
    return [CPU(f"CPU-{i}") for i in range(quantidade)]

def inicializarTarefas(listaTarefas):
    for tarefa in listaTarefas:
        tarefa["duracaoRestante"] = tarefa["duracaoTotal"]
    return ordenarPorDuracao(listaTarefas)

def ordenarPorDuracao(tarefas):
    for i in range(len(tarefas)):
        for j in range(i + 1, len(tarefas)):
            if tarefas[i]["duracaoTotal"] < tarefas[j]["duracaoTotal"]:
                tarefas[i], tarefas[j] = tarefas[j], tarefas[i]
    return tarefas

def criarHistoricoDasCpus(cpus):
    historico = {}
    for cpu in cpus:
        historico[cpu.name] = [] # E uma lista com o nome de CPU em PHP seria algo como ['nome' => []]
    return historico

# Executa o escalonador até que todas as tarefas sejam finalizadas
def executarEscalonador(tarefas, cpus, histCpu):
    tarefasFinalizadas = []

    while len(tarefasFinalizadas) < len(tarefas):
        cpusDisponiveis = cpus[:]
        filaExecucao = []

        for tarefa in tarefas:
            if tarefa["id"] in tarefasFinalizadas:
                continue
            if len(cpusDisponiveis) >= tarefa["cpusNecessarias"]:
                cpusAlocadas = []
                for _ in range(tarefa["cpusNecessarias"]):
                    cpusAlocadas.append(cpusDisponiveis.pop(0))
                filaExecucao.append((tarefa, cpusAlocadas))

        for tarefa, cpusAlocadas in filaExecucao:
            if tarefa["duracaoRestante"] <= 0:
                continue

            tempoAntes = tarefa["duracaoRestante"]
            tarefa["duracaoRestante"] -= 5
            tempoDepois = max(tarefa["duracaoRestante"], 0)

            for cpu in cpusAlocadas:
                histCpu[cpu.name].append(f'{tarefa["id"]}({tempoDepois})')

            if tempoDepois == 0:
                tarefasFinalizadas.append(tarefa["id"])

        for cpu in cpusDisponiveis:
            histCpu[cpu.name].append(".")

# Ordeno o historidco
def completarHistorico(histCpu):
    maiorTamanho = max(len(h) for h in histCpu.values())
    for h in histCpu.values():
        while len(h) < maiorTamanho:
            h.append(".")
    return maiorTamanho

# Imprimo de 10 em 10
def imprimirTabelaExecucao(histCpu, totalCiclos):
    print("\ncada ciclo = 5s, 10 por linha:\n")
    blocos = (totalCiclos + 9) // 10

    for bloco in range(blocos):
        inicio = bloco * 10
        fim = min(inicio + 10, totalCiclos)

        print("".ljust(8), end="") # é como um echo em PHP, obrigado Copilot python n faz sentido
        for i in range(inicio, fim):
            print(f"C{i+1}".center(10), end="")
        print()

        for nomeCpu in sorted(histCpu):
            print(nomeCpu.ljust(8), end="")
            for entrada in histCpu[nomeCpu][inicio:fim]:
                print(entrada.center(10), end="")
            print()
        print()

def calcularTempoTotal(histCpu):
    return max(len(h) for h in histCpu.values())

def main():
    tarefas = [
        {"id": "T1", "quantum": 10, "cpusNecessarias": 1, "duracaoTotal": 40},
        {"id": "T2", "quantum": 20, "cpusNecessarias": 2, "duracaoTotal": 20},
        {"id": "T3", "quantum": 10, "cpusNecessarias": 2, "duracaoTotal": 30},
        {"id": "T4", "quantum": 15, "cpusNecessarias": 1, "duracaoTotal": 40},
        {"id": "T5", "quantum": 15, "cpusNecessarias": 1, "duracaoTotal": 30},
        {"id": "T6", "quantum": 20, "cpusNecessarias": 4, "duracaoTotal": 60},
        {"id": "T7", "quantum": 10, "cpusNecessarias": 1, "duracaoTotal": 20},
        {"id": "T8", "quantum": 20, "cpusNecessarias": 2, "duracaoTotal": 40},
        {"id": "T9", "quantum": 15, "cpusNecessarias": 2, "duracaoTotal": 50},
        {"id": "T10", "quantum": 10, "cpusNecessarias": 4, "duracaoTotal": 60},
    ]

    cpus = inicializarCpus(4)
    tarefas = inicializarTarefas(tarefas)
    histCpu = criarHistoricoDasCpus(cpus)
    executarEscalonador(tarefas, cpus, histCpu)
    totalCiclos = completarHistorico(histCpu)
    imprimirTabelaExecucao(histCpu, totalCiclos)

    print(f"Tempo total: {totalCiclos * 5} segundos")

if __name__ == "__main__":
    main()
