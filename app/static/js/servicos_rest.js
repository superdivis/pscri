// +-------------------------------------------------------------+
// | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
// | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
// | Data inicio: 01/07/2024                                     |
// | Data finalização: xx/xx/xx                                  |
// | Autor: Alexandre Silva dos Santos                           |
// | Email: alexandresantoscompunb@gmail.com                     |
// | Módulo: Rotinas rest                                        |
// +-------------------------------------------------------------+----------------------------------------------------------

var ip_api = 'http://191.252.177.176';
//var ip_api = 'http://localhost:5000';


// +-----------------------------------------------------------------------------------
//
//   *******      ********  **         ********   **********   ********
//  /**////**   /**/////   /**        /**/////   /////**///   /**///// 
//  /**    /**  /**        /**        /**            /**      /**      
//  /**    /**  /*******   /**        /*******       /**      /******* 
//  /**    /**  /**////    /**        /**////        /**      /**////  
//  /**    **   /**        /**        /**            /**      /**      
//  /*******    /********  /********  /********      /**      /********
//  ///////     ////////   ////////   ////////       //        //////// 
//
// +-----------------------------------------------------------------------------------

function funcao_btn_confirma_delete(id_simulacao){
    var xhr = new XMLHttpRequest(id_simulacao);
    xhr.open("DELETE", ip_api + "/simulacao/excluir/"+id_simulacao, true);
    xhr.send();
    xhr.onload =function(){
        console.log(xhr.status)
        if(xhr.status===200){
            id_li=document.getElementById("id_li")
            id_li.remove();
            console.log('Deletado com sucesso '+id_simulacao)
        }else if(xhr.status==400){
            console.log('Não foi posivel deletar')
        }
    }
};

// +-----------------------------------------------------------------------------------
//
//    ********     ********  **********
//   **//////**   /**/////  /////**/// 
//  **      //    /**           /**    
//  /**           /*******      /**    
//  /**    *****  /**////       /**    
//  //**  ////**  /**           /**    
//   //********   /********     /**    
//    ////////    ////////      //     
//
// +-----------------------------------------------------------------------------------
function painel_simulacoes(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api + "/simulacoes", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let simulacao = JSON.parse(xhr.response);
            var $simu_tela = $('#simu_tela');
            $simu_tela.empty();
            for (let i in simulacao) {
                var id_simulacao = simulacao[i].id;
                var nome_simulacao = simulacao[i].nome;

                var html='<li id="id_li" class="d-flex align-items-center border-bottom py-3">';
                html +=        '<small class="d-inline-block text-truncate" style="max-width: 270px;">'+nome_simulacao+'</small>';
                html +=        '<div class="ms-auto">';
                html +=              '<button class="btn btn-outline-secondary btn-sm mb-3 mb-lg-0" data-bs-toggle="modal" data-bs-target="#deleteModal" onclick="funcao_btn_delete(' + "'" + nome_simulacao + "'" + ','+ id_simulacao + ');"><i class="fa-solid fa-trash"></i></button>';
                html +=              '<button class="btn btn-outline-success btn-sm mb-3 mb-lg-0" onclick=" funcao_btn_confirm('+id_simulacao+')"><i class="fa-solid fa-check"></i></button>';
                html +=        '</div>';
                html +=  '</li>';
                $simu_tela.append(html);
            }
        }
    }
};

function carregar_simulacao(id_simulacao){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api + "/simulacao/"+id_simulacao, true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let simulacao = JSON.parse(xhr.response);
            carrega_informacoes_simulacao(simulacao);
        }
    }
};

function carrega_nivel_territorial(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api + "/nivelterritorial", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let lstNvTerritorial = JSON.parse(xhr.response);
            var $select = $('#sel_nv_territorial');
            for (let i in lstNvTerritorial) {
                // Cria uma nova opção
                $select.append('<option value="'+lstNvTerritorial[i].id+'">'+lstNvTerritorial[i].nome+'</option>');
            }
            $select.selectpicker('refresh');
            $select.selectpicker('val', '1');
        }
    }
};

function carrega_regioes(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api + "/regioes", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let lstRegioes = JSON.parse(xhr.response);
            var $select = $('#sel_regioes');
            for (let i in lstRegioes) {
                // Cria uma nova opção
                $select.append('<option value="'+lstRegioes[i].id+'">'+lstRegioes[i].nome+'</option>');
            }
            $select.selectpicker('refresh');
            //$select.selectpicker('val', '1');
        }
    }
};

function carrega_sistemas(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api +"/sistemas", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let lstSistemas = JSON.parse(xhr.response);
            var $select = $('#sel_sistemas');
            for (let i in lstSistemas) {
                // Cria uma nova opção
                $select.append('<option value="' + lstSistemas[i].id+'">' + lstSistemas[i].nome + '</option>');
            }
            $select.selectpicker('refresh');
            $select.selectpicker('val', '0');
        }
    }
};

//Atualiza tabela resumo
function monta_resumo(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api +"/resumo", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let resumo = JSON.parse(xhr.response);
            carrega_informacoes_resumo(resumo);
            monta_top_setores(10);
        }
    }
};

//Atualiza tabela com os top pib e setores que sofreram maior impacto
function monta_top_setores(qt_setores){
    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api +"/pib_novo_top", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let top_setores = JSON.parse(xhr.response);
            carrega_informacoes_top_setores(top_setores,qt_setores);
            pib_por_regiao_atividade();       
        }
    }
};

//Atualiza treemap com dados retornados do serviço
function pib_por_regiao_atividade(){

    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api +"/pib_novo_completo_atividades", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status==200){
           let pib_setores_regiao = JSON.parse(xhr.response);
           carrega_informacoes_pib_setores_regiao(pib_setores_regiao);
           pib_por_regiao_map();  
        }else if(xhr.status==404){
            alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  
}

//Atualiza mapa com dados retornados do serviço
function pib_por_regiao_map(){

    const xhr = new XMLHttpRequest();
    xhr.open("GET",ip_api +"/pib_por_regiao", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status==200){
           let pib_por_regiao = JSON.parse(xhr.response);
           carrega_informacoes_mapa(pib_por_regiao);
        }else if(xhr.status==404){
           alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  
}

//Atualiza mapa com dados retornados do serviço
function aplicar_choque_completo(delta_y){

    const xhr = new XMLHttpRequest();
    xhr.open("POST",ip_api +"/enviar_delta_y", true);
    xhr.setRequestHeader("Content-Type", "application/json","Access-Control-Allow-Origin", "*");
    xhr.send(JSON.stringify(delta_y));
    
    //Reposta da aplicação do choque
    xhr.onload= function(){
        if(xhr.status==201){
           let pib_por_regiao = JSON.parse(xhr.response);     
           aplicar_choque_v2();
        }else if(xhr.status==404){
           alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  
}

//Atualiza mapa com dados retornados do serviço
function aplicar_choque_carrega_infos(delta_y){

    //Verifica presença de valores em delta_y
    if(!validar_delta_y(delta_y)){
        //Limpar cards
        $('#warningModal').modal('show');
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST",ip_api +"/aplicar_choque", true);
    xhr.setRequestHeader("Content-Type", "application/json","Access-Control-Allow-Origin", "*");
    xhr.send(JSON.stringify(delta_y));

    xhr.onload= function(){
        if(xhr.status==201){
           //Recebe informações para carga da interface
           let infos_interface = JSON.parse(xhr.response);     
           carrega_infos_interface(infos_interface);
        }else if(xhr.status==404){
           alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  
}
