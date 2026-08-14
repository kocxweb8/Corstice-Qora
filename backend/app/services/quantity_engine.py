import math

def calculate_quantities(detected_objects, default_wall_height=3.0, default_wall_thickness=0.23):
    # Aggregate walls: sum lengths
    wall_length = 0
    for obj in detected_objects:
        if obj.get("type") == "wall":
            geom = obj.get("geometry", {})
            if "length" in geom:
                wall_length += geom["length"] / 1000.0  # convert mm to m
            elif "points" in geom:
                pts = geom["points"]
                # approximate length by summing segments (simplified)
                # ...
                pass
    # For MVP, we use dummy values
    wall_volume = wall_length * default_wall_height * default_wall_thickness  # m3
    floor_area = 150.0  # dummy
    plaster_area = wall_length * default_wall_height * 2  # both sides
    painting_area = plaster_area + floor_area  # walls + ceiling
    
    # Deductions: assume 2 doors (2 m2 each) and 3 windows (1.5 m2 each)
    door_deduction = 2 * 2.0
    window_deduction = 3 * 1.5
    total_deduction = door_deduction + window_deduction
    # Deduct from plaster and painting
    plaster_net = plaster_area - total_deduction
    painting_net = painting_area - total_deduction
    
    quantities = {
        "walls": {"gross": wall_volume, "deduction": 0, "net": wall_volume, "unit": "m3"},
        "flooring": {"gross": floor_area, "deduction": 0, "net": floor_area, "unit": "m2"},
        "plaster": {"gross": plaster_area, "deduction": total_deduction, "net": plaster_net, "unit": "m2"},
        "painting": {"gross": painting_area, "deduction": total_deduction, "net": painting_net, "unit": "m2"}
    }
    return quantities