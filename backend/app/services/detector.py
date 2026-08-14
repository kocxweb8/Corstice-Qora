def detect_objects(entities):
    objects = []
    walls = []
    doors = []
    windows = []
    texts = []
    
    for ent in entities:
        layer = ent.get("layer", "").upper()
        etype = ent.get("type")
        if "WALL" in layer and etype in ["line", "polyline"]:
            walls.append(ent)
        elif "DOOR" in layer or (ent.get("properties", {}).get("block_name", "").startswith("D")):
            doors.append(ent)
        elif "WINDOW" in layer or ent.get("properties", {}).get("block_name", "").startswith("W"):
            windows.append(ent)
        elif etype == "text":
            texts.append(ent)
    
    # Build detected objects list
    for w in walls:
        objects.append({
            "type": "wall",
            "confidence": 0.95,
            "geometry": w.get("geometry", {}),
            "properties": {"layer": w.get("layer")}
        })
    for d in doors:
        objects.append({
            "type": "door",
            "confidence": 0.95,
            "geometry": d.get("geometry", {}),
            "properties": {"layer": d.get("layer"), "block": d.get("properties", {}).get("block_name")}
        })
    for win in windows:
        objects.append({
            "type": "window",
            "confidence": 0.95,
            "geometry": win.get("geometry", {}),
            "properties": {"layer": win.get("layer"), "block": win.get("properties", {}).get("block_name")}
        })
    # Room detection: look for closed polylines with text inside (simplified)
    # For MVP, we skip complex room detection and just return walls, doors, windows
    return objects