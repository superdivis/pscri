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
