import ezdxf
import math

def parse_dxf(filepath):
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()
    entities = []
    
    for e in msp:
        dxftype = e.dxftype()
        layer = e.dxf.layer
        if dxftype == "LINE":
            start = (e.dxf.start.x, e.dxf.start.y)
            end = (e.dxf.end.x, e.dxf.end.y)
            length = math.hypot(end[0]-start[0], end[1]-start[1])
            entities.append({
                "type": "line",
                "layer": layer,
                "geometry": {"start": start, "end": end, "length": length},
                "properties": {}
            })
        elif dxftype == "INSERT":
            # Block reference
            name = e.dxf.name
            insert = (e.dxf.insert.x, e.dxf.insert.y)
            entities.append({
                "type": "block",
                "layer": layer,
                "geometry": {"insert": insert},
                "properties": {"block_name": name}
            })
        elif dxftype == "TEXT" or dxftype == "MTEXT":
            text = e.dxf.text if hasattr(e.dxf, 'text') else e.text
            pos = (e.dxf.insert.x, e.dxf.insert.y) if hasattr(e.dxf, 'insert') else (0,0)
            entities.append({
                "type": "text",
                "layer": layer,
                "geometry": {"position": pos},
                "properties": {"content": text}
            })
        elif dxftype == "LWPOLYLINE" or dxftype == "POLYLINE":
            points = list(e.vertices()) if hasattr(e, 'vertices') else list(e.get_points())
            closed = e.closed if hasattr(e, 'closed') else False
            entities.append({
                "type": "polyline",
                "layer": layer,
                "geometry": {"points": points, "closed": closed},
                "properties": {}
            })
    return entities