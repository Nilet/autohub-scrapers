# Escola TI scrapers

### Setup


1. ```shell
    git clone http://escoladeti.unicesumar.edu.br:8083/escoladeti2023/003timeescoladeti2023/scrapers
    ```
2. ```shell
    cd autohub-scrapers
    ```
3. ```shell
    python -m venv .venv
   ```

4. ```shell
    source .venv/bin/activate
    ```
5. ```shell
    pip -r requirements.txt
    ```

### Executando

- Sempre ativar o ambiente virtual antes de realizar qualquer ação
    - ```shell
        source .venv/bin/activate
        ```

- Rodar o script referente ao site desejado
    - Olx: 
    ```shell
    python olx/olx.py
    ```
    - Mercado Livre: 
    ```shell
    python mercadolivre/ml.py
    ```
