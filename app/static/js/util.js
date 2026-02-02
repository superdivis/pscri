// +-------------------------------------------------------------+
// | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
// | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
// | Data inicio: 01/07/2024                                     |
// | Data finalização: xx/xx/xx                                  |
// | Autor: Alexandre Silva dos Santos                           |
// | Email: alexandresantoscompunb@gmail.com                     |
// | Módulo: Rotinas gerais do projeto                           |
// +-------------------------------------------------------------+----------------------------------------------------------

// Aplicação do choque
function aplicar_choque (){
    monta_resumo();
    monta_top_setores(10);
    pib_por_regiao_atividade();
    pib_por_regiao_map();
}


function aplicar_choque_v2 (){
    monta_resumo();
}

function esconde_regioes(){
    $("#rg_norte").hide();
    $("#rg_nordeste").hide();
    $("#rg_sul").hide();
    $("#rg_sudeste").hide();
    $("#rg_centroOeste").hide();
}

function exibe_regioes(item){
   var lbl = item.label;
    if( lbl == "Norte"){
        $("#rg_norte").show();
   }else if(lbl == "Nordeste"){
        $("#rg_nordeste").show();
    }else if(lbl == "Sul"){
        $("#rg_sul").show();
    }else if(lbl == "Sudeste"){
        $("#rg_sudeste").show();
    }else if(lbl == "Centro-Oeste"){
        $("#rg_centroOeste").show();
   }
}

function funcao_btn_delete(nome,id){
    document.getElementById("id_nome_simulacao").textContent = nome;
    document.getElementById("id_btn_modal_delete_confirm").id_delete = id;
}


function funcao_btn_confirm(id_simulacao){
    console.log('Simulação confirmada '+ id_simulacao)
}

//Limpar resumo
function limpar_resumo(){
    var $tb_resumo = $('#tb_resumo tbody');
    $tb_resumo.empty();
}

//Limpar top atividades/atividade
function limpar_top_setores(){
    var $tb_top_setores = $('#tb_top_setores tbody');
    $tb_top_setores.empty();
}

function init_select_region_event(){
    const selectDropdown = document.querySelector('#sel_regioes');
    selectDropdown.addEventListener('change', 
        function (e) {
            /* your code */
            let opts =  e.target.selectedOptions;
            esconde_regioes();
            for(let i = 0; i < opts.length ; i++){
                exibe_regioes(opts[i])
            }
        });
}


//+-------------------------------------------+
//| Função: carrega_informacoes_resumo        |
//| Descrição: Função principal que chama     |
//| as funções de apoio para carga  completa  | 
//| das informação na inteface do sistema.    |
//| parâmetro: resumo - json com infos.       |
//+-------------------------------------------+--------------------------------------------------------
function carrega_infos_interface(infos_interface){
    let qt_setores = 10;
    carrega_informacoes_resumo(infos_interface.resumo);
    carrega_informacoes_top_setores(infos_interface.top_setores, qt_setores);
    carrega_informacoes_pib_setores_regiao(infos_interface.pib_por_regiao);
    carrega_informacoes_mapa(infos_interface.info_mapa);
}

//+-------------------------------------------+
//| Função: carrega_informacoes_resumo        |
//| Descrição: Função de apoio que insere     |
//| as informações de resumo na inteface.     |
//| parâmetro: resumo - json com infos.       |
//+-------------------------------------------+--------------------------------------------------------
function carrega_informacoes_resumo (resumo) {
    var $tb_resumo = $('#tb_resumo tbody');
    $tb_resumo.empty();
    let str_tb_resumo = ""; 
    if(resumo.per_pib_n > 0.01){
        str_tb_resumo =  '<tr><td>Norte</td><td class="text-center">'+ resumo.multiplicador_n +'</td><td class="text-center">' + resumo.vazamento_n + '%</td><td class="text-center">' + resumo.per_pib_n + '%</td></tr>'
    }
                
    if (resumo.per_pib_ne > 0.01){
        str_tb_resumo = str_tb_resumo + '<tr><td>Nordeste</td><td class="text-center">'+ resumo.multiplicador_ne +'</td><td class="text-center">' + resumo.vazamento_ne + '%</td><td class="text-center">' + resumo.per_pib_ne + '%</td></tr>'
    }
    
    if (resumo.per_pib_se > 0.01){
        str_tb_resumo = str_tb_resumo + '<tr><td>Sudeste</td><td class="text-center">'+ resumo.multiplicador_se +'</td><td class="text-center">' + resumo.vazamento_se + '%</td><td class="text-center">' + resumo.per_pib_se + '%</td></tr>'
    }
    
    if (resumo.per_pib_s > 0.01){
        str_tb_resumo = str_tb_resumo + '<tr><td>Sul</td><td class="text-center">'+ resumo.multiplicador_s +'</td><td class="text-center">' + resumo.vazamento_s + '%</td><td class="text-center">' + resumo.per_pib_s + '%</td></tr>'
    }        

    if (resumo.per_pib_co > 0.01){
        str_tb_resumo = str_tb_resumo + '<tr><td>Centro-Oeste</td><td class="text-center">'+ resumo.multiplicador_co +'</td><td class="text-center">' + resumo.vazamento_co + '%</td><td class="text-center">' + resumo.per_pib_co + '%</td></tr>'
    }

    $tb_resumo.append(str_tb_resumo);
}

//+---------------------------------------------+
//| Função: carrega_informacoes_top_setores     |
//| Descrição: Função de apoio que insere       |
//| as informações dos top setores na           |
//| interface.                                  |
//| parâmetro: top_setores - json               |
//|            qt_setores  - int                |
//+---------------------------------------------+-----------------------------------------------------
function carrega_informacoes_top_setores(top_setores, qt_setores){
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

//+-----------------------------------------------+
//| Função: carrega_informacoes_pib_setores_regiao|
//| Descrição: Função de apoio que insere         |
//| as informações dos top setores na             |
//| interface.                                    |
//| parâmetro: pib_setores_regiao - json com infos|
//+-----------------------------------------------+---------------------------------------------------
function carrega_informacoes_pib_setores_regiao(pib_setores_regiao) {
    series.data.setAll([pib_setores_regiao]);
}

//+-----------------------------------------------+
//| Função: carrega_informacoes_mapa              |
//| Descrição: Função de apoio que atualiza as    |
//| informações dos setores na mapa de regiões.   |
//| parâmetro: dados - json com as infos          |
//+-----------------------------------------------+---------------------------------------------------
//function atualiza_mapa(dados){
function carrega_informacoes_mapa(dados){
   // Dados das regiões com valores para o heatmap (exemplo: população em milhões)
   regionPIBAtual = {
        "Norte": dados.delta_pib_total_n,
        "Nordeste": dados.delta_pib_total_ne,
        "Centro-Oeste": dados.delta_pib_total_co,
        "Sudeste": dados.delta_pib_total_se,
        "Sul": dados.delta_pib_total_s
    };

    // Dados das regiões com valores para o heatmap (exemplo: população em milhões)
    regionPIBNovo = {
        "Norte": dados.pib_total_n,
        "Nordeste": dados.pib_total_ne,
        "Centro-Oeste": dados.pib_total_co,
        "Sudeste": dados.pib_total_se,
        "Sul": dados.pib_total_s
    };
    
    //Define mapa 
    if (polygonSeries == undefined){
        polygonSeries = mchart.series.push(
            am5map.MapPolygonSeries.new(map_root, {
                //geoJSON: am5geodata_region_americas_brazilLow
                geoJSON: am5geodata_brazilLow
            })
        );

        // Aplicar as cores do heatmap
        polygonSeries.mapPolygons.template.adapters.add("fill", function(fill, target) {
            var region = stateToRegion[target.dataItem.dataContext.name];
            var value01 = regionPIBAtual[region] || minValue;
            var value02 = regionPIBNovo[region] || minValue;
            target.dataItem.dataContext.region = region;
            target.dataItem.dataContext.valor_pib_atual = value01;
            target.dataItem.dataContext.valor_pib_novo = value02;
            if (region) {
                if (region == "Norte") {
                    return corNorte; /* Vermelho */
                } else if (region == "Nordeste") {
                    return corNordeste; /* Azul Claro */
                } else if (region == "Sul") {
                    return corSul; /* Verde Forte */
                } else if (region == "Sudeste") {
                    return corSudeste; /* Laranja */
                } else {
                    return corCentroOeste; /* Roxo */
                }
            }
            return fill;
        });

        polygonSeries.mapPolygons.template.setAll({
            tooltipText: "Região: " + "{region}" +"\n" + "ΔPIB: " + "{valor_pib_atual}" +"\n" + "PIB novo: " + "{valor_pib_novo}" ,
            //tooltipText: regionData[region],
            interactive: true
        });

        polygonSeries.mapPolygons.template.states.create("hover", {
            fill: am5.color("#ffff99")
        });
   }
   
   //Cria legenda
   if(legend == undefined){
        var corNorte = am5.color("#5AAA95"); 
        var corNordeste = am5.color("#BB9F06"); 
        var corSudeste = am5.color("#08578C"); 
        var corSul = am5.color("#76A873"); 
        var corCentroOeste = am5.color("#092456"); 
    
        legend = mchart.children.push(am5.Legend.new(map_root, {
            nameField: "name",
            fillField: "color",
            strokeField: "color",
            useDefaultMarker: true,
            centerX: am5.p100,
            maxWidth: 100,
            x: am5.p100,
            centerY: am5.p100,
            y: am5.p100,
            dx: 10,
            dy: -20,
            background: am5.RoundedRectangle.new(map_root, {
            fill: am5.color(0xffffff),
            fillOpacity: 0.3
            })
        }));

        legend.data.setAll([{
            name: "Norte",
            color: corNorte
        }, {
            name: "Nordeste",
            color: corNordeste
        }, {
            name: "Centro Oeste",
            color: corCentroOeste
        }, {
            name: "Sudeste",
            color: corSudeste
        }, {
            name: "Sul",
            color: corSul
        }]);
    }
}

//+-----------------------------------------------+
//| Função: carrega_informacoes_simulacao         |
//| Descrição: Função de apoio que atualiza as    |
//| informações dos setores na mapa de regiões.   |
//| parâmetro: dados - json com as infos          |
//+-----------------------------------------------+---------------------------------------------------
function carrega_informacoes_simulacao (simulacao){
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

function validar_delta_y(delta_y){
    ret = false;
    for(i=0; i < delta_y.dados.length; i++){ 
        if (parseInt(delta_y.dados[i].valor) > 0) {
            return true    
        }
    }
    return ret;
}