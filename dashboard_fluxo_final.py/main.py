import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, DoubleVar, END, messagebox

# --- Dados iniciais ---
df = pd.DataFrame(columns=['Mês','Tipo','Descrição','Valor'])

# --- Funções ---
def adicionar_transacao():
    try:
        mes_val = int(mes.get())
        if mes_val < 1 or mes_val > 12:
            messagebox.showerror("Erro", "Mês inválido")
            return
        tipo_val = tipo.get().lower()
        if tipo_val not in ['receita','despesa']:
            messagebox.showerror("Erro", "Tipo inválido")
            return
        desc_val = descricao.get()
        valor_val = float(valor.get())
        global df
        df = pd.concat([df, pd.DataFrame([{'Mês': mes_val, 'Tipo': tipo_val, 'Descrição': desc_val, 'Valor': valor_val}])], ignore_index=True)
        mes_entry.delete(0, END)
        descricao_entry.delete(0, END)
        valor_entry.delete(0, END)
        atualizar_label()
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido")

def atualizar_label():
    fluxo = fluxo_mensal(df)
    label_fluxo.config(text=str(fluxo))

def fluxo_mensal(df_local):
    receitas = df_local[df_local['Tipo']=='receita'].groupby('Mês')['Valor'].sum()
    despesas = df_local[df_local['Tipo']=='despesa'].groupby('Mês')['Valor'].sum()
    meses = pd.Series(range(1,13), name='Mês')
    fluxo = pd.DataFrame({'Mês': meses})
    fluxo = fluxo.merge(receitas.rename('Receitas'), on='Mês', how='left')
    fluxo = fluxo.merge(despesas.rename('Despesas'), on='Mês', how='left')
    fluxo.fillna(0, inplace=True)
    fluxo['Saldo'] = fluxo['Receitas'] - fluxo['Despesas']
    fluxo['Saldo Acumulado'] = fluxo['Saldo'].cumsum()
    return fluxo

def plotar_grafico():
    fluxo = fluxo_mensal(df)
    plt.figure(figsize=(10,6))
    plt.bar(fluxo['Mês']-0.2, fluxo['Receitas'], width=0.4, label='Receitas', color='green')
    plt.bar(fluxo['Mês']+0.2, fluxo['Despesas'], width=0.4, label='Despesas', color='red')
    plt.plot(fluxo['Mês'], fluxo['Saldo Acumulado'], label='Saldo Acumulado', color='blue', marker='o')
    plt.xlabel('Mês')
    plt.ylabel('R$')
    plt.title('Fluxo de Caixa Mensal')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

# --- Interface Tkinter ---
root = Tk()
root.title("Simulador Fluxo de Caixa")

Label(root, text="Mês (1-12)").grid(row=0,column=0)
mes = IntVar()
mes_entry = Entry(root, textvariable=mes)
mes_entry.grid(row=0,column=1)

Label(root, text="Tipo (receita/despesa)").grid(row=1,column=0)
tipo = StringVar()
tipo_entry = Entry(root, textvariable=tipo)
tipo_entry.grid(row=1,column=1)

Label(root, text="Descrição").grid(row=2,column=0)
descricao = StringVar()
descricao_entry = Entry(root, textvariable=descricao)
descricao_entry.grid(row=2,column=1)

Label(root, text="Valor (R$)").grid(row=3,column=0)
valor = DoubleVar()
valor_entry = Entry(root, textvariable=valor)
valor_entry.grid(row=3,column=1)

Button(root, text="Adicionar Transação", command=adicionar_transacao).grid(row=4,column=0,columnspan=2)
Button(root, text="Gerar Gráfico", command=plotar_grafico).grid(row=5,column=0,columnspan=2)

label_fluxo = Label(root, text="")
label_fluxo.grid(row=6,column=0,columnspan=2)

root.mainloop()
