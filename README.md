# 🏦 Banco de Talentos RH  - EM CONSTRUÇÃO 
### Um sistema para recrutamento inteligente — construído do zero em Python  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> 💡 **De analista de RH para desenvolvedor Python** — este projeto faz parte da minha transição de carreira.  
> Construído inteiramente por mim, do zero, para treinar Python, APIs, bancos de dados e arquitetura limpa.

---

## 🎯 Objetivo

Criar um **sistema interno de banco de talentos** que:
- Cadastre candidatos com currículo em PDF  
- Liste perfis com objetivo profissional  
- Gerencie vagas em aberto  
- Sugira compatibilidade entre candidatos e vagas (**sem IA complexa!**)  
- Prepare o terreno para um Kanban de acompanhamento  

Tudo isso **com código limpo, testável e escalável** — não só funcional.

---

## 🛠️ Tecnologias & Boas Práticas

| Camada | Tecnologia | Por quê? |
|--------|------------|----------|
| **Backend** | Python 3.12 + FastAPI | Moderno, rápido, auto-documentado (`/docs`) |
| **Banco** | SQLite (→ PostgreSQL no futuro) | Zero configuração para início |
| **Validação** | Pydantic v2 | Segurança de tipos, validação automática de e-mails |
| **Upload** | `python-multipart` | Integração nativa com FastAPI |
| **Frontend** | HTML/CSS puro + Jinja2 + Tailwind CSS | Foco no aprendizado |
| **Dados** | **Faker** | Geração realista de candidatos e vagas para testes |
| **Arquitetura** | Camadas claras (`models`, `schemas`, `services`, `api`) |

---

## 🌟 Funcionalidades Implementadas

### Cadastro de Candidatos
- Formulário com validação no frontend e backend  
- Upload seguro de currículos (`uploads/`)  
- Tratamento de e-mails duplicados com mensagens amigáveis  
- Geração de dados com **Faker** para testes em massa:

---
## Rodando localmente

1. Clonar o repositório e entrar na pasta
```
git clone https://github.com/seu-usuario/banco-talentos-rh.git
cd banco-talentos-rh
```

2. Criar e ativar ambiente virtual (recomendado)
```
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# ou
.venv\Scripts\activate         # Windows
```

3. Instalar dependências
```
pip install -r requirements.txt
```
4. Gere dados falsos (opcional)
```
python seed.py
```

5. Iniciei o servidor local (port: 8000, opcional)
```
uvicorn app.main:app --reload
```

