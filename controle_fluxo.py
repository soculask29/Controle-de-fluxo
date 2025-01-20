"""
Controle de Fluxo
Desenvolvido por: Pedro Costa da Silva
Data: Janeiro de 2025
Contato: https://wa.me/5511948497614
Copyright © 2025 Pedro Costa da Silva. Todos os direitos reservados.
"""



import tkinter as tk
from tkinter import ttk, messagebox

# Funções
def adicionar_registro():
    nome = entrada_nome.get().strip()
    preco = entrada_preco.get().strip()
    tipo = tipo_operacao.get()

    if not nome or not preco:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "O preço deve ser um número válido!")
        return

    # Adiciona o registro na tabela com formatação
    valor_formatado = f"R$ {preco:,.2f}".replace(",", ".")
    linha_id = tabela.insert("", tk.END, values=(nome, valor_formatado, tipo))

    # Aplica cor com base no tipo
    if tipo == "Entrada":
        tabela.item(linha_id, tags=("entrada",))
    elif tipo == "Saída":
        tabela.item(linha_id, tags=("saida",))

    # Atualiza totais
    atualizar_totais(tipo, preco)

    # Limpa os campos
    entrada_nome.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)

def atualizar_totais(tipo, preco):
    global total_entrada, total_saida
    if tipo == "Entrada":
        total_entrada += preco
    elif tipo == "Saída":
        total_saida += preco

    saldo_atual = total_entrada - total_saida
    label_total_entrada.config(text=f"Total Entradas: R$ {total_entrada:,.2f}".replace(",", "."))
    label_total_saida.config(text=f"Total Saídas: R$ {total_saida:,.2f}".replace(",", "."))
    label_saldo_atual.config(text=f"Saldo Atual: R$ {saldo_atual:,.2f}".replace(",", "."))

def remover_registro():
    try:
        item_selecionado = tabela.selection()[0]
        valores = tabela.item(item_selecionado, "values")
        preco = float(valores[1].replace("R$", "").replace(".", "").replace(",", "."))
        tipo = valores[2]

        # Atualiza totais
        if tipo == "Entrada":
            global total_entrada
            total_entrada -= preco
        elif tipo == "Saída":
            global total_saida
            total_saida -= preco

        tabela.delete(item_selecionado)
        atualizar_totais("Remover", 0)
    except IndexError:
        messagebox.showwarning("Aviso", "Nenhum registro selecionado!")

def limpar_tabela():
    if messagebox.askyesno("Confirmação", "Deseja limpar todos os registros?"):
        tabela.delete(*tabela.get_children())
        global total_entrada, total_saida
        total_entrada, total_saida = 0, 0
        atualizar_totais("Limpar", 0)

# Configuração inicial
janela = tk.Tk()
janela.title("Controle de Fluxo")
janela.geometry("650x550")
janela.config(bg="#f4f4f4")

total_entrada = 0
total_saida = 0

# Título
titulo = tk.Label(janela, text="Controle de Fluxo - Entradas e Saídas", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#333")
titulo.pack(pady=10)

# Frame para entradas
frame_entrada = tk.Frame(janela, bg="#f4f4f4")
frame_entrada.pack(pady=10)

# Campos de entrada
tk.Label(frame_entrada, text="Nome:", font=("Arial", 12), bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5)
entrada_nome = tk.Entry(frame_entrada, font=("Arial", 12), width=20)
entrada_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Preço:", font=("Arial", 12), bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=5)
entrada_preco = tk.Entry(frame_entrada, font=("Arial", 12), width=20)
entrada_preco.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Tipo:", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0, padx=5, pady=5)
tipo_operacao = ttk.Combobox(frame_entrada, values=["Entrada", "Saída"], font=("Arial", 12), state="readonly")
tipo_operacao.grid(row=2, column=1, padx=5, pady=5)
tipo_operacao.current(0)

# Botão adicionar
btn_adicionar = tk.Button(frame_entrada, text="Adicionar", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=adicionar_registro)
btn_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

# Tabela
frame_tabela = tk.Frame(janela, bg="#f4f4f4")
frame_tabela.pack(pady=10)

tabela = ttk.Treeview(frame_tabela, columns=("Nome", "Preço", "Tipo"), show="headings", height=10)
tabela.heading("Nome", text="Nome")
tabela.heading("Preço", text="Preço")
tabela.heading("Tipo", text="Tipo")
tabela.column("Nome", width=200)
tabela.column("Preço", width=100, anchor=tk.CENTER)
tabela.column("Tipo", width=100, anchor=tk.CENTER)
tabela.pack(side=tk.LEFT)

# Tags para cores
tabela.tag_configure("entrada", background="#d4f8e8")  # Verde claro
tabela.tag_configure("saida", background="#f8d4d4")    # Vermelho claro

scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tabela.config(yscrollcommand=scrollbar.set)

# Totais
frame_totais = tk.Frame(janela, bg="#f4f4f4")
frame_totais.pack(pady=10)

label_total_entrada = tk.Label(frame_totais, text="Total Entradas: R$ 0.00", font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#4CAF50")
label_total_entrada.grid(row=0, column=0, padx=20)

label_total_saida = tk.Label(frame_totais, text="Total Saídas: R$ 0.00", font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#f44336")
label_total_saida.grid(row=0, column=1, padx=20)

label_saldo_atual = tk.Label(janela, text="Saldo Atual: R$ 0.00", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
label_saldo_atual.pack(pady=10)

# Botões de controle
frame_botoes = tk.Frame(janela, bg="#f4f4f4")
frame_botoes.pack(pady=20)

btn_remover = tk.Button(frame_botoes, text="Remover Selecionado", bg="#f44336", fg="white", font=("Arial", 12, "bold"), command=remover_registro)
btn_remover.grid(row=0, column=0, padx=10)

btn_limpar = tk.Button(frame_botoes, text="Limpar Tudo", bg="#FFC107", fg="white", font=("Arial", 12, "bold"), command=limpar_tabela)
btn_limpar.grid(row=0, column=1, padx=10)

 # Rodapé
def abrir_link():
    import webbrowser
    webbrowser.open("https://wa.me/5511948497614")

rodape_frame = tk.Frame(janela, bg="#f4f4f4")
rodape_frame.pack(side=tk.BOTTOM, pady=10)

rodape_texto = tk.Label(rodape_frame, text="Feito por: Pedro Costa da Silva", font=("Arial", 10), bg="#f4f4f4", fg="#666")
rodape_texto.pack(side=tk.LEFT, padx=5)

rodape_link = tk.Label(rodape_frame, text="(WhatsApp)", font=("Arial", 10, "underline"), bg="#f4f4f4", fg="#0000EE", cursor="hand2")
rodape_link.pack(side=tk.LEFT)
rodape_link.bind("<Button-1>", lambda e: abrir_link())


# Loop da interface
janela.mainloop()
