import re
import markdown

def format_perfume_info(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividir el contenido en secciones de perfumes
    perfumes = re.split(r'\n\n+', content.strip())

    formatted_perfumes = []
    seen_perfumes = set()

    for perfume in perfumes:
        lines = perfume.split('\n')
        if len(lines) < 2:
            continue

        marca = lines[0].strip()
        nombre = lines[1].strip()

        # Evitar duplicados
        if (marca, nombre) in seen_perfumes:
            continue
        seen_perfumes.add((marca, nombre))

        formatted_perfume = f"# {marca}\n## {nombre}\n\n"

        # Formatear secciones
        sections = {
            'Infografía': '',
            'Diseño': '',
            'Para': '',
            'Uso': '',
            'Duración': '',
            'Estilo': '',
            'Concentración': '',
            'Texto': ''
        }

        current_section = None
        for line in lines[2:]:
            if line.strip() in sections:
                current_section = line.strip()
                if current_section != 'Texto':
                    formatted_perfume += f"### {current_section}\n"
            elif current_section:
                if current_section == 'Diseño':
                    if 'Codificación de colores por familias olfativas:' in line:
                        formatted_perfume += line + '\n'
                    else:
                        color_match = re.match(r'(\w+): (\w+)', line.strip())
                        if color_match:
                            family, color = color_match.groups()
                            formatted_perfume += f"- {family}: <span style='color: {color.lower()}'>{color}</span>\n"
                elif current_section == 'Texto':
                    if line.startswith('Título:'):
                        formatted_perfume += f"#### {line}\n"
                    elif line.startswith('Descripción:'):
                        formatted_perfume += f"#### {line}\n"
                    elif line.startswith('Llamada a la acción:'):
                        formatted_perfume += f"#### {line}\n"
                        # Verificar y corregir números de WhatsApp
                        whatsapp_numbers = re.findall(r'\((\d{4})\) (\d{6})', line)
                        if len(whatsapp_numbers) == 2:
                            formatted_perfume += f"WhatsApp: (0972) 260891 - (0986) 794774\n"
                        else:
                            formatted_perfume += "WhatsApp: (0972) 260891 - (0986) 794774\n"
                else:
                    formatted_perfume += line + '\n'

        formatted_perfumes.append(formatted_perfume)

    # Escribir el resultado en formato Markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(formatted_perfumes))

    print(f"Archivo formateado guardado como {output_file}")

# Uso del script
input_file = 'perfumes.txt'
output_file = 'perfumes_formateados.md'
format_perfume_info(input_file, output_file)
