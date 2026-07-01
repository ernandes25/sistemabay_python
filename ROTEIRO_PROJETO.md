# Roteiro do Sistema Bay

Este arquivo sera usado como mapa de estudo e implantacao do projeto. A ideia e avancar aos poucos, entendendo cada etapa antes de seguir.

## 1. Visao geral

- Caminho oficial do projeto: `/home/ernandes/Bay Software/sistemabay_python`.
- Linguagem principal: Python.
- Framework principal: Django.
- Banco de dados: PostgreSQL.
- O sistema sera uma aplicacao web modular.
- O primeiro modulo sera Empresas.
- Depois virao Tarefas, Financeiro simples e Escala de louvor.
- Nao comecaremos com microservicos.

## 2. Por que Django

- Django facilita a criacao de sistemas web completos.
- Ele ja traz estrutura para banco de dados, telas administrativas, usuarios, permissoes e formularios.
- Para este projeto, Django ajuda a sair mais rapido do planejamento e chegar a um sistema funcionando.
- O foco sera aprender construindo o Sistema Bay.

## 3. Modulos previstos

- Base do sistema
- Empresas
- Usuarios
- Departamentos
- Tarefas
- Planos de tarefas
- Relatorios
- Notificacoes
- Financeiro simples, no futuro
- Escala de louvor, no futuro

## 4. Primeiro modulo: Empresas

- Nome.
- CNPJ.
- Endereco: logradouro, numero, complemento, bairro, cidade, UF e CEP.
- Contato: telefone/WhatsApp.
- Email.
- Tributacao: Simples Nacional, Lucro Presumido, Lucro Real, MEI ou PF.
- Observacao.
- A tributacao devera ajudar na escolha do plano de tarefas.

## 5. Modulo tarefas

- Departamentos.
- Tipos de tarefa.
- Cadastro de tarefas.
- Vencimentos e periodicidades.
- Vinculo entre empresas e tarefas.
- Planos de tarefas por tipo de tributacao.
- Conclusao e reabertura de tarefas.
- Filtros, grade, calendario e relatorios.
- Notificacoes futuras via WhatsApp.

## 6. Modulo financeiro futuro

- Controle de caixa.
- Lancamentos de despesas.
- Lancamentos de recebimentos.
- Categorias financeiras.
- Consulta de saldo.
- Relatorios simples.

## 7. Modulo escala de louvor futuro

- Cadastro de pessoas.
- Cadastro de funcoes.
- Cadastro de datas.
- Montagem de escalas.
- Consulta de escalas por periodo.
- Possiveis notificacoes.

## 8. Ferramentas do projeto

- Python 3.
- Django.
- PostgreSQL.
- VS Code.
- DBeaver.
- Git.
- Navegador web.

## 9. Ferramentas e base ja preparadas

- Pasta `sistemabay_python` criada.
- Ambiente virtual `venv` criado.
- Django instalado.
- `psycopg2-binary` instalado.
- Projeto Django criado com `config`.
- Servidor Django testado em `http://127.0.0.1:8000/`.
- Banco `sistemabay_python_db` criado.
- Usuario `sistemabay_user` criado.
- Django configurado para usar PostgreSQL.
- Migracoes iniciais do Django aplicadas no PostgreSQL.
- App `empresas` criado e registrado.
- Model `Empresa` criado.
- Migration inicial de empresas criada e aplicada.
- Campo `complemento` adicionado em Empresa.
- Empresa registrada no admin do Django.
- Superusuario do Django criado.
- Cadastro de empresas testado pelo admin.
- App `tarefas` criado e registrado.
- Model `Departamento` criado.
- Migration inicial de tarefas criada e aplicada.
- Departamento registrado no admin do Django.
- Model `TipoTarefa` criado.
- Migration de tipos de tarefa criada e aplicada.
- Tipo de tarefa registrado no admin do Django.
- Model `Tarefa` criado.
- Migration de tarefas criada e aplicada.
- Tarefa registrada no admin do Django.
- Model `PlanoTarefa` criado.
- Model `PlanoTarefaItem` criado.
- Migration de planos de tarefas criada e aplicada.
- Plano de tarefas registrado no admin do Django.
- Empresa vinculada opcionalmente a um Plano de Tarefas.
- Model `EmpresaTarefaAjuste` criado.
- Ajuste individual de tarefas por empresa registrado no admin do Django.

## 10. Estrutura geral do Django

- `manage.py`: comando principal do projeto Django.
- `config/settings.py`: configuracoes do sistema.
- `config/urls.py`: rotas principais do sistema.
- `config/wsgi.py` e `config/asgi.py`: arquivos usados para publicacao do sistema.
- `venv`: ambiente virtual com as bibliotecas do projeto.
- Apps Django: partes do sistema, como `empresas`, `tarefas` e `financeiro`.

## 11. Conceitos importantes

- Projeto Django: configuracao geral do sistema.
- App Django: modulo interno do sistema.
- Model: classe que representa uma tabela do banco.
- Migration: arquivo que ensina o Django a criar ou alterar tabelas.
- Admin: painel administrativo automatico do Django.
- View: parte que recebe uma requisicao e devolve uma resposta.
- Template: arquivo HTML usado para montar telas.
- URL: endereco que leva para uma tela ou funcao do sistema.

## 12. Ordem recomendada de implantacao

1. Preparar ambiente Python.
2. Criar projeto Django.
3. Configurar PostgreSQL.
4. Aplicar migracoes iniciais.
5. Criar o app `empresas`.
6. Registrar o app no Django.
7. Criar o model `Empresa`.
8. Criar as migrations de empresas.
9. Aplicar as migrations no banco.
10. Registrar Empresa no admin.
11. Criar superusuario do Django.
12. Testar cadastro de empresas pelo admin.
13. Criar o app `tarefas`.
14. Criar o model `Departamento`.
15. Criar o cadastro de tipos de tarefa.
16. Criar o cadastro basico de tarefas.
17. Criar o cadastro de planos de tarefas.
18. Vincular tarefas aos planos.
19. Vincular empresa a um plano de tarefas.
20. Criar ajustes individuais de tarefas por empresa.

## 13. Proximo passo atual

- Testar o cadastro de planos de tarefas pelo admin.
- Criar o plano padrao do Simples Nacional.
- Vincular tarefas ao plano.
- Abrir o cadastro da empresa e selecionar o plano de tarefas.
- Testar ajuste individual adicionando ou removendo uma tarefa para uma empresa.

## 14. Regra de estudo

- Fazer uma etapa por vez.
- Nao tentar construir tudo no mesmo dia.
- Primeiro entender a ideia.
- Depois entender a estrutura.
- Depois implementar com calma.
- Evitar codigo pronto sem entender.
- Manter foco em Python e Django.
