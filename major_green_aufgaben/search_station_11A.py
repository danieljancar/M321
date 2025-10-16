import scanner
import energy
import navigation
import time
import json
import math
from datetime import datetime


def follow_moving_station(target_name, initial_x, initial_y):
    """
    Continuously follow a moving station once it's been found
    Similar to following Captain Morris - tracks and follows the station
    """
    print(f"🎯 Starting continuous tracking of {target_name}")
    print(f"Initial position: ({initial_x}, {initial_y})")
    print("📝 Logging all position updates...")
    
    # Travel to initial position first
    navigation.travel_position_until_recive(initial_x, initial_y)
    print(f"✅ Reached initial position of {target_name}")
    
    position_log = []
    last_logged_time = time.time()
    
    while True:
        scan_result = scanner.scan()
        if scan_result:
            station_found = False
            
            for obj in scan_result:
                if obj.get("name") == target_name:
                    station_pos = obj.get("pos", {})
                    current_x, current_y = station_pos.get("x"), station_pos.get("y")
                    
                    if current_x is not None and current_y is not None:
                        station_found = True
                        current_time = time.time()
                        
                        print(f"📍 {target_name} tracked at: x={current_x}, y={current_y}")
                        
                        # Log position every 30 seconds or significant movement
                        if (current_time - last_logged_time > 30 or 
                            not position_log or 
                            abs(current_x - position_log[-1]["x"]) > 100 or 
                            abs(current_y - position_log[-1]["y"]) > 100):
                            
                            position_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "x": current_x,
                                "y": current_y,
                                "time_since_start": current_time - time.time()
                            }
                            position_log.append(position_entry)
                            last_logged_time = current_time
                            
                            # Save tracking log periodically
                            log_tracking_data(target_name, position_log)
                        
                        # Follow the station
                        navigation.travel_position(current_x, current_y)
                        time.sleep(0.5)
                        break
            
            if not station_found:
                print(f"⚠️  Lost track of {target_name}! Performing local search...")
                
                # Get current position and search around it
                current_pos = navigation.get_position().json()["pos"]
                found_again = local_search_for_moving_station(target_name, 
                                                            current_pos["x"], 
                                                            current_pos["y"])
                
                if not found_again:
                    print(f"❌ Unable to relocate {target_name}")
                    print("💾 Saving final tracking log...")
                    log_tracking_data(target_name, position_log, final=True)
                    return False
        
        time.sleep(0.5)


def local_search_for_moving_station(target_name, center_x, center_y, search_radius=3000):
    """
    Search in a small area around the last known position when station is lost
    """
    print(f"🔍 Local search for {target_name} around ({center_x}, {center_y})")
    
    import math
    
    # Search in 8 directions around the last known position
    for angle in range(0, 360, 45):
        for radius in [1000, 2000, 3000]:
            search_x = center_x + radius * math.cos(math.radians(angle))
            search_y = center_y + radius * math.sin(math.radians(angle))
            
            print(f"  Checking: ({int(search_x)}, {int(search_y)})")
            navigation.travel_position_until_recive(int(search_x), int(search_y))
            
            scan_result = scanner.scan()
            if scan_result:
                for obj in scan_result:
                    if obj.get("name") == target_name:
                        station_pos = obj.get("pos", {})
                        found_x, found_y = station_pos.get("x"), station_pos.get("y")
                        
                        if found_x is not None and found_y is not None:
                            print(f"🎯 Relocated {target_name} at: ({found_x}, {found_y})")
                            return True
            
            time.sleep(0.3)
    
    return False


def log_tracking_data(station_name, position_log, final=False):
    """
    Log the continuous tracking data of the moving station
    """
    log_data = {
        "station_name": station_name,
        "tracking_session": {
            "start_time": position_log[0]["timestamp"] if position_log else datetime.now().isoformat(),
            "last_update": position_log[-1]["timestamp"] if position_log else datetime.now().isoformat(),
            "total_positions": len(position_log),
            "session_complete": final
        },
        "position_history": position_log
    }
    
    if len(position_log) >= 2:
        # Calculate movement statistics
        start_pos = position_log[0]
        end_pos = position_log[-1]
        total_distance = math.sqrt((end_pos["x"] - start_pos["x"])**2 + (end_pos["y"] - start_pos["y"])**2)
        
        log_data["movement_analysis"] = {
            "start_position": {"x": start_pos["x"], "y": start_pos["y"]},
            "current_position": {"x": end_pos["x"], "y": end_pos["y"]},
            "total_distance_traveled": total_distance,
            "tracking_duration_minutes": len(position_log) * 0.5  # Approximate
        }
    
    filename = f"{station_name.replace(' ', '_').replace('-', '_').lower()}_tracking_log.json"
    
    try:
        with open(filename, "w") as f:
            json.dump(log_data, f, indent=2)
        
        status = "FINAL" if final else "UPDATE"
        print(f"📝 {status} tracking log saved to: {filename}")
        
        if len(position_log) >= 2 and "movement_analysis" in log_data:
            analysis = log_data["movement_analysis"]
            print(f"📊 Movement: {analysis['total_distance_traveled']:.0f} units over {analysis['tracking_duration_minutes']:.1f} minutes")
            
    except Exception as e:
        print(f"❌ Error saving tracking log: {e}")


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
    
    Reference: Station 5-A moved ~6,900 units from (15400, -11200) to (8760, -9308)
    So we should search in expanding rings up to at least 10,000+ units
    
    PRIORITY: Station was seen moving towards upper-left (negative X, positive Y)
    """
    print(f"Starting expanding search from last known position: ({last_known_x}, {last_known_y})")
    print("Station is confirmed to have moved from this location")
    print("📊 Reference: Station 5-A moved ~6,900 units from its last known position")
    print("🎯 PRIORITY SEARCH: Upper-left direction (negative X, positive Y) - station seen moving that way")
    
    import math
    
    # Based on Station 5A data, search in expanding rings up to 15km+ to be safe
    # Station 5A moved ~6.9km, so Station 11-A could be similar distance or further
    # PRIORITY: Search upper-left quadrant first where station was seen moving
    radii = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000, 15000, 20000, 25000]
    
    for radius in radii:
        print(f"\n🔍 Searching radius {radius} units from last known position...")
        print(f"   (Station 5-A reference: moved ~6,900 units)")
        print(f"   🎯 PRIORITY: Upper-left quadrant first")
        
        # Generate search points with PRIORITY for upper-left quadrant
        search_points = []
        
        if radius <= 10000:
            # For smaller radii, focus heavily on upper-left quadrant
            num_points = 16
            
            # Generate points with bias towards upper-left
            for i in range(num_points):
                angle = (360 / num_points) * i
                
                # Add extra points in upper-left quadrant (135° to 315°, but prioritize 135° to 225°)
                if 135 <= angle <= 225:  # Upper-left quadrant priority
                    # Add this point and an extra point nearby
                    offset_x = last_known_x + radius * math.cos(math.radians(angle))
                    offset_y = last_known_y + radius * math.sin(math.radians(angle))
                    search_points.append((int(offset_x), int(offset_y)))
                    
                    # Add extra point in this quadrant
                    extra_angle = angle + 15  # Small offset for better coverage
                    extra_x = last_known_x + radius * math.cos(math.radians(extra_angle))
                    extra_y = last_known_y + radius * math.sin(math.radians(extra_angle))
                    search_points.append((int(extra_x), int(extra_y)))
                else:
                    # Regular points for other directions
                    offset_x = last_known_x + radius * math.cos(math.radians(angle))
                    offset_y = last_known_y + radius * math.sin(math.radians(angle))
                    search_points.append((int(offset_x), int(offset_y)))
        else:
            # For larger radii, comprehensive coverage
            num_points = max(20, radius // 1500)
            for i in range(num_points):
                angle = (360 / num_points) * i
                offset_x = last_known_x + radius * math.cos(math.radians(angle))
                offset_y = last_known_y + radius * math.sin(math.radians(angle))
                search_points.append((int(offset_x), int(offset_y)))
        
        # Sort search points to prioritize upper-left quadrant
        def priority_sort(point):
            x, y = point
            # Calculate angle from last known position
            angle = math.degrees(math.atan2(y - last_known_y, x - last_known_x))
            if angle < 0:
                angle += 360
            
            # Priority order: upper-left (135-225°) gets priority 0, others get priority 1+
            if 135 <= angle <= 225:
                return 0  # Highest priority
            elif 90 <= angle < 135 or 225 < angle <= 270:
                return 1  # Medium priority  
            else:
                return 2  # Lower priority
        
        search_points.sort(key=priority_sort)
        
        print(f"  Checking {len(search_points)} points at radius {radius} (upper-left prioritized)")
        
        for i, (x, y) in enumerate(search_points):
            # Calculate direction for display
            dx = x - last_known_x
            dy = y - last_known_y
            if dx < 0 and dy > 0:
                direction = "🎯 PRIORITY"
            elif dx < 0:
                direction = "⬅️ LEFT"  
            elif dy > 0:
                direction = "⬆️ UP"
            else:
                direction = "➡️ OTHER"
                
            print(f"    Point {i+1}/{len(search_points)}: ({x}, {y}) {direction}")
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
                                print(f"Current Position: x={station_x}, y={station_y}")
                                print(f"Distance moved from last known: {distance_moved:.0f} units")
                                print(f"📊 Comparison: Station 5-A moved ~6,900 units, this station moved {distance_moved:.0f} units")
                                print(f"⚠️  {target_name} is MOVING - Starting continuous tracking IMMEDIATELY...")
                                
                                # Log the discovery with movement info
                                log_station_discovery(target_name, station_x, station_y, obj, 
                                                    last_known_pos=(last_known_x, last_known_y),
                                                    distance_moved=distance_moved)
                                
                                # Start continuous following mode IMMEDIATELY
                                print(f"🔄 Switching to continuous following mode for {target_name}")
                                return follow_moving_station(target_name, station_x, station_y)
                
                time.sleep(0.5)
            
            time.sleep(0.3)  # Brief pause between search points
    
    print(f"❌ {target_name} not found within 25,000 units of last known position")
    print("💡 Consider: Station might have moved further than Station 5-A's ~6,900 units")
    print("💡 Try searching further in upper-left direction where it was last seen moving")
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
    Main function to search for and continuously track moving Station 11-A
    Station 11-A has moved from its last known position and continues to move
    """
    target_station = "Station 11-A"
    last_known_x, last_known_y = -24900, 13800
    
    print(f"🔍 Starting search and tracking mission for {target_station}")
    print(f"📍 Last known position: ({last_known_x}, {last_known_y}) - Station confirmed to have moved")
    print("⚠️  Station is MOVING and requires continuous tracking once found")
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

# FOUND AND HALTED AT -24311.0/14624.0