#!/usr/bin/env python3
"""Emula el formulario PIM->PSM: inyecta tipado concreto (input_parameters_psm,
output_parameters_psm, data_structure_psm) y descripciones de integracion HW
en el PIM app-generado de SVIF, con los tipos de la actividad (seccion 1.2)."""
import json, re, sys, html

# name -> tipo concreto C++ (actividad 1.2: unsigned long, char[32], float, bool)
TYPE_MAP = {
    "timestamp": "unsigned long", "person_id": "char[32]", "person_name": "char[32]",
    "confidence": "float", "authorized": "bool", "decision": "bool", "match": "bool",
    "face_template": "char[64]", "frame": "uint8_t*", "face": "uint8_t*",
    "identification_event": "IdentificationEvent", "access_event": "AccessLogEntry",
}
DEFAULT_TYPE = "int"

# integration_operation_description por hw_resource (id_cim_parent -> pin/wiring)
HW_INTEGRATION = {
    "cim-r1": "Camara OV2640 conectada por interfaz paralela DVP al ESP32-CAM.",
    "cim-r3": "Cerradura electromecanica controlada por rele en RELAY_PIN (salida digital).",
    "cim-r4": "Alarma sonora (buzzer) controlada por BUZZER_PIN (salida digital).",
}

def unesc(s): return html.unescape(s)
def esc(obj): return json.dumps(obj, ensure_ascii=False).replace('"', "&quot;")

def typed(json_escaped):
    """Toma un array JSON escapado de {name,description} y agrega type a cada uno."""
    arr = json.loads(unesc(json_escaped))
    for f in arr:
        f["type"] = TYPE_MAP.get(f["name"], DEFAULT_TYPE)
    return esc(arr)

def process_object(tag):
    """Dado un <object ...> tag completo, agrega los atributos _psm derivados."""
    add = {}
    for base, psm in [("input_parameters", "input_parameters_psm"),
                      ("output_parameters", "output_parameters_psm"),
                      ("data_structure", "data_structure_psm"),
                      ("dependum_data_structure", "dependum_data_structure_psm")]:
        m = re.search(base + r'="([^"]*)"', tag)
        if m:
            add[psm] = typed(m.group(1))
    m = re.search(r'id_cim_parent="([^"]*)"', tag)
    if m and m.group(1) in HW_INTEGRATION:
        add["integration_operation_description"] = HW_INTEGRATION[m.group(1)]
    if not add:
        return tag
    inject = "".join(f' {k}="{v}"' for k, v in add.items())
    return tag[:len("<object")] + inject + tag[len("<object"):]

def main(src, dst):
    xml = open(src, encoding="utf-8").read()
    out = re.sub(r'<object\b[^>]*>', lambda m: process_object(m.group(0)), xml)
    open(dst, "w", encoding="utf-8").write(out)
    print(f"OK -> {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
