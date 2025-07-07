# off.journal ✨

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Language: Python](https://img.shields.io/badge/Language-Python-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![GUI: GTK3 + WebKit](https://img.shields.io/badge/GUI-GTK3%20%2B%20WebKit-729fcf.svg?style=flat&logo=gtk)](https://www.gtk.org/)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-FCC624.svg?style=flat&logo=linux)](https://www.kernel.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Um diário e planejador 100% offline, seguro e privado, com interfaces para o terminal (CLI) e gráfica (GUI).

> 📸 Screenshot da interface gráfica em breve...

**off.journal** foi criado para quem valoriza a privacidade e o controle sobre seus próprios dados. Tudo fica no seu computador, em formatos abertos e acessíveis.

---

## 🎯 Funcionalidades

-   **Interface Dupla**: Escolha como interagir.
    -   **GUI (Gráfica)**: Uma experiência visual moderna e intuitiva.
    -   **CLI (Linha de Comando)**: Perfeita para automação, scripts e para quem ama o terminal.
-   **Privacidade Total**: Seus dados nunca saem da sua máquina. Não há servidores, contas ou nuvem.
-   **Formatos Abertos**: As entradas do diário são salvas em **Markdown** (`.md`) e os eventos do planejador em **JSON**, permitindo que você acesse seus dados com qualquer editor de texto.
-   **Arquitetura Modular**: O coração do sistema (`core`) é separado das interfaces, facilitando a manutenção e a criação de novas funcionalidades ou até mesmo outras interfaces.

---

## 🚀 Guia Rápido de Instalação e Uso

### 1. Pré-requisitos
-   Python 3.8+
-   `git` (para clonar o projeto)

### 2. Instalação
Navegue até o diretório onde deseja instalar o projeto e execute:
```bash
git clone https://github.com/seu-usuario/offjournal.git
cd offjournal
```

### 3. Executando a Interface Gráfica (GUI)
Esta é a forma recomendada de uso.

**a) Instale as dependências do sistema:**

> A GUI depende de bibliotecas que são instaladas via gerenciador de pacotes do seu Linux, não com `pip`.

-   **Debian / Ubuntu / Mint:**
    ```bash
    sudo apt update && sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
    ```
-   **Arch Linux / Manjaro:**
    ```bash
    sudo pacman -Syu python-gobject webkit2gtk
    ```
-   **Fedora / CentOS:**
    ```bash
    sudo dnf install python3-gobject webkit2gtk4.0
    ```

**b) Inicie a aplicação:**
```bash
python3 main.py gui
```

<br>

<details>
<summary>
    <strong>👉 Clique aqui para ver como usar a Interface de Linha de Comando (CLI)</strong>
</summary>

### 4. Usando via Linha de Comando (CLI)

Todos os comandos são executados a partir do arquivo `main.py`.

#### Comandos do Diário

-   **Listar todas as entradas:**
    ```bash
    python3 main.py listar
    ```
-   **Criar uma nova entrada:**
    ```bash
    python3 main.py nova "Um título incrível para minha entrada"
    ```
-   **Ler o conteúdo de uma entrada:**
    > Use o ID numérico que aparece no comando `listar`.
    ```bash
    python3 main.py ler 20250716103000
    ```
-   **Apagar uma entrada (cuidado, é permanente!):**
    ```bash
    python3 main.py apagar 20250716103000
    ```

#### Comandos do Planejador

-   **Listar todos os eventos:**
    ```bash
    python3 main.py planner listar
    ```
-   **Adicionar um novo evento:**
    > O formato da data deve ser `AAAA-MM-DD`.
    ```bash
    python3 main.py planner add 2025-12-25 "Ceia de Natal"
    ```
-   **Remover um evento pelo ID:**
    ```bash
    python3 main.py planner del 1
    ```

</details>

---

## 📁 Onde os Dados Ficam Armazenados?

Para total transparência, o `off.journal` salva tudo em uma pasta oculta no seu diretório de usuário:

-   **Localização**: `~/.offjournal/`
-   **Entradas do Diário**: `~/.offjournal/entries/`
-   **Eventos do Planejador**: `~/.offjournal/planner.json`

Você pode fazer backup desta pasta para garantir a segurança dos seus dados.

<br>

<details>
<summary>
    <strong>🛠️ Para Desenvolvedores: Arquitetura e Testes</strong>
</summary>

### Arquitetura do Projeto

O `off.journal` foi projetado com uma clara separação de responsabilidades:

1.  **`core/`**: O motor do projeto. Contém toda a lógica de negócio (manipulação de entradas, eventos, etc.). **Nenhum código no `core` interage com o usuário**; ele apenas processa dados e retorna resultados estruturados (dicionários, listas).
2.  **Interfaces**:
    -   `main.py`: A interface de linha de comando (CLI).
    -   `offjournal_gui/`: A interface gráfica (GUI).

    Ambas as interfaces são "clientes" do `core`. Elas enviam requisições, recebem os dados e os formatam para exibição.

### Executando os Testes

Usamos a biblioteca `unittest` nativa do Python. Para rodar todos os testes e garantir que tudo está funcionando, execute:
```bash
python3 -m unittest discover tests
```
</details>

---

## 📄 Licença
Este projeto é distribuído sob a **Licença GPLv3**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
