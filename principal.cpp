#include "principal.hpp"//tem que adicionar o header correspondente
#include <iostream>//Biblioteca de print
#include "server.hpp"

Principal::Principal(){
    //inicializa atributos
}

void Principal::executar(){
    Server server;
    server.iniciarServidor();
}



