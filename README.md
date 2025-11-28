# Desafio-2

# Simulação Educacional de Malware — Ransomware & Keylogger (Projeto DIO)

**Autor:** Elielton da Silva Tavares
**Propósito:** Demonstrar, de forma ética e segura, os conceitos de ransomware e keylogger por meio de simulações em ambiente controlado. O objetivo é entender o funcionamento, os vetores de ataque, e principalmente as estratégias de detecção e mitigação.

> **Aviso importante:** Não há nem haverá código malicioso funcional neste repositório. Todos os scripts e demonstrações são **simulações seguras** que não danificam arquivos reais nem capturam dados sensíveis. Execute apenas em máquinas isoladas com snapshots e em ambiente de teste.

---

## Sumário

* Escopo e ética
* Ambiente usado
* Metodologia (como simulei o Ransomware e o Keylogger de forma segura)
* Ferramentas de monitoramento e coleta de evidências
* Resultados e análise (exemplos de logs / capturas)
* Recomendações de defesa e medidas preventivas
* Estrutura do repositório e como reproduzir a simulação de forma segura

---

## 1. Escopo e considerações éticas

Este projeto tem fins educacionais e foi realizado em ambiente isolado (VirtualBox, rede host-only). Não realizei criptografia de arquivos de produção nem capturei teclas reais de usuários. O objetivo é entender padrões de comportamento de ameaça e construir contramedidas.

---

## 2. Ambiente utilizado

* Host: VirtualBox (com snapshots antes de todo teste)
* Máquina alvo: Ubuntu/Windows (VM isolada — sem internet ou com rede host-only)
* Máquina analista: Kali Linux / Windows com ferramentas de monitoramento
* Ferramentas: Wireshark, Sysmon (Windows), auditd / inotify (Linux), osquery, Falco, antivírus (ex.: Windows Defender), editor de logs, Python (apenas para scripts de simulação)

---

## 3. Metodologia segura de simulação

### Ransomware (simulado)

* **Objetivo didático:** demonstrar fluxo: descoberta → encriptação (simulada) → nota de resgate → impacto em disponibilidade.
* **Abordagem segura usada:**

  * Geração de **arquivos de teste** (por ex. 100 arquivos `test_001.txt`...`test_100.txt` com conteúdo "TEST").
  * Script **simulado** que **não modifica** o conteúdo original. Em vez disso, cria cópias em `simulated_encrypted/` com um header que diz: "THIS IS A SIMULATION — CONTENT NOT ENCRYPTED".
  * O script registra eventos em `ransom_simulation.log` com timestamps (ex.: "arquivo X simulado como criptografado às HH:MM").
  * Geração de uma **nota de resgate** (`README_RANSOM_NOTE.txt`) contendo instruções fictícias (sem incluir qualquer mecanismo de pagamento real).
* **Objetivo de análise:** observar logs de criação/remoção de arquivos, alertas do sistema, tráfego de rede (se houve tentativa de exfil), e time to detect.

### Keylogger (simulado)

* **Objetivo didático:** explicar pipeline de captura → armazenamento → exfiltração.
* **Abordagem segura usada:**

  * Em vez de capturar teclas reais, usei um arquivo de **entrada simulada** (`simulated_keystrokes.txt`) contendo exemplos de digitação.
  * Um script/processo demo lê esse arquivo e grava linhas em `simulated_keylog.txt`, mostrando como um keylogger gravaria localmente.
  * Em vez de enviar por rede, o fluxo demonstra preparação para exfiltração ao gravar um artefato em `exfil_ready/` e produzir um log de "envio simulado".
* **Objetivo de análise:** monitorar processos que leem arquivos, logs de disco e rede, e demonstrar como EDR e regras de IDS poderiam detectar o comportamento.

---

## 4. Ferramentas de monitoramento e testes de detecção

* **Linux:** `auditd`, `inotifywait`, `syslog`, `osquery`
* **Windows:** Sysmon (configuração de monitoramento de criação de processos, escrita de arquivos e conexões de rede), Process Monitor
* **Rede:** Wireshark para capturar tráfego e identificar exfiltração simulada
* **SIEM/alerta:** configurar regras simples (ex.: alertar quando processo `python` cria mais de N arquivos em M segundos)
* **EDR/antivírus:** testar se ações simuladas geram alertas (esperado: scripts simulados não devem ser bloqueados, mas padrões anômalos podem ser detectados)

---

## 5. Resultados esperados (exemplos)

* `ransom_simulation.log` — registros de “arquivos criptografados” (simulação) com timestamps.
* `simulated_encrypted/` — cópias de arquivos de teste com nota “SIMULAÇÃO” no cabeçalho.
* `simulated_keylog.txt` — arquivo com linhas provenientes do dataset simulado.
* Wireshark capture mostrando tráfego HTTP POST (caso ativado um envio de teste para servidor local).
* Sysmon/auditd logs mostrando processos e eventos de arquivo.

(Os arquivos reais de evidência devem ser colocados na pasta `outputs/` do repositório.)

---

## 6. Medidas de defesa e mitigação

* **Backups isolados e testados** (imediatamente restauráveis).
* **Controle de privilégios:** limitar direitos de escrita em diretórios sensíveis.
* **EDR e regras Sysmon:** monitorar criação em massa de arquivos, processos que leem dispositivos de entrada, spawn de shells.
* **Segmentação de rede e bloqueio de canais de exfiltração:** DNS filtering, blocklists e proxies com inspeção.
* **Conscientização de usuários:** não executar anexos ou scripts desconhecidos.
* **Política de aplicação de patches e hardening.**

---

## 7. Estrutura sugerida do repositório

```
/simulacao-malware-dio/
├─ README.md
├─ scripts_simulados/
│  ├─ generate_test_files.py          # gera arquivos de teste (não malicioso)
│  ├─ simulate_ransom.py              # SIMULA (cria cópias com header), NÃO encripta
│  └─ simulate_keylog_pipeline.py    # lê dataset simulado e escreve log (sem capturar teclas reais)
├─ datasets/
│  ├─ simulated_keystrokes.txt
│  └─ test_files_sample/
├─ outputs/
│  ├─ ransom_simulation.log
│  ├─ simulated_keylog.txt
│  └─ wireshark_capture.pcap
├─ images/
│  ├─ sysmon_alert.png
│  └─ wireshark_exfil.png
└─ report.md
```

---

## 8. Como reproduzir (passos seguros)

1. Crie snapshots das VMs.
2. Clone o repositório na VM alvo de teste.
3. Execute `generate_test_files.py` para popular a pasta de teste.
4. Execute `simulate_ransom.py --simulate` (modo simulado: NÃO altera arquivos originais) e observe `outputs/`.
5. Execute `simulate_keylog_pipeline.py --input datasets/simulated_keystrokes.txt` para simular pipeline.
6. Coleta: abra Sysmon/ auditd / Wireshark para capturar eventos durante execução.
7. Analise `outputs/` e `report.md`.

---

## 9. Entrega e documentação

* README.md (este arquivo) — instruções e ética.
* scripts_simulados/ — scripts seguros usados nas simulações (com comentários).
* outputs/ — logs e capturas que comprovam a execução.
* report.md — análise final, lições aprendidas e recomendações.

---

## 10. Observações finais

Este projeto tem foco em **educação e defesa**. Se você quiser que eu **gere os scripts de simulação (apenas não-destrutivos e comentados)**, ou que eu escreva `report.md` e `ransom_simulation.log` de exemplo, me avise que eu crio os artefatos seguros para você adicionar ao repositório.

---


