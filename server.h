//Nos arquivos .h, você cria os metodos, no cpp você expecifica eles

#pragma once /*Sempre coloque em todo .h pra
                não ter problema de include*/
#include <stdio.h> 
#include <string>
#include <vector>

class server{
    private:
        //atributos e outros itens
            // atributos para controlar a comunicacao
        // fila de imagens a processar
        // fila de imagens prontas
    public:
        //metodos
        server();
        void iniciarServidor();
        int runinC();
        int runinPython();
        int enviaDadosCliente();
};

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