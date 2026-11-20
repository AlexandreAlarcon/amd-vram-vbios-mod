# AMD Radeon VBIOS Mod & VRAM Expansion Study

Este repositório documenta um estudo prático de engenharia reversa, modificação de firmware (VBIOS) e adaptação lógica de memória em placas de vídeo AMD Radeon hd6700 (arquitetura Juniper) para expansão teórica de VRAM.

## 🛠️ Sobre o Projeto
O objetivo deste projeto é analisar a estrutura interna de uma VBIOS de 64 KB, localizar os blocos de configuração da controladora de memória na tabela `VRAM_Info` (AtomBIOS v2.1) e automatizar o processo de atualização de parâmetros de densidade (`ucDensity`) e capacidade (`ucMemorySize`) através de automação em Python.

## 📂 Estrutura do Repositório
* `BiosOriginal.rom` — Dump original da VBIOS extraído via GPU-Z (64 KB).
* `bios_modificada.rom` — Ficheiro gerado com os parâmetros ajustados para simulação de 2 GB e checksum recalculado.
* ` hd6700_hex_modifier.py` — Script em Python responsável por automatizar o patch binário e o balanceamento de CRC de 8 bits.

## 🚀 Como Executar o Script de Patch
Certifique-se de que o ficheiro de dump original (`bios_original.rom`) está na mesma pasta e com nome correto no arquivo e execute o script via terminal:

```cmd
python hd6700_hex_modifier.py
