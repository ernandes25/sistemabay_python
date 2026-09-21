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
- Organizacoes
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
- Cada empresa pertence a uma Organizacao.
- No futuro, a Organizacao representara cada escritorio ou cliente que usa o sistema.

## 5. Modulo tarefas

- Departamentos.
- Tipos de tarefa.
- Cadastro de tarefas.
- Tarefas principais e subtarefas.
- Data interna de execucao para tarefas principais.
- Alerta por antecedencia para execucao interna.
- Baixa/conclusao feita pelas subtarefas.
- Vencimentos e periodicidades.
- Ajuste de vencimento em dia nao util.
- Dias de antecedencia para alerta.
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
- Model `Organizacao` criado.
- Model `Empresa` criado.
- Migration inicial de empresas criada e aplicada.
- Campo `complemento` adicionado em Empresa.
- Empresa registrada no admin do Django.
- Organizacao registrada no admin do Django.
- Organizacao padrao `Bay Software` criada.
- Empresas existentes vinculadas a Organizacao padrao.
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
- Campos `ajuste_dia_nao_util` e `dias_antecedencia_alerta` adicionados em Tarefa.
- Campos de tarefa principal, subtarefas e execucao interna adicionados em Tarefa.
- Regra definida: tarefas principais nao devem ser baixadas diretamente; subtarefas devem ser baixadas individualmente.
- Model `OcorrenciaTarefa` criado.
- Ocorrencias de tarefas registradas no admin do Django.
- Status gravados definidos: Pendente, Concluida e Cancelada.
- Status Atrasada definido como calculado automaticamente pelo sistema.
- Biblioteca `holidays` instalada e registrada no `requirements.txt`.
- Arquivo `tarefas/dias_uteis.py` criado, com as funcoes `eh_feriado`, `eh_dia_util`, `dia_util_anterior` e `dia_util_posterior`.
- Funcao `calcular_data_vencimento` completa, com ultimo dia do mes, ultimo dia util e ajuste de dia nao util.
- Funcao `calcular_data_execucao` criada, para o prazo interno de execucao das tarefas principais.
- Funcao `calcular_data_alerta` criada, usando a execucao para tarefa principal e o vencimento para tarefa simples ou subtarefa.
- Funcao `buscar_tarefas_da_empresa` alterada para devolver tarefas, incluindo as subtarefas das tarefas principais do plano, e aplicando os ajustes individuais de adicionar e remover.
- `Tarefa.clean()` passa a exigir pelo menos uma subtarefa quando a tarefa principal ja existe no banco.
- Correcao do calculo de mes quando a competencia passa de um ano, como dezembro com doze meses depois.
- Testes de calculo de datas, de execucao, de alerta e de busca de tarefas da empresa.

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
- Organizacao: representa o dono dos dados. Hoje sera usada para o proprio escritorio; no futuro permitira separar os dados de varios clientes do sistema.
- Tarefa principal: agrupa subtarefas e controla a execucao interna.
- Subtarefa: representa cada entrega ou obrigacao que pode ser baixada pelo usuario.
- Tarefa simples: tarefa que nao tem subtarefas e pode ser executada sozinha.
- O cadastro de tarefa possui o campo Natureza, com as opcoes Tarefa principal, Tarefa simples e Subtarefa.

## 11.1 Regras importantes de tarefas

- Uma tarefa principal nao deve ser baixada diretamente.
- A baixa/conclusao deve acontecer nas subtarefas.
- Uma subtarefa pode ser baixada individualmente pelo usuario.
- Uma tarefa principal deve ser considerada concluida somente quando todas as suas subtarefas estiverem concluidas.
- Uma tarefa sem subtarefas podera ser baixada diretamente.
- O plano de tarefas deve receber tarefas principais ou tarefas simples.
- Subtarefas nao devem ser adicionadas diretamente ao plano; elas entram no plano por meio da tarefa principal.
- Ajustes individuais por empresa poderao adicionar ou remover tarefas especificas, inclusive subtarefas, quando for necessario tratar uma excecao.
- Ao editar uma subtarefa no admin, os campos de execucao interna devem ficar visualmente inativos.
- Tarefa simples e subtarefa nao podem controlar execucao interna; essa regra pertence a tarefa principal.
- O campo Tarefa principal deve listar apenas tarefas cadastradas como Tarefa principal.
- Uma subtarefa so pode ser vinculada a uma tarefa principal do mesmo departamento.
- No admin, ao escolher o departamento da subtarefa, o campo Tarefa principal deve mostrar apenas tarefas principais daquele departamento.
- Para tarefas principais, o grupo principal de datas e o Prazo interno de execucao.
- Para tarefas simples e subtarefas, o grupo principal de datas e o Vencimento oficial da tarefa.
- Os campos de mes da competencia devem ser exibidos como opcoes simples, de Na propria competencia ate Doze meses depois.
- Essa regra permite cadastrar obrigacoes anuais que vencem no ano seguinte, como ECD e ECF.
- A ocorrencia de tarefa representa uma tarefa real de uma empresa em uma competencia.
- O cadastro de tarefa guarda a regra; a ocorrencia guarda o que precisa ser executado naquele periodo.
- Atrasada nao deve ser marcada manualmente; o sistema calcula quando a ocorrencia esta pendente e passou da data de referencia.
- Para tarefa principal, a data de referencia da ocorrencia e a data de execucao interna.
- Para tarefa simples ou subtarefa, a data de referencia da ocorrencia e a data de vencimento oficial.

## 11.2 Diferenca entre tarefa simples e subtarefa

As duas podem ser baixadas pelo usuario, mas nao sao a mesma coisa.

- Tarefa simples: existe sozinha, nao tem tarefa principal e pode ser adicionada diretamente ao plano.
- Subtarefa: existe sempre dentro de uma tarefa principal, e obrigatorio informar a tarefa principal dela.
- Subtarefa nao pode ser adicionada diretamente ao plano; ela entra no plano por meio da tarefa principal.
- Apenas a tarefa principal controla execucao interna e possui prazo interno de execucao.
- Tarefa simples e subtarefa possuem vencimento oficial proprio.
- No banco, as tres naturezas sao valores separados: Tarefa principal, Tarefa simples e Subtarefa.

## 11.3 Regras de remocao de tarefas de uma empresa

Estas regras valem para os ajustes individuais por empresa.

- O usuario pode remover a tarefa principal. Nesse caso, o sistema remove a tarefa principal e todas as subtarefas dela de uma so vez, para que ele nao precise remover subtarefa por subtarefa.
- O usuario tambem pode remover apenas uma subtarefa especifica, quando a empresa nao tem aquela obrigacao. Exemplo: empresa que so tem retirada de pro-labore nao gera guia de FGTS.
- Se o usuario remover a ultima subtarefa de uma tarefa principal, o sistema avisa e remove tambem a tarefa principal, porque ela ficaria sem subtarefas.
- Nos casos de remocao da tarefa principal ou da ultima subtarefa, o usuario deve ser avisado antes da remocao ser efetivada.
- Remover uma subtarefa que nao e a ultima nao altera a tarefa principal.

## 11.4 Regras de adicao de tarefas de uma empresa

- Ao adicionar uma tarefa principal como ajuste individual, e obrigatorio informar pelo menos uma subtarefa.
- Uma tarefa principal nunca deve existir sem pelo menos uma subtarefa.
- Ao salvar a tarefa principal pela primeira vez, ela ainda nao possui subtarefas, por isso a exigencia so e verificada a partir do momento em que a tarefa ja existe no banco.
- Tarefa simples e subtarefa podem ser adicionadas como ajuste individual sem exigencia extra.

## 12. Ordem recomendada de implantacao

1. Preparar ambiente Python.
2. Criar projeto Django.
3. Configurar PostgreSQL.
4. Aplicar migracoes iniciais.
5. Criar o app `empresas`.
6. Registrar o app no Django.
7. Criar o model `Organizacao`.
8. Criar o model `Empresa`.
9. Criar as migrations de empresas.
10. Aplicar as migrations no banco.
11. Registrar Organizacao e Empresa no admin.
12. Criar superusuario do Django.
13. Testar cadastro de empresas pelo admin.
14. Criar o app `tarefas`.
15. Criar o model `Departamento`.
16. Criar o cadastro de tipos de tarefa.
17. Criar o cadastro basico de tarefas.
18. Criar o cadastro de planos de tarefas.
19. Vincular tarefas aos planos.
20. Vincular empresa a um plano de tarefas.
21. Criar ajustes individuais de tarefas por empresa.
22. Criar tarefas principais e subtarefas.
23. Configurar execucao interna das tarefas principais.
24. Criar ocorrencias de tarefas por competencia.
25. Criar controle de baixa/conclusao das subtarefas.
26. Criar reabertura de ocorrencias concluidas.

Situacao atual desta lista:

- Itens 1 a 23 concluidos.
- Item 24 em andamento: as funcoes de calculo de datas, a busca de tarefas da empresa com subtarefas e ajustes e as regras de principal com subtarefas ja estao prontas; falta a funcao que cria as ocorrencias.
- Itens 25 e 26 ainda nao iniciados.

## 13. Proximo passo atual

Concluido:

- Logica que calcula datas de vencimento, de execucao e de alerta.
- Tratamento de ultimo dia do mes e de ultimo dia util.
- Ajuste de data que cai em dia nao util: manter, antecipar ou prorrogar.
- Funcoes auxiliares de feriados e dias uteis no arquivo `tarefas/dias_uteis.py`, usando a biblioteca `holidays` com feriados nacionais do Brasil.
- `Tarefa.clean()` passa a exigir pelo menos uma subtarefa quando a tarefa principal ja existe no banco.
- `buscar_tarefas_da_empresa` passa a devolver tarefas, incluindo as subtarefas de cada tarefa principal do plano, e ja aplica os ajustes individuais de adicionar e remover.

Proximos passos:

- Aplicar as regras de remocao em grupo no admin de ajustes: remover a tarefa principal remove junto as subtarefas dela, com aviso ao usuario.
- Avisar e remover a tarefa principal quando a ultima subtarefa dela for removida.
- Exigir pelo menos uma subtarefa ao adicionar uma tarefa principal como ajuste individual.
- Criar uma forma de gerar ocorrencias de tarefas por empresa e competencia.
- Testar ocorrencias geradas para tarefa principal, tarefa simples e subtarefa.

## 14. Regra de estudo

- Fazer uma etapa por vez.
- Nao tentar construir tudo no mesmo dia.
- Primeiro entender a ideia.
- Depois entender a estrutura.
- Depois implementar com calma.
- Evitar codigo pronto sem entender.
- Manter foco em Python e Django.
