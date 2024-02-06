import pandas as pd

# Lista para armazenar os DataFrames
df_list = []

# Iterar sobre os números de 7 a 46
for i in range(1, 24):

    # Abrir o arquivo CSV correspondente
    file_name = f"dataFrame{i}.csv"
    df = pd.read_csv(file_name)

    # Adicionar o DataFrame à lista
    df_list.append(df)

# Combinar os DataFrames da lista
df = pd.concat(df_list, ignore_index=True)

# Salvar o DataFrame como um arquivo CSV
df.to_csv("arquivo_combinado_Netflix.csv")

# Ler o arquivo CSV
df = pd.read_csv("arquivo_combinado_Netflix.csv")

# Converte o DataFrame em um objeto JSON
json_data = df.to_json()

# Salva o objeto JSON em um arquivo
with open("arquivo_combinado_Netflix.json", "w") as f:
    f.write(json_data)