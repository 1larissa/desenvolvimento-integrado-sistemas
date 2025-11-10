// O servidor irá rodar em 1 instância com multiplas threads, 
// para tratar a reconstrução da imagem
// A criação de outras threads alem da principal se da caso haja espaço em 
// memoria e na CPU


// struct global da solicitacao de reconstrucao de imagem
    // id da solicitacao
    // qual modelo
    // qual sinal
    // qual algoritmo usado
    // numero de vezes que cedeu a vez para outra imagem rodar ao inves dela rodar..
    // numero de iteracoes
    // tempo total reconstrução

// Acho q a fila de solicitações tambem pode ser global...

// defino GLOBAL quanto mais ou menos eh o consumo de memoria para poder 
// processar o modelo 1 (grande 60*60) e o modelo 2 (pequeno 30*30)


// Inicializa o servidor geral

    // Inicializa o processamento em c++

        // Enquanto a comunicação estiver aberta
        // Deixa a porta de comunicacao liberada,
        // vai recebendo as solicitações e 
        // colocando no final da fila

         // Enquanto a comunicação estiver aberta ou a fila não estiver vazia

            // Vou reconstruir cada imagem da fila de solicitacoes

            // Antes de tratar uma solicitação o gerenciador da fila 
            // escolhe qual a proxima a ser tratada
                // verifico se a escolhida eh do modelo grande ou pequeno
                // dai verifico se existe espaco para rodar,
                // se nao ou tento encaixar um menor da fila, dai marco que essa
                // tarefa cedeu a sua vez para outra rodar++
                // se nao deixo ocioso mesmo ate liberar espaco

            // Abre nova thread
            // Reconstroi a imagem com o algoritmo escolhido
                // A cada 1s gera o relatorio de como esta o consumo de CPU e memoria
            // Encerra a thread

            // Gera o relatório da imagem criada dizendo qual o numero da solicitacao
            // número de iterações e tempo total de reconstrução

            // Salva em uma lista, dicionario, sei la..todas as imagens e informaçoes de processamento

        // Retorna toda a lista reconstruida para os clientes

    // Encerro o processamento em c++
    // Inicializo o processamento em python
    // Igual em c++
