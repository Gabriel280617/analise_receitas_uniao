import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#Load the dataset
df = pd.read_csv('Receita-Orcamentaria-da-Uniao.csv', encoding='latin1', sep=';')

#Select 12 relevant columns
colunas = [
    'ANO DE REFERENCIA', 'RECEITAS CORRENTES', 'RECEITA TRIBUTARIA',
    'RECEITA DE CONTRIBUICOES', 'RECEITA PATRIMONIAL', 'RECEITA AGROPECUARIA',
    'RECEITA INDUSTRIAL', 'RECEITA DE SERVICOS', 'TRANSFERENCIA CORRENTES',
    'OUTRAS RECEITAS CORRENTES', 'RECEITAS DE CAPITAL', 'OPERACOES DE CREDITO'
]

df = df[colunas]

#Cleaning

for col in df.columns[1:]:  # Ignore 'ANO DE REFERENCIA'
    df[col] = df[col].replace('[.,]', '', regex=True).astype(float, errors='ignore') / 100
df.fillna(0, inplace=True)  # Replace blanks with 0

# Função para formatar valores em reais (ex.: R$ 1,23T)
def formatar_valor(valor):
    if valor >= 1e12:  # Trilhões
        return f'R$ {valor / 1e12:,.2f}T'
    elif valor >= 1e9:  # Bilhões
        return f'R$ {valor / 1e9:,.2f}B'
    elif valor >= 1e6:  # Milhões
        return f'R$ {valor / 1e6:,.2f}M'
    else:
        return f'R$ {valor:,.2f}'


# Função para criar o gráfico
def plot_receitas(ano):
    df_filtered = df[df['ANO DE REFERENCIA'] == int(ano)]
    categorias = [
        'RECEITA TRIBUTARIA', 'RECEITA DE CONTRIBUICOES', 'RECEITA PATRIMONIAL',
        'RECEITA AGROPECUARIA', 'RECEITA INDUSTRIAL', 'RECEITA DE SERVICOS',
        'TRANSFERENCIA CORRENTES', 'OUTRAS RECEITAS CORRENTES', 'RECEITAS DE CAPITAL',
        'OPERACOES DE CREDITO'
    ]
    valores = [df_filtered[cat].iloc[0] / 1e9 for cat in categorias]  # Converter para bilhões para o gráfico

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(categorias, valores, color='#1f77b4')
    ax.set_title(f'Receitas da União - {ano}')
    ax.set_xlabel('Categoria de Receita')
    ax.set_ylabel('Valor (R$ Bilhões)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig


# Interface gráfica com Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Análise de Receitas da União')

        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Dropdown para ano
        ttk.Label(frame, text="Selecione o Ano:").grid(row=0, column=0, sticky=tk.W)
        self.ano_var = tk.StringVar()
        anos = sorted(df['ANO DE REFERENCIA'].unique().astype(str))
        self.ano_dropdown = ttk.Combobox(frame, textvariable=self.ano_var, values=anos, state='readonly')
        self.ano_dropdown.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.ano_dropdown.set(anos[0])

        # Botão para gerar gráfico
        ttk.Button(frame, text="Gerar Gráfico", command=self.atualizar_grafico).grid(row=1, column=0, columnspan=2,
                                                                                     pady=10)

        # Área para estatísticas
        self.stats_label = ttk.Label(frame, text="")
        self.stats_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Área para o gráfico
        self.canvas = None

    def atualizar_grafico(self):
        ano = self.ano_var.get()

        # Atualizar estatísticas
        df_filtered = df[df['ANO DE REFERENCIA'] == int(ano)]
        total_receitas = df_filtered['RECEITAS CORRENTES'].iloc[0] + df_filtered['RECEITAS DE CAPITAL'].iloc[0]
        self.stats_label.config(text=f"Total de Receitas: {formatar_valor(total_receitas)}")

        # Limpar gráfico anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Criar novo gráfico
        fig = plot_receitas(ano)
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)


# Iniciar a aplicação
root = tk.Tk()
app = App(root)
root.mainloop()
