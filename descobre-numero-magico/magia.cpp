// descobre quanto consome de cpu e de memoria para processar em cada modelo
// para poder usar essa medida na comparacao do server e ver se consegue rodar 
// outra imagem ao mesmo tempo sem crashar o sistema

// esse teste roda 100 vezes a reconstrucao de uma imagem
// para ter a nocao de quanto de cpu e memoria eh utilizado

// leio o csv

// enquanto tentativa <= 100
    // aplico o algoritmo
    // monitoro o cpu/mem antes da execucao
    // monitoro se houve algum pico(max) no cpu/mem durante a execucao
    // monitoro o cpu/mem depois da execucao
    // imprimo tudo isso
// faco uma media de consumo antes da execucao, depois e dos picos
// imprimo tb
