---
description: Regra Absoluta de Atualização do README.md e Histórico de Updates (Sprint de Inovação)
---

# Regra Absoluta: Atualização de Catálogo de Updates (README.md)

Este documento define a regra absoluta e o padrão de engenharia para atualização do histórico de lançamentos do **AgroPet Lambari** no arquivo `README.md` e a criação de relatórios de sprint. Sempre que novas funcionalidades forem concluídas, o Agente de IA deve seguir estas diretrizes sem exceção.

---

## 🕹️ 1. O Padrão de Atualização do `README.md`

### 🧹 Limpeza de Histórico Obsoleto (Prevenção de Inchaço)
- Sempre localize a seção `## 🕹️ Histórico de Updates Realizados (Sprint de Inovação)`.
- **Regra de Descarte**: Remova permanentemente os **dois primeiros (mais antigos)** tópicos da listagem anterior para manter o arquivo README compacto, limpo e focado nos marcos recentes.
- **Reordenação**: Reordene de forma sequencial todos os tópicos restantes que foram mantidos (começando do número 1).

### ➕ Inserção dos Novos Lançamentos
- Adicione os novos recursos implementados no commit atual, numerando-os sequencialmente a partir dos existentes.
- Escreva uma explicação detalhada e rica sobre o que foi implementado para cada tópico novo.
- **Marcador de Novidade**: No final do título de cada nova seção criada, adicione a etiqueta:
  ```markdown
  (NOVO!!!) — DD/MM/AAAA
  ```
  *(Onde DD/MM/AAAA deve ser substituído pela data local corrente no formato brasileiro)*.

### 🖼️ Manutenção do Banner de Updates
- O arquivo vetorial `updates-banner.svg` está localizado na pasta consolidada de assets (`assets/updates-banner.svg`).
- **Garantia de Caminho**: Certifique-se de que a tag `<img>` correspondente no README aponte corretamente para:
  ```html
  <img src="assets/updates-banner.svg?v=..." width="500" alt="AgroPet Updates" />
  ```
  *(Qualquer referência direta sem a pasta `assets/` deve ser proativamente corrigida)*.

---

## 📑 2. Criação do Relatório Técnico `update_[N].md`

Sempre que concluir um ciclo de entregas (Sprint), o agente deve gerar um relatório autônomo e aprofundado documentando a arquitetura e o funcionamento técnico das novidades.

- **Localização**: Crie o arquivo `update_[N].md` (onde `[N]` é o número sequencial da Sprint, ex: `update_2.md`) dentro de:
  ```
  updates/update/
  ```
- **Identidade Estética Premium**: O relatório deve imitar o design de alta fidelidade visual de `update_1.md`:
  - Utilizar waving header do Capsule-Render no topo.
  - Tabela centralizada com badges de status, framework e banco de dados.
  - Diagramas explicativos em `mermaid` demonstrando o fluxo lógico das interações.
  - Separação rica por componentes (Cliente vs Admin vs Banco de Dados).
  - Indicação clara de resultados de verificação de tipos e compilação limpa.

---

## 🛡️ 3. Guardrails e Validação de Compilação

Antes de concluir qualquer tarefa ou propor a mensagem de commit:
1. **TypeScript Type-Safety**: Rode `npx tsc --noEmit` nos projetos modificados para garantir que nenhuma refatoração quebrou tipos ou interfaces.
2. **Sem Placeholders**: Documente a realidade exata do código modificado, citando os arquivos corretos.
3. **Tom de Comunicação**: Mantenha um tom profissional, humilde, rico e focado em engenharia de software de alta fidelidade técnica.
