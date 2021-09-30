## Projeto de gestão de espaços esportivos



### Tecnologias utilizadas:
- Flask
- SQLite
- HTML
- CSS
- JAVASCRIPT


### Preparando ambiente e executando:

Abrir terminal e clonar o repositório atráves do comando abaixo
```bash
git clone https://github.com/weslleyalmeid/futdata.git
```

Criar arquivo secrets e adicionar secret
```bash
vim .secrets.toml
```

```vi
[default]
SECRET_KEY = "NomeQualquer"
```

Criar ambiente virtual
```bash
virtualenv .venv
source bin activate
```

Instalar dependências
```bash
make install 
```

Inicilizando database e executando
```bash
make init-db
make run
```

### Site:
[Link Futdata](http://weslleyalmeid.pythonanywhere.com/)
