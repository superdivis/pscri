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
    var btn_aplicar = document.querySelector("#btnAplicar");
    var btn_limpar_tudo = document.querySelector("#btnLimparTudo");
    var mchart ;
    
    //Inicialização da main
    function main_init(){
        painel_simulacoes();
        carrega_nivel_territorial();
        carrega_regioes();
        carrega_sistemas();
        //monta_resumo();
        //monta_top_setores(10);
        //pib_por_regiao_atividade();
        //pib_por_regiao_map();

        //Limpar cards
        limpar_resumo();
        limpar_top_setores();
        init_select_region_event();
        esconde_regioes();

        //Limpar valores atividades
        limpar_regioes_choque();
    
    };

    var limpar_atividades = function (id){
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            atividade_selecionada.value = 0;
        }
    };

    //Inicia Painel de simulações
    main_init();
        
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
    
    //Carregar painel de simulações
    btn_aplicar.addEventListener("click", function(event) {
        
        //Carrega dados e monta json
        var dados = [];
        ct = 1;
        var id_atividade = "#atividades_n_";
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id_atividade + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            var at_valor = atividade_selecionada.value;
            item = {id: ct , valor: at_valor};
            dados.push(item);
            var ct = ct + 1;
        }
        id_atividade = "#atividades_ne_";
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id_atividade + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            var at_valor = atividade_selecionada.value;
            item = {id: ct , valor: at_valor};
            dados.push(item);
            var ct = ct + 1;
        }
        id_atividade = "#atividades_su_";
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id_atividade + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            var at_valor = atividade_selecionada.value;
            item = {id: ct , valor: at_valor};
            dados.push(item);
            var ct = ct + 1;
        }
        id_atividade = "#atividades_sd_";
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id_atividade + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            var at_valor = atividade_selecionada.value;
            item = {id: ct , valor: at_valor};
            dados.push(item);
            var ct = ct + 1;
        }
        id_atividade = "#atividades_co_";
        for(let i = 1; i < 69 ; i++){
            var btn_nome_base = id_atividade + i.toString();
            var atividade_selecionada = document.querySelector(btn_nome_base);
            var at_valor = atividade_selecionada.value;
            item = {id: ct , valor: at_valor};
            dados.push(item);
            var ct = ct + 1;
        }
        
        dados_delta_y = {dados};
        aplicar_choque_completo(dados_delta_y);
    });  
    
    //Carregar painel de simulações
    btn_limpar_tudo.addEventListener("click", function(event) {
        limpar_regioes_choque();
    });  

    function limpar_regioes_choque(){
        limpar_atividades("#atividades_n_");
        limpar_atividades("#atividades_ne_");
        limpar_atividades("#atividades_sd_");
        limpar_atividades("#atividades_su_");
        limpar_atividades("#atividades_co_");
    };

});