// O servidor irá rodar em 1 instância com multiplas threads, 
// para tratar a reconstrução da imagem
// A criação de outras threads alem da principal se da caso haja espaço em 
// memoria e na CPU

// defino GLOBAL quanto mais ou menos eh o consumo de memoria para poder 
// processar o modelo 1 (grande 60*60) e o modelo 2 (pequeno 30*30)

#include "server.h"//tem que adicionar o header correspondente
#include <iostream>//Biblioteca de print
using namespace std;

server::server(){

}   

void server::iniciarServidor(){
    // Inicializa o servidor geral
    cout << "Servidor Principal Inicializado!\n";

    // Inicializa o processamento em c++
    if (!runinC()) {cout << "Processamento em C finalizado!\n";}
    else {cout << "Erro durante o processamento em C++!\n";};

    // // Inicializa o processamento em Python
    // if (!runinPython()) {cout << "Processamento em Python finalizado!\n";}
    // else {cout << "Erro durante o processamento em Python!\n";};

    // // Retorna as imagens reconstruidas e os dados para os clientes
    // if(!enviaDadosCliente()) {cout << "Dados enviados ao cliente com sucesso!\n";}
    // else {cout << "Erro ao enviar dados ao cliente!\n";}
}
int server::runinC(){
        cout << "Iniciando o processamento em C++!\n";

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
    return 0;
}

int server::runinPython(){
    cout << "Iniciando o processamento em Python!\n";
    return 0;
}

int server::enviaDadosCliente(){
        // Retorna toda a lista de imagens reconstruidas para os clientes
    return 0;
}
