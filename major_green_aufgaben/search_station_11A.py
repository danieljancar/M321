import scanner
import energy
import navigation
import time
import json
from datetime import datetime


def systematic_search_for_station(target_name, search_range=50000, grid_spacing=8000):
    """
    Systematically search for a stationary station using a grid pattern
    """
    print(f"Starting systematic search for {target_name}")
    print(f"Search range: ±{search_range}, Grid spacing: {grid_spacing}")
    
    # Create search grid
    search_points = []
    for x in range(-search_range, search_range + 1, grid_spacing):
        for y in range(-search_range, search_range + 1, grid_spacing):
            search_points.append((x, y))
    
    print(f"Generated {len(search_points)} search points")
    
    for i, (x, y) in enumerate(search_points):
        print(f"Searching point {i+1}/{len(search_points)}: ({x}, {y})")
        
        # Travel to search point
        navigation.travel_position_until_recive(x, y)
        
        # Scan multiple times at this position to be thorough
        for scan_attempt in range(3):
            scan_result = scanner.scan()
            if scan_result:
                for obj in scan_result:
                    if obj.get("name") == target_name:
                        station_pos = obj.get("pos", {})
                        station_x, station_y = station_pos.get("x"), station_pos.get("y")
                        
                        if station_x is not None and station_y is not None:
                            print(f"\n🎯 FOUND {target_name}!")
                            print(f"Station Position: x={station_x}, y={station_y}")
                            
                            # Log the discovery
                            log_station_discovery(target_name, station_x, station_y, obj)
                            
                            # Travel to the station and halt there
                            print(f"Traveling to {target_name}...")
                            navigation.travel_position_until_recive(station_x, station_y)
                            
                            print(f"✅ Successfully reached {target_name}")
                            print("🛑 MISSION COMPLETE - Halting at station")
                            return True
            
            time.sleep(1)  # Brief pause between scans
        
        time.sleep(0.5)  # Brief pause before moving to next point
    
    print(f"❌ Search completed - {target_name} not found in specified range")
    return False


def expanding_search_from_last_known(target_name, last_known_x=-24900, last_known_y=13800):
    """
    Search in expanding rings from the last known position
    Since the station has moved from its last known location, search outward
    """
    print(f"Starting expanding search from last known position: ({last_known_x}, {last_known_y})")
    print("Station is confirmed to have moved from this location")
    
    import math
    
    # Start with small radius and expand outward
    for radius in [2000, 4000, 6000, 8000, 10000, 15000, 20000, 25000, 30000]:
        print(f"\n🔍 Searching radius {radius} units from last known position...")
        
        # Calculate number of points based on radius to ensure good coverage
        # More points for larger radii to maintain good coverage
        num_points = max(8, radius // 2000)  # At least 8 points, more for larger radii
        
        search_points = []
        for i in range(num_points):
            angle = (360 / num_points) * i
            offset_x = last_known_x + radius * math.cos(math.radians(angle))
            offset_y = last_known_y + radius * math.sin(math.radians(angle))
            search_points.append((int(offset_x), int(offset_y)))
        
        print(f"  Checking {len(search_points)} points at radius {radius}")
        
        for i, (x, y) in enumerate(search_points):
            print(f"    Point {i+1}/{len(search_points)}: ({x}, {y})")
            navigation.travel_position_until_recive(x, y)
            
            # Scan multiple times at each point
            for scan_attempt in range(2):
                scan_result = scanner.scan()
                if scan_result:
                    for obj in scan_result:
                        if obj.get("name") == target_name:
                            station_pos = obj.get("pos", {})
                            station_x, station_y = station_pos.get("x"), station_pos.get("y")
                            
                            if station_x is not None and station_y is not None:
                                distance_moved = math.sqrt((station_x - last_known_x)**2 + (station_y - last_known_y)**2)
                                print(f"\n🎯 FOUND {target_name}!")
                                print(f"New Position: x={station_x}, y={station_y}")
                                print(f"Distance moved from last known: {distance_moved:.0f} units")
                                
                                # Log the discovery with movement info
                                log_station_discovery(target_name, station_x, station_y, obj, 
                                                    last_known_pos=(last_known_x, last_known_y),
                                                    distance_moved=distance_moved)
                                
                                # Travel to the station and halt there
                                print(f"Traveling to {target_name}...")
                                navigation.travel_position_until_recive(station_x, station_y)
                                
                                print(f"✅ Successfully reached {target_name}")
                                print("🛑 MISSION COMPLETE - Halting at station")
                                return True
                
                time.sleep(0.5)
            
            time.sleep(0.3)  # Brief pause between search points
    
    print(f"❌ {target_name} not found within 30,000 units of last known position")
    return False


def log_station_discovery(station_name, x, y, full_data, last_known_pos=None, distance_moved=None):
    """
    Log the station discovery to a file with timestamp and movement info
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "station_name": station_name,
        "position": {"x": x, "y": y},
        "full_scan_data": full_data
    }
    
    if last_known_pos and distance_moved:
        log_entry["movement_info"] = {
            "last_known_position": {"x": last_known_pos[0], "y": last_known_pos[1]},
            "distance_moved": distance_moved,
            "movement_confirmed": True
        }
    
    filename = f"{station_name.replace(' ', '_').replace('-', '_').lower()}_discovery.json"
    
    try:
        with open(filename, "w") as f:
            json.dump(log_entry, f, indent=2)
        print(f"📝 Station discovery logged to: {filename}")
        if distance_moved:
            print(f"📝 Movement data: Station moved {distance_moved:.0f} units from last known position")
    except Exception as e:
        print(f"❌ Error logging discovery: {e}")
        # Fallback - print to console
        print(f"📝 DISCOVERY LOG: {log_entry}")


def search_station_11a():
    """
    Main function to search for Station 11-A starting from last known position
    """
    target_station = "Station 11-A"
    last_known_x, last_known_y = -24900, 13800
    
    print(f"🔍 Starting search mission for {target_station}")
    print(f"📍 Last known position: ({last_known_x}, {last_known_y}) - Station confirmed to have moved")
    print("=" * 70)
    
    energy.set_limit_normal()
    
    # Start expanding search from last known position
    print("🎯 Strategy: Expanding search from last known position...")
    found = expanding_search_from_last_known(target_station, last_known_x, last_known_y)
    
    if not found:
        print("\n🔄 Expanding search didn't find station, trying systematic grid search...")
        # If expanding search fails, fall back to systematic search
        found = systematic_search_for_station(target_station, search_range=40000, grid_spacing=10000)
    
    if not found:
        print(f"\n❌ {target_station} not found after complete search")
        print("Consider expanding search range or checking if station name changed")
    
    return found


if __name__ == "__main__":
    try:
        search_station_11a()
    except KeyboardInterrupt:
        print("\n🛑 Search interrupted by user")
        print("Current position maintained")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("Search terminated")
