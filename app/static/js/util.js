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
};


function aplicar_choque_v2 (){
    monta_resumo();
};

function esconde_regioes(){
    $("#rg_norte").hide();
    $("#rg_nordeste").hide();
    $("#rg_sul").hide();
    $("#rg_sudeste").hide();
    $("#rg_centroOeste").hide();
};

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
};

function funcao_btn_delete(nome,id){
    document.getElementById("id_nome_simulacao").textContent = nome;
    document.getElementById("id_btn_modal_delete_confirm").id_delete = id;
};


function funcao_btn_confirm(id_simulacao){
    console.log('Simulação confirmada '+ id_simulacao)
};

//Limpar resumo
function limpar_resumo(){
    var $tb_resumo = $('#tb_resumo tbody');
    $tb_resumo.empty();
};

//Limpar top atividades/atividade
function limpar_top_setores(){
    var $tb_top_setores = $('#tb_top_setores tbody');
    $tb_top_setores.empty();
};

function atualiza_mapa(dados){
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


};

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
};

