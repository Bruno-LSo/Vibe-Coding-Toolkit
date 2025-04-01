![Vibe Coding Toolkit](image/VibeCodingToolkit.png)

# Vibe Coding Toolkit

Desenvolver aplicações com muitos arquivos e componentes é desafiador. Mesmo modelos de IA avançados, como o Claude 3.7 Sonnet, ainda enfrentam limitações para compreender projetos grandes de forma completa, o que dificulta interações realmente eficazes com a IA.

Desenvolvi esta aplicação em Python com o objetivo de tornar possível o que esses modelos ainda não conseguem fazer sozinhos: entender o contexto de toda uma aplicação.

A ferramenta gera dois arquivos a partir de um diretório do seu projeto:

- Um `.bash` com a estrutura completa de diretórios e arquivos (a arquitetura da aplicação);
- Um `.txt` com o conteúdo de todos os arquivos, limpo e organizado.

Esses documentos podem ser colados diretamente em chats com IA para fornecer uma visão completa da aplicação, permitindo interações mais precisas: como criação de novas funcionalidades, correção de bugs ou sugestões de melhorias com base em todo o contexto.

A interface gráfica é simples, com opção de ignorar arquivos ou pastas específicas. Também é possível usá-la para extrair o conteúdo de arquivos individuais.

Importante: a aplicação **não modifica nenhum arquivo existente**, apenas gera dois novos arquivos no diretório local.

O objetivo é claro: empoderar qualquer pessoa — experiente ou iniciante — a usar a inteligência artificial para criar, entender e evoluir aplicações com mais facilidade.

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Como Interagir com a Aplicação](#como-interagir-com-a-aplicação)
- [Contribuição Social](#contribuição-social)
- [Explore Mais](#explore-mais)

---

## Funcionalidades

- Seleção de diretório ou arquivo específico.
- Geração de dois arquivos:
  - `NOMEDIRETORIOArquitetura.bash`: representa a árvore de diretórios e arquivos.
  - `NOMEDIRETORIOConteudo.txt`: contém o conteúdo de todos os arquivos, separados por delimitadores.
- Interface gráfica com seleção interativa de pastas/arquivos a serem ignorados.
- Filtro opcional de conteúdos como imagens base64 e metadados irrelevantes (exclusivo para projetos de Ciência de dados).
- Extração isolada do conteúdo de qualquer arquivo individual.
- Progresso exibido no console durante a geração.

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **Tkinter** – Interface gráfica nativa.
- **OS / RE** – Manipulação de diretórios, leitura e regex para filtragem de conteúdo.

---

## Como Executar o Projeto

### 1. Pré-requisitos

- Ter o **Python 3.10 ou superior** instalado.
- Utilizar um editor de código como o **VSCode** (Visual Studio Code).

### 2. Clonar o Repositório

```bash
git clone https://github.com/Bruno-LSo/Vibe-Coding-Toolkit.git
```

### 3. Executar no VSCode

- Abra o diretório no VSCode.
- Certifique-se de que o ambiente virtual (se necessário) está ativado.
- No terminal integrado, execute:

```bash
python VibeCodingToolkit.py
```

> `VibeCodingToolkit` é o arquivo principal que contém o código da aplicação. 
---

## Como Interagir com a Aplicação

1. Ao executar, será exibida uma **interface gráfica**.
2. Selecione:
   - Um **diretório**, para gerar os dois arquivos (`.bash` e `.txt`), com opção de ignorar itens via checkbox.
   - Ou um **arquivo específico**, para gerar apenas seu conteúdo em um `.txt`.
3. Clique em **Executar Aplicação**.
4. Após o processamento, o sistema perguntará se deseja **remover códigos de imagem base64** automaticamente (específico para projetos de ciência de dados, pois remove - do arquivo txt gerado - parte do arquivo que é indiferente para a compreensão do projeto por parte da IA, portanto **Se não for um projeto de ciência de dados, selecione a opção "Não").
5. Os arquivos gerados serão salvos no mesmo diretório do script.

---

## Contribuição Social

Este projeto é parte de uma iniciativa maior que busca **democratizar o desenvolvimento de aplicações**. Ele permite que pessoas com ideias inovadoras, mas sem conhecimento técnico, usem IA para materializar suas soluções com clareza e agilidade.

---

## Explore Mais

Se você gostou deste projeto, confira também outros projetos disponíveis no meu GitHub e me acompanhe pelo LinkedIn:

- [GitHub](https://github.com/Bruno-LSo)
- [LinkedIn](https://www.linkedin.com/in/bruno-lima-ds)
- **Email**: bruno_ls@uol.com.br

---
Obrigado pela atenção!
