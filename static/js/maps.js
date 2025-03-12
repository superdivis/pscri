var map_root;
var heatLegend;
var polygonSeries;
var mchart;

// Dados das regiões com valores para o heatmap (exemplo: população em milhões)
var regionPIBAtual;
// Dados das regiões com valores para o heatmap (exemplo: população em milhões)
var regionPIBNovo;

// Definição da escala de cores (de azul para vermelho)
var minColor;
var maxColor; 

// Encontra o mínimo e o máximo dos valores
var minValue;
var maxValue;

// Associação de estados às regiões
var stateToRegion;

am5.ready(function() {
    map_root = am5.Root.new("mapdiv");
    map_root.setThemes([ am5themes_Animated.new(map_root) ]);

    
    //var corNorte = am5.color("#E9F0A0"); 
    //var corNorte = am5.color("#FF0000"); 
    //var corNordeste = am5.color("#0080FF"); 
    //var corSudeste = am5.color("#FFA500"); 
    //var corSul = am5.color("#00C800"); 
    //var corCentroOeste = am5.color("#800080"); 

    var corNorte = am5.color("#5AAA95"); 
    var corNordeste = am5.color("#BB9F06"); 
    var corSudeste = am5.color("#08578C"); 
    var corSul = am5.color("#76A873"); 
    var corCentroOeste = am5.color("#092456"); 
    
    mchart = map_root.container.children.push(
        am5map.MapChart.new(map_root, {
            panX: "rotateX",
            panY: "translateY",
            projection: am5map.geoMercator()
        })
    );

    polygonSeries = mchart.series.push(
        am5map.MapPolygonSeries.new(map_root, {
            //geoJSON: am5geodata_region_americas_brazilLow
            geoJSON: am5geodata_brazilLow
        })
    );

    // Dados das regiões com valores para o heatmap (exemplo: população em milhões)
    regionPIBAtual = {
        "Norte": 15,      // Exemplo: 18 milhões
        "Nordeste": 57,
        "Centro-Oeste": 10,
        "Sudeste": 90,
        "Sul": 30
    };

    // Dados das regiões com valores para o heatmap (exemplo: população em milhões)
    regionPIBNovo = {
        "Norte": 30,      // Exemplo: 18 milhões
        "Nordeste": 114,
        "Centro-Oeste": 20,
        "Sudeste": 180,
        "Sul": 60
    };

    // Associação de estados às regiões
    stateToRegion = {
        "Acre": "Norte", "Amapá": "Norte", "Amazonas": "Norte", "Pará": "Norte", "Rondônia": "Norte", "Roraima": "Norte", "Tocantins": "Norte",
        "Alagoas": "Nordeste", "Bahia": "Nordeste", "Ceará": "Nordeste", "Maranhão": "Nordeste", "Paraíba": "Nordeste", "Pernambuco": "Nordeste", "Piauí": "Nordeste", "Rio Grande do Norte": "Nordeste", "Sergipe": "Nordeste",
        "Distrito Federal": "Centro-Oeste", "Goiás": "Centro-Oeste", "Mato Grosso": "Centro-Oeste", "Mato Grosso do Sul": "Centro-Oeste",
        "Espírito Santo": "Sudeste", "Minas Gerais": "Sudeste", "Rio de Janeiro": "Sudeste", "São Paulo": "Sudeste",
        "Paraná": "Sul", "Rio Grande do Sul": "Sul", "Santa Catarina": "Sul"
    };

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

    // Legend
    var legend = mchart.children.push(am5.Legend.new(map_root, {
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

});
