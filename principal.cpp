#include "principal.h"//tem que adicionar o header correspondente
#include <iostream>//Biblioteca de print
#include "server.h"

principal::principal(){
    //inicializa atributos
}

void principal::executar(){
    server server;
    server.iniciarServidor();
}



