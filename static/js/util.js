// +-------------------------------------------------------------+
// | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
// | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
// | Data inicio: 01/07/2024                                     |
// | Data finalização: xx/xx/xx                                  |
// | Autor: Alexandre Silva dos Santos                           |
// | Email: alexandresantoscompunb@gmail.com                     |
// | Módulo: Rotinas gerais do projeto                           |
// +-------------------------------------------------------------+----------------------------------------------------------

function funcao_btn_delete(nome,id){
    document.getElementById("id_nome_simulacao").textContent = nome;
    document.getElementById("id_btn_modal_delete_confirm").id_delete = id;
};


function funcao_btn_confirm(id_simulacao){
    console.log('Simulação confirmada '+ id_simulacao)
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

};

