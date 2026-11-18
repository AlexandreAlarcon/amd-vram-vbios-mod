import os
import sys

# Caminhos dos arquivos no diretório C:\Users\Alexandre\Desktop\bios
DIR_BIOS = r"C:\Users\Alexandre\Desktop\bios"
ARQUIVO_ORIGINAL = os.path.join(DIR_BIOS, "BiosOriginal.rom")
ARQUIVO_MODIFICADO = os.path.join(DIR_BIOS, "bios_modificada.rom")

# Offsets exatos mapeados na tabela ATOM_VRAM_MODULE_V7 (VRAM_Info em 0xB036)
# Cada módulo (MT41J64M16, H5TQ1G63DFR, K4W1G1646G, ATI_23EY2387MA, NT5CB64M16DP)
# possui ucDensity (+0x0E) = 0x42 (64Mx16 / 1Gbit) e ucMemorySize (+0x14) = 0x10 (16 * 64MB = 1024MB)
MODULOS_VRAM = [
    {"nome": "MT41J64M16 (Micron)",     "offset_base": 0xB04A},
    {"nome": "H5TQ1G63DFR (Hynix)",     "offset_base": 0xB0CA},
    {"nome": "K4W1G1646G (Samsung)",    "offset_base": 0xB17A},
    {"nome": "ATI_23EY2387MA (Elixir)", "offset_base": 0xB28A},
    {"nome": "NT5CB64M16DP (Nanya)",    "offset_base": 0xB30A},
]

# Valores para 2 GB (2048 MB) em barramento 128-bit (8 chips x 256 MB / 2 Gbit = 128Mx16)
NOVA_DENSIDADE = 0x52    # 128Mx16 (2 Gbit por chip DDR3/GDDR3)
NOVO_MEMORY_SIZE = 0x20  # 32 * 64 MB = 2048 MB (2 GB)

def patch_vbios():
    if not os.path.exists(ARQUIVO_ORIGINAL):
        print(f"[ERRO] Arquivo original não encontrado em: {ARQUIVO_ORIGINAL}")
        sys.exit(1)

    with open(ARQUIVO_ORIGINAL, "rb") as f:
        rom = bytearray(f.read())

    if len(rom) != 65536:
        print(f"[ERRO] Tamanho inesperado: {len(rom)} bytes (esperado: 65536 bytes).")
        sys.exit(1)

    if rom[0:2] != b"\x55\xAA":
        print("[ERRO] Assinatura PCI ROM (55 AA) inválida.")
        sys.exit(1)

    print(f"[OK] VBIOS original carregada ({len(rom)} bytes). Assinatura 55 AA confirmada.\n")

    # 1. Aplicar alterações nos registros de densidade e capacidade de cada módulo
    for mod in MODULOS_VRAM:
        base = mod["offset_base"]
        off_density = base + 0x0E
        off_memsize = base + 0x14

        dens_antiga = rom[off_density]
        size_antigo = rom[off_memsize]

        rom[off_density] = NOVA_DENSIDADE
        rom[off_memsize] = NOVO_MEMORY_SIZE

        print(f"Módulo: {mod['nome']}")
        print(f"  - ucDensity    [0x{off_density:04X}]: 0x{dens_antiga:02X} -> 0x{NOVA_DENSIDADE:02X}")
        print(f"  - ucMemorySize [0x{off_memsize:04X}]: 0x{size_antigo:02X} ({size_antigo*64} MB) -> 0x{NOVO_MEMORY_SIZE:02X} ({NOVO_MEMORY_SIZE*64} MB)")

    # 2. Recálculo do Checksum de 8 bits da ROM (padrão PCI / AtomBIOS)
    offset_checksum = 0xFFFE
    rom[offset_checksum] = 0x00
    soma_atual = sum(rom) % 256
    byte_correcao = (256 - soma_atual) % 256
    rom[offset_checksum] = byte_correcao

    # Verificação final de integridade
    checksum_final = sum(rom) % 256
    print(f"\n[OK] Checksum recalculado (offset 0x{offset_checksum:04X} = 0x{byte_correcao:02X}). Soma mod 256 = 0x{checksum_final:02X}")

    with open(ARQUIVO_MODIFICADO, "wb") as f:
        f.write(rom)

    print(f"[SUCESSO] Novo arquivo gerado com 64 KB em:\n  {ARQUIVO_MODIFICADO}")

if __name__ == "__main__":
    patch_vbios()
