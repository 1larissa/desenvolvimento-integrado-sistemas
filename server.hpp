//Nos arquivos .h, você cria os metodos, no cpp você expecifica eles

#pragma once /*Sempre coloque em todo .h pra
                não ter problema de include*/
#include <stdio.h> 
#include <string>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>

// struct global da solicitacao de reconstrucao de imagem
struct solicitacao {
    // id da solicitacao
    int id;
    // nome do modelo de matriz
    std::string modelo_nome;
    // tamanho do problema
    int linhas; 
    int colunas; 
    // o modelo de matriz H
    std::vector<double> matriz;
    // o sinal g
    std::vector<double> sinal;
    // qual algoritmo usado
    std::string algoritmo;
    // numero de vezes que cedeu a vez para outra imagem rodar ao inves dela rodar..
    int cedido;
    // numero de iteracoes
    int total_interacoes;
    // tempo total reconstrução
    int tempo_reconstrucao;
    // imagem final f
    std::vector<double> imagem_reconstruida;
};

class Server{
    private:
        //atributos e outros itens
        // atributos para controlar a comunicacao
        // fila de imagens a processar
        std::queue<solicitacao> fila_solicitacoes;
        // fila de imagens prontas
        std::queue<solicitacao> fila_solicitacoes_prontas;

        // mutex pra previnir a disputa de acesso
        // std::mutex mutex_fila;
        // uma condicao de acesso
        // std::condition_variable cond_fila;

    public:
        //metodos gerais

        Server();
        void iniciarServidor();
        int runinC();
        int runinPython();
        int enviaDadosCliente();
        // metodos para o gerenciador de fila (sera q precisamos de outra classe "gerenciador de fila"?)

        void adicionarSolicitacao(const solicitacao& nova_solicitacao);
        // retorna e remove uma solicitação da fila
        bool obterProximaSolicitacao(solicitacao& proxima_solicitacao);
};
