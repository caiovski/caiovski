---
description: Regra de Atualização e Registro de Relatórios Técnicos (Testes, Bugfixes, Patches e Manutenções)
---

# Regra Absoluta: Registro de Relatórios Técnicos (opsx-technical)

Este documento define as regras absolutas, o padrão de design e a convenção de nomenclatura em inglês para os relatórios técnicos salvos na pasta de manutenção técnica:
```
updates/update-tecnico/
```

Sempre que a IA receber o comando `/opsx:technical` ou `@opsx-technical {tipo de problema técnico}`, ela deve seguir este fluxo rigorosamente.

---

## 🏷️ 1. Convenção de Nomenclatura em Inglês

A IA deve analisar o `{tipo de problema técnico}` fornecido e categorizar a intervenção em um dos cinco padrões abaixo. O nome do arquivo deve ser gerado em minúsculas (lower snake_case) seguindo o respectivo prefixo:

| Categoria | Descrição | Padrão de Nome do Arquivo | Exemplo Prático |
| :--- | :--- | :--- | :--- |
| **Tests** | Novos testes unitários/integração | `test_[funcionalidade_testada]_[N].md` | `test_pdv_checkout_1.md` |
| **Bugfix** | Correção de bugs, crashes e erros | `bugfix_[descricao_do_bug]_[N].md` | `bugfix_rls_timeout_1.md` |
| **Patch** | Ajustes rápidos, correções críticas | `patch_[descricao_do_patch]_[N].md` | `patch_frete_switch_1.md` |
| **Maintenance** | Refatoração, performance, limpeza | `maintenance_[descricao_manutencao]_[N].md` | `maintenance_db_migrations_1.md` |
| **Others (Tech)** | Outras mudanças de infra/configuração | `tech_[descricao_tecnica]_[N].md` | `tech_supabase_setup_1.md` |

*(Onde `[N]` representa o número sequencial daquele tipo de ajuste técnico específico, iniciando em 1 e incrementando caso já existam arquivos com o mesmo nome na pasta `updates/update-tecnico/`)*.

### Exemplo de Mapeamento de Comando:
- `@opsx-technical correção de bugs de erros` ➡️ Categoria: **Bugfix** ➡️ Arquivo: `updates/update-tecnico/bugfix_rls_timeout_1.md`
- `@opsx-technical novos testes de checkout` ➡️ Categoria: **Tests** ➡️ Arquivo: `updates/update-tecnico/test_checkout_flow_1.md`

---

## 💎 2. Padrão Estético e Estrutura do Relatório

O relatório gerado dentro de `updates/update-tecnico/` deve seguir um layout de alto nível e rica legibilidade, contendo:

1. **Header Visual Premium**:
   - Capsule-render no topo: `<img style="width:100%" src="https://capsule-render.vercel.app/api?type=waving&color=3F51B5&section=header" />`
   - Título centralizado com a categoria em evidência: `🛠️ [BUGFIX] - Descrição Curta`

2. **Badges de Status e Escopo**:
   - Badges contendo `Status: Resolvido/Concluído`, `Categoria`, `Impacto` e `Plataforma`.

3. **Seções Mandatórias**:
   - **🔍 1. Descrição do Problema / Cenário**: Explicação clara do erro reportado pelo usuário ou da necessidade de teste.
   - **🧠 2. Análise de Causa Raiz**: Investigação técnica detalhada do porquê o erro acontecia (ex: recursão infinita, vazamento de memória).
   - **⚡ 3. Solução Implementada**: Resumo técnico da refatoração e código aplicado para resolver o problema.
   - **📂 4. Arquivos Modificados**: Links absolutos e limpos para os arquivos que sofreram modificação.
   - **🧪 5. Resultados de Validação & Logs**: Logs de saída de testes, logs de build ou a comprovação de compilação limpa via `npx tsc --noEmit`.

---

## 🛡️ 3. Guardrails e Validação

- **Bypass de Overlaps**: Sempre verifique o diretório `updates/update-tecnico/` antes de salvar para evitar sobrescrever logs anteriores, garantindo a sequência incremental `_N.md`.
- **Integridade da Base**: Certifique-se de que os ajustes não corrompam a integridade dos dados históricos locais ou em nuvem.
- **Compilação Limpa**: Nunca dê um ticket técnico como "resolvido" sem atestar 100% de compilação livre de erros nas plataformas do AgroPet.
