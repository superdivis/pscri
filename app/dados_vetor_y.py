import json

# Gera a lista com 340 itens
dados = [{"id": i, "valor": 0} for i in range(1, 341)]

# Cria o dicionário final
estrutura = {"dados": dados}

# Converte para JSON formatado
json_formatado = json.dumps(estrutura, indent=4)

print (json_formatado)

# Salva em um arquivo (opcional)
with open("dados_340.json", "w") as f:
    f.write(json_formatado)

# Exibe o início do JSON
print(json_formatado[:1000])  # só os primeiros 1000 caracteres para não lotar o terminal