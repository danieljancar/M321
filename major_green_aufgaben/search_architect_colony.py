import navigation
import energy
import json
import scanner
import time
from datetime import datetime


def fly_lane_with_continuous_scan(x, start_y, end_y, target_name):
    """
    Fly along a lane from start_y to end_y at fixed x coordinate
    Continuously scan while flying - no stopping
    Returns True if target is found, False otherwise
    """
    print(f"� Flying lane at x={x} from y={start_y} to y={end_y}")
    
    # Start flying to the beginning of the lane
    navigation.travel_position(x, start_y)
    
    # Wait until we reach the start position
    while not navigation.recived_position(x, start_y):
        # Scan while traveling to start position
        scan_result = scanner.scan()
        if scan_result:
            found = check_scan_results(scan_result, target_name)
            if found:
                return True
        time.sleep(0.2)
    
    print(f"✅ Reached lane start, now flying to end y={end_y}")
    
    # Now fly along the lane to the end while continuously scanning
    navigation.travel_position(x, end_y)
    
    # Continuously scan while flying the lane
    while not navigation.recived_position(x, end_y):
        scan_result = scanner.scan()
        if scan_result:
            found = check_scan_results(scan_result, target_name)
            if found:
                return True
        time.sleep(0.2)  # Quick scans while flying
    
    print(f"✅ Completed lane at x={x}")
    return False


def check_scan_results(scan_result, target_name):
    """
    Check scan results for the target colony
    Returns True if found and handles colony travel, False otherwise
    """
    for obj in scan_result:
        obj_name = obj.get("name", "")
        
        # Check for exact match
        if obj_name == target_name:
            pos = obj.get("pos", {})
            colony_x, colony_y = pos.get("x"), pos.get("y")
            
            if colony_x is not None and colony_y is not None:
                current_pos = navigation.get_position().json()["pos"]
                print(f"\n🎯 FOUND {target_name}!")
                print(f"📍 Colony Position: x={colony_x}, y={colony_y}")
                print(f"📍 Current Position: x={current_pos['x']}, y={current_pos['y']}")
                
                # Log the discovery
                log_colony_discovery(target_name, colony_x, colony_y, obj, current_pos['x'], current_pos['y'])
                
                # Travel to the colony
                print(f"🚀 Traveling to {target_name}...")
                navigation.travel_position_until_recive(colony_x, colony_y)
                
                print(f"✅ Reached {target_name}")
                print("🛑 MISSION COMPLETE - Colony found and reached!")
                return True
        
        # Also log any other interesting objects in the area
        elif obj_name and "colony" in obj_name.lower():
            current_pos = navigation.get_position().json()["pos"]
            print(f"   ℹ️  Found related object: {obj_name}")
            log_other_discovery(obj_name, obj, current_pos['x'], current_pos['y'])
    
    return False


def systematic_search_architect_colony():
    """
    Continuously fly through the search area with systematic pattern while scanning
    Search area: X from -112000 to -48000, Y from -112000 to -48000
    No stopping at points - just continuous flight and scanning
    """
    target_name = "Architect Colony"
    center_x = -80000
    center_y = -80000
    search_range = 32000
    
    start_x = center_x - search_range  # -112000
    end_x = center_x + search_range    # -48000
    start_y = center_y - search_range  # -112000
    end_y = center_y + search_range    # -48000
    
    lane_width = 3000  # 3km between flight lanes for good scanner coverage
    
    print(f"🔍 Starting continuous flight search for '{target_name}'")
    print(f"📍 Search center: ({center_x}, {center_y})")
    print(f"📏 Search range: ±{search_range} units")
    print(f"🗺️  Search area: X[{start_x} to {end_x}], Y[{start_y} to {end_y}]")
    print(f"✈️  Lane width: {lane_width} units")
    print("🔄 Mode: Continuous flight with scanning")
    print("=" * 70)
    
    # Calculate flight lanes
    total_lanes = int((end_x - start_x) / lane_width) + 1
    print(f"📊 Total flight lanes: {total_lanes}")
    print("🚀 Starting continuous search flight...\n")
    
    lane_count = 0
    
    # Fly in systematic lanes (snake pattern)
    x = start_x
    while x <= end_x:
        lane_count += 1
        progress = (lane_count / total_lanes) * 100
        
        print(f"✈️  Flying lane {lane_count}/{total_lanes} ({progress:.1f}%) at x={x}")
        
        if lane_count % 2 == 1:
            # Odd lanes: fly south to north
            flight_start_y, flight_end_y = start_y, end_y
        else:
            # Even lanes: fly north to south (snake pattern)
            flight_start_y, flight_end_y = end_y, start_y
        
        # Start continuous flight and scanning for this lane
        found_colony = fly_lane_with_continuous_scan(x, flight_start_y, flight_end_y, target_name)
        if found_colony:
            return True
        
        x += lane_width
        print(f"📈 Completed lane at x={x-lane_width}, moving to next lane...")
    
    print(f"\n❌ Search completed - '{target_name}' not found in specified area")
    print(f"📊 Flew {total_lanes} lanes covering area ({start_x},{start_y}) to ({end_x},{end_y})")
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
    Main mission to find the Architect Colony with continuous flight scanning
    """
    print("🚀 ARCHITECT COLONY CONTINUOUS FLIGHT SEARCH")
    print("Target: 'Architect Colony'")
    print("Area: (-80000, -80000) ±32000")
    print("Mode: Continuous flight with scanning - no stopping!")
    print("=" * 60)
    
    energy.set_limit_normal()
    
    try:
        # Start continuous flight search
        found = systematic_search_architect_colony()
        
        if found:
            print(f"\n✅ SUCCESS! Colony found and reached!")
            return True
        else:
            print(f"\n❌ Colony not found in search area")
            print("� Consider expanding search range or checking colony name")
            
    except Exception as e:
        print(f"\n⚠️  Error during search: {e}")
        print("Search terminated")
    
    return False


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