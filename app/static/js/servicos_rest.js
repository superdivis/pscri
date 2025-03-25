// +-------------------------------------------------------------+
// | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
// | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
// | Data inicio: 01/07/2024                                     |
// | Data finalização: xx/xx/xx                                  |
// | Autor: Alexandre Silva dos Santos                           |
// | Email: alexandresantoscompunb@gmail.com                     |
// | Módulo: Rotinas rest                                        |
// +-------------------------------------------------------------+----------------------------------------------------------


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
    xhr.open("DELETE", "/simulacao/excluir/"+id_simulacao, true);
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
    xhr.open("GET","/simulacoes", true);
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
    xhr.open("GET","/simulacao/"+id_simulacao, true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let simulacao = JSON.parse(xhr.response);
            
            var accordion_norte = $('#norte');
            var accordion_nordeste = $('#nordeste');
            var accordion_centro_oeste = $('#centroOeste');
            var accordion_sul = $('#sul');
            var accordion_sudeste = $('#sudeste');
            
            //Clean regions content
            accordion_norte.empty();
            accordion_nordeste.empty();
            accordion_centro_oeste.empty();
            accordion_sul.empty();
            accordion_sudeste.empty();

            for (let i in simulacao) {
                var descricaoatividade = simulacao[i].descricaoatividade;
                var id_atividade = simulacao[i].id_atividade;
                var id_regiao = simulacao[i].id_regiao;
                var id_simulacao = simulacao[i].id_simulacao;
                var nome = simulacao[i].nome;
                var nome_regiao = simulacao[i].nome_regiao;
                var valor = simulacao[i].valor;

               /*
                var html='<li id="id_li" class="d-flex align-items-center border-bottom py-3">';
                html +=        '<small class="d-inline-block text-truncate" style="max-width: 270px;">'+nome_simulacao+'</small>';
                html +=        '<div class="ms-auto">';
                html +=              '<button class="btn btn-outline-secondary btn-sm mb-3 mb-lg-0" data-bs-toggle="modal" data-bs-target="#deleteModal" onclick="funcao_btn_delete(' + "'" + nome_simulacao + "'" + ','+ id_simulacao + ');"><i class="fa-solid fa-trash"></i></button>';
                html +=              '<button class="btn btn-outline-success btn-sm mb-3 mb-lg-0" onclick=" funcao_btn_confirm('+id_simulacao+')"><i class="fa-solid fa-check"></i></button>';
                html +=        '</div>';
                html +=  '</li>';
                $simu_tela.append(html);*/
            }
        }
    }
};

function carrega_nivel_territorial(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET","/nivelterritorial", true);
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
    xhr.open("GET","/regioes", true);
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
            $select.selectpicker('val', '1');
        }
    }
};

function carrega_sistemas(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET","/sistemas", true);
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
    xhr.open("GET","/resumo", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let resumo = JSON.parse(xhr.response);
            var $tb_resumo = $('#tb_resumo tbody');
            $tb_resumo.empty();
            let str_tb_resumo =  '<tr><td>Norte</td><td class="text-center">'+ resumo.multiplicador_n +'</td><td class="text-center">' + resumo.vazamento_n + '%</td><td class="text-center">' + resumo.per_pib_n + '%</td></tr>'
			str_tb_resumo = str_tb_resumo + '<tr><td>Nordeste</td><td class="text-center">1.50</td><td class="text-center">15%</td><td class="text-center">0.12%</td></tr>'
            str_tb_resumo = str_tb_resumo + '<tr><td>Sudeste</td><td class="text-center">1.71</td><td class="text-center">6%</td><td class="text-center">0.03%</td></tr>'
            str_tb_resumo = str_tb_resumo + '<tr><td>Sul</td><td class="text-center">1.54</td><td class="text-center">17%</td><td class="text-center">0.10%</td></tr>'
            str_tb_resumo = str_tb_resumo + '<tr><td>Centro-Oeste</td><td class="text-center">1.84</td><td class="text-center">32%</td><td class="text-center">0.14%</td></tr>'
            $tb_resumo.append(str_tb_resumo);
        }
    }
};

//Atualiza tabela com os top pib e setores que sofreram maior impacto
function monta_top_setores(qt_setores){
    const xhr = new XMLHttpRequest();
    xhr.open("GET","/pib_novo_top", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status===200){
            let top_setores = JSON.parse(xhr.response);
            var $tb_top_setores = $('#tb_top_setores tbody');
            $tb_top_setores.empty();
            let str_tb_top_setores = '';
            for (var i = 0; i < qt_setores; i++) {
                // Cria uma nova opção
                str_tb_top_setores = '<tr><td>'+ top_setores[i].desc_atividade +'</td>' +
                '<td><div class="row no-gutters align-items-center"><div class="col"><div class="progress me-2" style="height: 8px">' +
                '<div class="progress-bar bg-danger" role="progressbar" style="width: '+ top_setores[i].pib_participacao +'%" aria-valuenow="8" aria-valuemin="0" aria-valuemax="8">' + 
                '</div></div></div><div class="col-auto"><span>'+ top_setores[i].pib_participacao + '%</span></div></div></td>'+
                '<td class="text-center">' + top_setores[i].delta_x + '</td>'+
                '<td class="text-center">' + top_setores[i].perc_crescimento + '%</td>'+
                '<td>'+ top_setores[i].nome_regiao +'</td></tr>';
                $tb_top_setores.append(str_tb_top_setores);
            }          
        }
    }
};

//Atualiza treemap com dados retornados do serviço
function pib_por_regiao_atividade(){

    const xhr = new XMLHttpRequest();
    xhr.open("GET","/pib_novo_completo_atividades", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status==200){
           let pib_setores_regiao = JSON.parse(xhr.response);
           series.data.setAll([pib_setores_regiao]);
        }else if(xhr.status==404){
            alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  

}

//Atualiza mapa com dados retornados do serviço
function pib_por_regiao_map(){

    const xhr = new XMLHttpRequest();
    xhr.open("GET","/pib_por_regiao", true);
    xhr.send();
    xhr.onload= function(){
        if(xhr.status==200){
           let pib_por_regiao = JSON.parse(xhr.response);
           atualiza_mapa(pib_por_regiao);
        }else if(xhr.status==404){
           alert ("Erro no serviço - pib_novo_completo_atividades");
        }
    }  

}