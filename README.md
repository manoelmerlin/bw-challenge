
# Desafio BW

Este projeto é uma solução para o Desafio BW, utilizando o Python na versão 3.9 com o ambiente Conda para gerenciamento de dependências e ambientes.

## Pré-requisitos
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) instalado na máquina
- Python 3.9 (caso o ambiente Conda ainda não esteja configurado)

## Configuração do Ambiente

1. **Criar o ambiente Conda**: Se você ainda não possui um ambiente com Python 3.9, execute o comando abaixo:
   ```bash
   conda create -y -n bwenv python=3.9
   ```

2. **Ativar o ambiente Conda**:
   ```bash
   conda activate bwenv
   ```

## Executando os Scripts

Para rodar os scripts, basta utilizar os seguintes comandos. Cada script inclui testes de acordo com os exemplos fornecidos no arquivo do desafio:

- **Reconciliar Contas**: 
  ```bash
  python reconcile_accounts.py
  ```

- **Últimas Linhas do Arquivo**:
  ```bash
  python last_lines.py
  ```

- **Propriedade Computada**:
  ```bash
  python bw_computed_property.py
  ```

---

## Scripts e Funcionalidades

### `reconcile_accounts.py`
Script que realiza a reconciliação de contas, ajustando valores conforme o desafio proposto.

### `last_lines.py`
Script que lê as linhas de um arquivo em ordem inversa, similar ao comando `tac` em Unix.

### `bw_computed_property.py`
Implementa um decorator que simula uma propriedade computada com cache, recomputando o valor apenas quando as dependências são alteradas.

---

## Observações
Este projeto foi desenvolvido para ser executado no ambiente Conda com Python 3.9. Certifique-se de que o ambiente está ativado antes de rodar os scripts. 
