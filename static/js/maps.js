am5.ready(function() {
    // Cria o root do gráfico
    let root = am5.Root.new("mapdiv");

    // Adiciona um tema
    root.setThemes([
        am5themes_Animated.new(root)
    ]);

    // Cria o mapa do tipo ChartMap
    let chart = root.container.children.push(
        am5map.MapChart.new(root, {
            projection: am5map.geoMercator()
        })
    );

    // Define as regiões e seus estados
    const regions = {
        Norte: ["BR-AC", "BR-AP", "BR-AM", "BR-PA", "BR-RO", "BR-RR", "BR-TO"],
        Nordeste: ["BR-AL", "BR-BA", "BR-CE", "BR-MA", "BR-PB", "BR-PE", "BR-PI", "BR-RN", "BR-SE"],
        CentroOeste: ["BR-DF", "BR-GO", "BR-MT", "BR-MS"],
        Sudeste: ["BR-ES", "BR-MG", "BR-RJ", "BR-SP"],
        Sul: ["BR-PR", "BR-RS", "BR-SC"]
    };

    // Define as cores para cada região
    const regionColors = {
        Norte: am5.color(0x67B7DC),      // Rosa claro (algodão doce)
        Nordeste: am5.color(0x6771DC),   // Laranja pastel suave (algodão doce)
        CentroOeste: am5.color(0xA367DC),// Azul claro (algodão doce)
        Sudeste: am5.color(0xDC67AB),    // Lilás suave (algodão doce)
        Sul: am5.color(0x6794DC) 
    };

    // Carrega o mapa do Brasil
    let polygonSeries = chart.series.push(
        am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_brazilLow
        })
    );

    // Configurações padrão de aparência
    polygonSeries.mapPolygons.template.setAll({
        tooltipText: "{name}",
        interactive: true,
        fillOpacity: 1, // Opacidade padrão
        stroke: am5.color(0xffffff),
        strokeWidth: 0.5
    });

    // Adapta as cores de acordo com a região
    polygonSeries.mapPolygons.template.adapters.add("fill", function(fill, target) {
        let stateCode = target.dataItem.dataContext.id;
        for (const [region, states] of Object.entries(regions)) {
            if (states.includes(stateCode)) {
                return regionColors[region]; // Aplica a cor da região
            }
        }
        return fill; // Cor padrão
    });

    // Define o estado de hover (alterando o `fillOpacity`)
    polygonSeries.mapPolygons.template.states.create("hover", {
        fillOpacity: 0.6 // Reduz a opacidade ao passar o mouse
    });

    // Adiciona evento ao clicar em um estado
    polygonSeries.mapPolygons.template.events.on("click", function(ev) {
        alert("Você clicou em: " + ev.target.dataItem.dataContext.name);
    });

    chart.appear(1000, 100);
});
