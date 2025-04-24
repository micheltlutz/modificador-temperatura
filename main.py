import argparse
import re
import os

def modificar_gcode(input_path, output_path, temp_inicial=240, temp_final=190, step_mm=5.0):
    with open(input_path, 'r') as file:
        linhas = file.readlines()

    nova_temperatura = temp_inicial
    decremento = (temp_inicial - temp_final) / ((temp_inicial - temp_final) // (step_mm or 1))
    proxima_altura_alvo = step_mm

    nova_linha_gcode = []

    for linha in linhas:
        nova_linha_gcode.append(linha)
        match = re.search(r'G1\s[^;]*Z([\d\.]+)', linha)
        if match:
            z_atual = float(match.group(1))
            if z_atual >= proxima_altura_alvo:
                nova_temperatura = max(temp_final, nova_temperatura - decremento)
                nova_linha_gcode.append(f"; ===== ALTERANDO PARA {int(nova_temperatura)}C =====\n")
                nova_linha_gcode.append(f"M109 S{int(nova_temperatura)}\n")
                proxima_altura_alvo += step_mm

    with open(output_path, 'w') as file:
        file.writelines(nova_linha_gcode)

    print(f"✔ Arquivo modificado salvo em: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modificar todos G-codes em input_gcode/ e salvar em output_gcodes/")
    parser.add_argument("--temp_inicial", type=int, default=240, help="Temperatura inicial (default: 240)")
    parser.add_argument("--temp_final", type=int, default=190, help="Temperatura final (default: 190)")
    parser.add_argument("--step_mm", type=float, default=5.0, help="Altura entre alterações de temperatura em mm (default: 5.0)")

    args = parser.parse_args()

    input_dir = "input_gcode"
    output_dir = "output_gcodes"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".gcode"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"mod_{filename}")
            modificar_gcode(input_path, output_path, args.temp_inicial, args.temp_final, args.step_mm)
