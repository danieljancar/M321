import navigation
import energy
import json
import scanner
import time
from datetime import datetime


def systematic_search_architect_colony():
    """
    Systematically search for "Architect Colony" around (-80000, -80000) ±32000
    Search area: X from -112000 to -48000, Y from -112000 to -48000
    """
    target_name = "Architect Colony"
    center_x = -80000
    center_y = -80000
    search_range = 32000
    
    start_x = center_x - search_range  # -112000
    end_x = center_x + search_range    # -48000
    start_y = center_y - search_range  # -112000
    end_y = center_y + search_range    # -48000
    
    step_size = 5000  # 5km grid for good coverage
    
    print(f"🔍 Starting systematic search for '{target_name}'")
    print(f"📍 Search center: ({center_x}, {center_y})")
    print(f"📏 Search range: ±{search_range} units")
    print(f"🗺️  Search area: X[{start_x} to {end_x}], Y[{start_y} to {end_y}]")
    print(f"📐 Grid step size: {step_size} units")
    print("=" * 70)
    
    # Calculate total search points
    x_points = int((end_x - start_x) / step_size) + 1
    y_points = int((end_y - start_y) / step_size) + 1
    total_points = x_points * y_points
    
    print(f"📊 Total search points: {total_points} ({x_points} x {y_points})")
    print("🚀 Starting search...\n")
    
    point_count = 0
    
    # Systematic grid search using alternating direction (snake pattern)
    x = start_x
    while x <= end_x:
        point_count += 1
        
        if (x - start_x) // step_size % 2 == 0:
            # Even columns: bottom to top
            y_start, y_end, y_step = start_y, end_y + step_size, step_size
        else:
            # Odd columns: top to bottom (snake pattern for efficiency)
            y_start, y_end, y_step = end_y, start_y - step_size, -step_size
        
        for y in range(y_start, y_end, y_step):
            point_count += 1
            progress = (point_count / total_points) * 100
            
            print(f"🔍 Point {point_count}/{total_points} ({progress:.1f}%): ({x}, {y})")
            
            # Travel to search point
            navigation.travel_position_until_recive(x, y)
            
            # Scan multiple times at each point for thorough coverage
            for scan_attempt in range(3):
                scan_result = scanner.scan()
                
                if scan_result:
                    for obj in scan_result:
                        obj_name = obj.get("name", "")
                        
                        # Check for exact match
                        if obj_name == target_name:
                            pos = obj.get("pos", {})
                            colony_x, colony_y = pos.get("x"), pos.get("y")
                            
                            if colony_x is not None and colony_y is not None:
                                print(f"\n🎯 FOUND {target_name}!")
                                print(f"📍 Position: x={colony_x}, y={colony_y}")
                                print(f"🎉 SUCCESS! Colony discovered at search point {point_count}/{total_points}")
                                
                                # Log the discovery
                                log_colony_discovery(target_name, colony_x, colony_y, obj, x, y)
                                
                                # Travel to the colony
                                print(f"🚀 Traveling to {target_name}...")
                                navigation.travel_position_until_recive(colony_x, colony_y)
                                
                                print(f"✅ Reached {target_name}")
                                print("🛑 MISSION COMPLETE - Colony found and reached!")
                                return True
                        
                        # Also log any other interesting objects in the area
                        elif obj_name and "colony" in obj_name.lower():
                            print(f"   ℹ️  Found related object: {obj_name}")
                            log_other_discovery(obj_name, obj, x, y)
                
                time.sleep(0.5)  # Brief pause between scans
            
            time.sleep(0.2)  # Brief pause before moving to next point
        
        x += step_size
        print(f"📈 Completed column at x={x-step_size}, moving to next column...")
    
    print(f"\n❌ Search completed - '{target_name}' not found in specified area")
    print(f"📊 Searched {total_points} points in area ({start_x},{start_y}) to ({end_x},{end_y})")
    print("💡 Consider expanding search range or checking colony name")
    return False


def log_colony_discovery(colony_name, x, y, full_data, search_x, search_y):
    """
    Log the colony discovery with detailed information
    """
    discovery_log = {
        "timestamp": datetime.now().isoformat(),
        "colony_name": colony_name,
        "colony_position": {"x": x, "y": y},
        "discovery_location": {"search_x": search_x, "search_y": search_y},
        "full_scan_data": full_data,
        "mission_status": "COLONY_FOUND"
    }
    
    filename = f"{colony_name.replace(' ', '_').lower()}_discovery.json"
    
    try:
        with open(filename, "w") as f:
            json.dump(discovery_log, f, indent=2)
        print(f"📝 Colony discovery logged to: {filename}")
    except Exception as e:
        print(f"❌ Error logging discovery: {e}")
        print(f"📝 DISCOVERY LOG: {discovery_log}")


def log_other_discovery(obj_name, obj_data, search_x, search_y):
    """
    Log other interesting objects found during search
    """
    discovery_entry = {
        "timestamp": datetime.now().isoformat(),
        "object_name": obj_name,
        "search_location": {"x": search_x, "y": search_y},
        "object_data": obj_data
    }
    
    try:
        with open("architect_area_discoveries.json", "a") as f:
            f.write(json.dumps(discovery_entry) + "\n")
    except Exception as e:
        print(f"❌ Error logging other discovery: {e}")


def main_search_mission():
    """
    Main mission to find the Architect Colony
    """
    print("🚀 ARCHITECT COLONY SEARCH MISSION")
    print("Target: 'Architect Colony'")
    print("Area: (-80000, -80000) ±32000")
    print("=" * 50)
    
    energy.set_limit_normal()
    
    # Start systematic search
    found = systematic_search_architect_colony()
    
    if not found:
        print("\n🔄 Colony not found in primary search area")
        print("💭 Consider expanding search or checking alternative coordinates")
    
    return found


if __name__ == "__main__":
    try:
        main_search_mission()
    except KeyboardInterrupt:
        print("\n🛑 Search interrupted by user")
        print("Current position maintained")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("Search terminated")

# im stations.json nach station suchen für cords --> nav.travel_position_until_recive(-108503, -108888)