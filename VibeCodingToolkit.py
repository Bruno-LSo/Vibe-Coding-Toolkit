import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def remover_imagem_por_tamanho(texto):
    """
    Substitui ocorrências do padrão:
        "image/png": "<base64_content>"
    por "Removed due to size".
    
    Além disso, se encontrar exatamente algum dos seguintes trechos:
    
     "metadata": {
      "ExecuteTimeLog": [
    
     "metadata": {
      "colab": {
       "provenance": []
      },
      "kernelspec": [
    
     "metadata": {
      "kernelspec": {
    
    Remove tudo, a partir do trecho encontrado (inclusive ele) até o final do documento.

    Futuramente irei adicionar mais trechos para remover, conforme os identificar.
    """
    padrao = r'("image/png":\s*")[^"]+(")'
    texto = re.sub(padrao, r'\1Removed due to size\2', texto)
    
    markers = [
        '"metadata": {\n  "ExecuteTimeLog": [',
        '"metadata": {\n  "colab": {\n   "provenance": []\n  },\n  "kernelspec": [',
        '"metadata": {\n  "kernelspec": {'
    ]
    indices = []
    for marker in markers:
        idx = texto.find(marker)
        if idx != -1:
            indices.append(idx)
    if indices:
        pos = min(indices)
        texto = texto[:pos]
    return texto

def emitir_alerta_de_progresso(atual, total, marco_anterior, marcos=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
    progresso = int((atual / total) * 100)
    if progresso >= marcos[marco_anterior + 1]:
        print(f"Progresso atingiu {marcos[marco_anterior + 1]}%.")
        return marco_anterior + 1
    return marco_anterior

# Funções auxiliares para geração da árvore aprimorada no .bash
def is_ignored(path, ignore_list):
    path_abs = os.path.abspath(path)
    for ignorada in ignore_list:
        if os.path.commonpath([path_abs, ignorada]) == ignorada:
            return True
    return False

def gerar_subarvore(path, prefix, ignore_list):
    lines = []
    try:
        children = os.listdir(path)
    except Exception:
        children = []
    # Filtra itens ignorados
    children = [child for child in children if not is_ignored(os.path.join(path, child), ignore_list)]
    children.sort(key=lambda s: s.lower())
    # Separa diretórios e arquivos (diretórios primeiro)
    dirs = [child for child in children if os.path.isdir(os.path.join(path, child))]
    files = [child for child in children if not os.path.isdir(os.path.join(path, child))]
    children = dirs + files
    for i, child in enumerate(children):
        child_path = os.path.join(path, child)
        if i == len(children) - 1:
            connector = "┗ "
            new_prefix = prefix + "   "
        else:
            connector = "┣ "
            new_prefix = prefix + "┃ "
        line = prefix + connector + child + ("/" if os.path.isdir(child_path) else "")
        lines.append(line)
        if os.path.isdir(child_path):
            lines.extend(gerar_subarvore(child_path, new_prefix, ignore_list))
    return lines

def gerar_arvore(path, ignore_list):
    basename = os.path.basename(os.path.normpath(path))
    root_line = basename + "/"
    lines = [root_line]
    # Para a raiz, usamos um prefixo simples (um espaço) para os filhos, conforme o exemplo do file-tree-generator
    lines.extend(gerar_subarvore(path, " ", ignore_list))
    return lines

def gerar_arquitetura_e_conteudo(caminho_inicial, arquivo_bash, arquivo_txt, pastas_ignoradas):
    """
    Gera os arquivos de saída (.bash e .txt) a partir do diretório inicial,
    ignorando os caminhos (pastas ou arquivos) informados em pastas_ignoradas.
    Para garantir a comparação correta, todos os caminhos são convertidos para absolutos.
    """
    separador = '/' * 100
    total_diretorios = 0
    total_arquivos = 0
    marco_atual = 0

    caminho_inicial = os.path.abspath(caminho_inicial)
    # Converte os caminhos ignorados para absolutos
    pastas_ignoradas = [os.path.abspath(p) for p in pastas_ignoradas]

    # Geração do arquivo .bash com a árvore aprimorada
    with open(arquivo_bash, 'w', encoding='utf-8') as bash_file:
        tree_lines = gerar_arvore(caminho_inicial, pastas_ignoradas)
        for line in tree_lines:
            bash_file.write(line + "\n")
    
    # Geração do arquivo .txt com os caminhos e conteúdos dos arquivos
    with open(arquivo_txt, 'w', encoding='utf-8') as txt_file:
        for raiz, diretorios, arquivos in os.walk(caminho_inicial):
            raiz_abs = os.path.abspath(raiz)
            if any(os.path.commonpath([raiz_abs, ignorada]) == ignorada for ignorada in pastas_ignoradas):
                continue
            total_diretorios += 1
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                caminho_completo_abs = os.path.abspath(caminho_completo)
                if any(os.path.commonpath([caminho_completo_abs, ignorada]) == ignorada for ignorada in pastas_ignoradas):
                    continue
                total_arquivos += 1
                txt_file.write(f"{caminho_completo_abs}\n\n")
                try:
                    with open(caminho_completo_abs, 'r', encoding='utf-8') as file:
                        conteudo = file.read()
                        txt_file.write(conteudo)
                except Exception as e:
                    txt_file.write(f"Erro ao ler o arquivo: {e}\n")
                txt_file.write(f"\n{separador}\n\n")
                marco_atual = emitir_alerta_de_progresso(total_arquivos, total_arquivos + total_diretorios, marco_atual)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Processamento de Arquivos e Diretórios")
        self.geometry("900x600")
        self.selected_path = None
        self.is_directory = False  # Será True se o usuário escolher um diretório
        self.item_paths = {}       # Mapeia o ID do item na árvore para seu caminho completo
        self.ignore_state = {}     # Mapeia o ID do item para o estado de ignorar (True/False)
        self.create_widgets()

    def create_widgets(self):
        # Frame de seleção de caminho
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        lbl = tk.Label(top_frame, text="Selecione um caminho:")
        lbl.pack(side=tk.LEFT)

        btn_dir = tk.Button(top_frame, text="Selecionar Diretório", command=self.select_directory)
        btn_dir.pack(side=tk.LEFT, padx=5)

        btn_file = tk.Button(top_frame, text="Selecionar Arquivo", command=self.select_file)
        btn_file.pack(side=tk.LEFT, padx=5)

        self.lbl_selected = tk.Label(top_frame, text="Nenhum caminho selecionado", fg="blue")
        self.lbl_selected.pack(side=tk.LEFT, padx=10)

        # Frame para a árvore (visível apenas se for diretório)
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Ignorar",), show="tree headings")
        self.tree.heading("#0", text="Nome")
        self.tree.heading("Ignorar", text="Ignorar")
        self.tree.column("Ignorar", width=150, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Usa clique simples na coluna "Ignorar"
        self.tree.bind("<Button-1>", self.on_tree_click)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão para executar a aplicação
        btn_exec = tk.Button(self, text="Executar Aplicação", command=self.run_application, bg="green", fg="white")
        btn_exec.pack(pady=10)

    def select_directory(self):
        path = filedialog.askdirectory(title="Selecione um Diretório")
        if path:
            self.selected_path = path
            self.is_directory = True
            self.lbl_selected.config(text=f"Diretório selecionado: {path}")
            self.populate_tree()
        else:
            messagebox.showwarning("Atenção", "Nenhum diretório foi selecionado.")

    def select_file(self):
        path = filedialog.askopenfilename(title="Selecione um Arquivo")
        if path:
            self.selected_path = path
            self.is_directory = False
            self.lbl_selected.config(text=f"Arquivo selecionado: {path}")
            # Se for arquivo, limpa a árvore (caso haja dados anteriores)
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.item_paths.clear()
            self.ignore_state.clear()
        else:
            messagebox.showwarning("Atenção", "Nenhum arquivo foi selecionado.")

    def populate_tree(self):
        # Limpa a árvore e os dicionários
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_paths.clear()
        self.ignore_state.clear()
        # Insere a raiz
        root_node = self.tree.insert("", "end", text=os.path.basename(self.selected_path), values=("☐",))
        self.item_paths[root_node] = self.selected_path
        self.ignore_state[root_node] = False
        self.insert_nodes(root_node, self.selected_path)

    def insert_nodes(self, parent, path):
        try:
            items = os.listdir(path)
        except Exception as e:
            return
        items.sort(key=lambda s: s.lower())
        for item in items:
            abspath = os.path.join(path, item)
            node = self.tree.insert(parent, "end", text=item, values=("☐",))
            self.item_paths[node] = abspath
            self.ignore_state[node] = False
            if os.path.isdir(abspath):
                self.insert_nodes(node, abspath)

    def on_tree_click(self, event):
        # Identifica a região e a coluna clicada
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            # A coluna "Ignorar" é a primeira coluna extra (ID "#1")
            if col == "#1":
                item = self.tree.identify_row(event.y)
                if item:
                    current = self.ignore_state.get(item, False)
                    self.ignore_state[item] = not current
                    new_text = "☑" if not current else "☐"
                    self.tree.set(item, "Ignorar", new_text)

    def run_application(self):
        if not self.selected_path:
            messagebox.showerror("Erro", "Nenhum caminho selecionado!")
            return

        if self.is_directory:
            # Monta a lista de itens ignorados a partir da árvore
            ignorados = []
            for item, state in self.ignore_state.items():
                if state:
                    ignorados.append(self.item_paths[item])
            nome_diretorio = os.path.basename(os.path.normpath(self.selected_path))
            arquivo_bash = f"{nome_diretorio}Arquitetura.bash"
            arquivo_txt = f"{nome_diretorio}Conteudo.txt"
            try:
                gerar_arquitetura_e_conteudo(self.selected_path, arquivo_bash, arquivo_txt, ignorados)
                messagebox.showinfo("Sucesso", f"Arquivos gerados com sucesso:\n{arquivo_bash}\n{arquivo_txt}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro durante o processamento: {e}")
        else:
            nome_arquivo = os.path.splitext(os.path.basename(self.selected_path))[0]
            arquivo_txt = f"{nome_arquivo}Conteudo.txt"
            try:
                with open(self.selected_path, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                with open(arquivo_txt, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(conteudo)
                messagebox.showinfo("Sucesso", f"Arquivo gerado com sucesso:\n{arquivo_txt}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")

        # Após a geração dos arquivos, pergunta se deseja remover o código para imagem
        if messagebox.askyesno("Remover Código de Imagem", "Deseja apagar o código para imagem no arquivo gerado?"):
            try:
                with open(arquivo_txt, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                novo_conteudo = remover_imagem_por_tamanho(conteudo)
                with open(arquivo_txt, 'w', encoding='utf-8') as file:
                    file.write(novo_conteudo)
                messagebox.showinfo("Sucesso", f"Código para imagem removido com sucesso no arquivo {arquivo_txt}.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover o código para imagem no arquivo {arquivo_txt}: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
