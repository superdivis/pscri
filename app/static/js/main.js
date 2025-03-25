// +-------------------------------------------------------------+
// | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
// | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
// | Data inicio: 01/07/2024                                     |
// | Data finalização: xx/xx/xx                                  |
// | Autor: Alexandre Silva dos Santos                           |
// | Email: alexandresantoscompunb@gmail.com                     |
// | Módulo: Javascript principal                                |
// +-------------------------------------------------------------+----------------------------------------------------------

window.addEventListener('load', function() { 
    //Definição de objetos 
    var formulariodecaptura=document.querySelector("#id_formulario_de_captura");
    var btn_simulacoes = document.querySelector("#id_btn_simulacoes");
    var btn_modal_delete_confirm = document.querySelector("#id_btn_modal_delete_confirm");

    //Inicia Painel de simulações
    painel_simulacoes();
    carrega_nivel_territorial();
    carrega_regioes();
    carrega_sistemas();
    monta_resumo();
    monta_top_setores(10);
    pib_por_regiao_atividade();
    pib_por_regiao_map();
        
    //carregar_simulacao(2);

    //Carregar painel de simulações
    btn_simulacoes.addEventListener("click", function(event) {
        painel_simulacoes();
    });     

    //Ação do botão de exclusão de simulações
    btn_modal_delete_confirm.addEventListener("click", function(event) {
        id_simulacao=document.getElementById("id_btn_modal_delete_confirm").id_delete        
        funcao_btn_confirma_delete(id_simulacao);
    });     

});