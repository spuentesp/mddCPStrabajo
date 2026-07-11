#!/usr/bin/env python3
"""Emula el formulario 'Apply Rules' de aomdd4cps: inyecta en el CIM de SVIF
los parametros del disenador documentados en actividad-mdd4cps.md, con el
formato exacto (JSON HTML-escapado) que espera el XSLT CIM-PIM.xsl."""
import json, re, sys

def esc(obj):
    return json.dumps(obj, ensure_ascii=False).replace('"', "&quot;")

def field(name, desc):
    return {"name": name, "description": desc}

# --- Parametros del disenador (actividad seccion 1.1) ---
GOALS = {
    "cim-g1": 500,   # Monitorear presencia de personas (percepcion 2 Hz)
    "cim-g2": 250,   # Controlar acceso al recinto (actuacion mas reactiva)
}
TASKS = {  # id: (input_parameters, output_parameters)
    "cim-t1":  ([], [field("frame", "Cuadro capturado por la camara.")]),
    "cim-t2":  ([field("frame", "Cuadro capturado por la camara.")],
                [field("face", "Region de rostro detectada.")]),
    "cim-t3":  ([field("frame", "Cuadro capturado por la camara.")],
                [field("identification_event", "Evento de identificacion resultante.")]),
    "cim-t4":  ([field("face", "Region de rostro detectada.")],
                [field("match", "Coincidencia con la base de enrolados.")]),
    "cim-t5":  ([field("identification_event", "Evento de identificacion a publicar.")], []),
    "cim-t6":  ([field("identification_event", "Evento de identificacion recibido.")],
                [field("decision", "Decision de autorizacion.")]),
    "cim-t7":  ([field("decision", "Decision de autorizacion.")], []),
    "cim-t8":  ([], []),   # Desbloquear cerradura (rama OR)
    "cim-t9":  ([], []),   # Activar alarma (rama OR)
    "cim-t10": ([field("access_event", "Evento de acceso a registrar.")], []),
}
SW_RESOURCES = {  # resource_type software + data_structure
    "cim-r2": [field("person_id", "Identificador del enrolado."),
               field("person_name", "Nombre del enrolado."),
               field("face_template", "Plantilla biometrica local.")],
    "cim-r5": [field("timestamp", "Marca de tiempo del acceso."),
               field("person_id", "Identificador de la persona."),
               field("decision", "Resultado de la autorizacion.")],
}
HW_RESOURCES = ["cim-r1", "cim-r3", "cim-r4"]  # camara, cerradura, alarma
DEPENDUM = {  # dependum_data_structure (minimizacion: identidad, nunca imagen)
    "cim-d1": 500, "cim-d1-sd": 500,
}
DEPENDUM_FIELDS = [
    field("timestamp", "Marca de tiempo del evento."),
    field("person_id", "Identificador de la persona."),
    field("person_name", "Nombre de la persona."),
    field("confidence", "Confianza de la identificacion."),
    field("authorized", "Indicador de autorizacion."),
]

def add_attrs(xml, obj_id, attrs):
    """Inserta attrs en el tag <object ...> que tenga id=obj_id."""
    pat = re.compile(r'(<object\b)([^>]*?\bid="' + re.escape(obj_id) + r'")')
    inject = "".join(f' {k}="{v}"' for k, v in attrs.items())
    new, n = pat.subn(lambda m: m.group(1) + inject + m.group(2), xml)
    if n == 0:
        print(f"  WARN: id {obj_id} no encontrado", file=sys.stderr)
    return new

# is_a_cpc: marca que agentes SR se vuelven CPS Component (disparador real del XSLT)
CPC_TRUE = ["cim-a1sr-c", "cim-a2sr-c"]                       # Face Monitor / Access Actuator
CPC_FALSE = ["cim-a1", "cim-a1-c", "cim-a2", "cim-a2-c",
             "cim-a1sr", "cim-a2sr", "cim-a3"]                # SD / administrador

def main(src, dst):
    xml = open(src, encoding="utf-8").read()
    for aid in CPC_TRUE:
        xml = add_attrs(xml, aid, {"is_a_cpc": "true"})
    for aid in CPC_FALSE:
        xml = add_attrs(xml, aid, {"is_a_cpc": "false"})
    for gid, ms in GOALS.items():
        xml = add_attrs(xml, gid, {"interval_in_milliseconds": ms,
                                   "operation_modes_enabled": "false"})
    for tid, (ip, op) in TASKS.items():
        xml = add_attrs(xml, tid, {"input_parameters": esc(ip),
                                   "output_parameters": esc(op),
                                   "operation_modes_enabled": "false"})
    for rid, ds in SW_RESOURCES.items():
        xml = add_attrs(xml, rid, {"resource_type": "software",
                                   "data_structure": esc(ds)})
    for rid in HW_RESOURCES:
        xml = add_attrs(xml, rid, {"resource_type": "hardware"})
    for did, ms in DEPENDUM.items():
        xml = add_attrs(xml, did, {"dependum_data_structure": esc(DEPENDUM_FIELDS),
                                   "interval_in_milliseconds": ms,
                                   "operation_modes_enabled": "false"})
    open(dst, "w", encoding="utf-8").write(xml)
    print(f"OK -> {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
