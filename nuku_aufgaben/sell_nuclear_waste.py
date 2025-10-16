import navigation
import energy
import communication as comm
import cargo_hold as cargo
import time


def sell_all_nuclear_waste():
    """
    Travel to Nuku station and sell all nuclear waste (W) from inventory
    """
    nuku_x = -96486
    nuku_y = -80625
    nuku_station = "Nuku Station"
    nuclear_waste_code = "W"
    
    print("🚀 NUCLEAR WASTE SELLING MISSION")
    print(f"Target: {nuku_station}")
    print(f"Coordinates: ({nuku_x}, {nuku_y})")
    print(f"Selling: Nuclear Waste ({nuclear_waste_code})")
    print("=" * 50)
    
    # Set energy to normal
    energy.set_limit_normal()
    
    # Check current inventory first
    print("📦 Checking current inventory...")
    cargo_data = cargo.get_cargo_hold()
    
    if "error" in cargo_data:
        print(f"❌ Error getting cargo data: {cargo_data['error']}")
        return False
    
    resources = cargo_data["hold"]["resources"]
    nuclear_waste_amount = resources.get(nuclear_waste_code, 0)
    
    print(f"📊 Current Nuclear Waste in inventory: {nuclear_waste_amount}")
    
    if nuclear_waste_amount <= 0:
        print("ℹ️  No nuclear waste to sell!")
        return True
    
    print(f"💰 Will sell {nuclear_waste_amount} units of nuclear waste")
    
    # Travel to Nuku station
    print(f"\n🚀 Traveling to {nuku_station}...")
    navigation.travel_position_until_recive(nuku_x, nuku_y)
    
    # Wait a moment to ensure we're properly positioned
    time.sleep(1)
    
    # Check if we're at a station
    print("🔍 Checking for nearby stations...")
    stations_response = comm.get_near_station()
    
    if stations_response.status_code != 200:
        print(f"❌ Error getting station info: {stations_response.status_code}")
        return False
    
    stations_data = stations_response.json()
    available_stations = stations_data.get("stations", {})
    
    if not available_stations:
        print("❌ No stations in reach! Check coordinates.")
        return False
    
    # Find Nuku station or use the first available station
    station_name = None
    for station in available_stations.keys():
        if "nuku" in station.lower() or "Nuku" in station:
            station_name = station
            break
    
    if not station_name:
        # Use first available station if Nuku not found by name
        station_name = list(available_stations.keys())[0]
        print(f"⚠️  Using available station: {station_name}")
    else:
        print(f"✅ Found {station_name}")
    
    # Sell all nuclear waste
    print(f"\n💰 Selling {nuclear_waste_amount} units of nuclear waste...")
    
    try:
        sell_response = comm.sell(station_name, nuclear_waste_code, nuclear_waste_amount)
        
        if sell_response.status_code == 200:
            print(f"✅ Successfully sold {nuclear_waste_amount} units of nuclear waste!")
            
            # Check updated inventory
            updated_cargo = cargo.get_cargo_hold()
            if "error" not in updated_cargo:
                credits = updated_cargo["hold"]["credits"]
                remaining_waste = updated_cargo["hold"]["resources"].get(nuclear_waste_code, 0)
                print(f"💰 Current credits: {credits}")
                print(f"📦 Remaining nuclear waste: {remaining_waste}")
            
            print("🎉 MISSION COMPLETE!")
            return True
        else:
            print(f"❌ Failed to sell nuclear waste. Status: {sell_response.status_code}")
            print(f"Response: {sell_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during sale: {e}")
        return False


def display_cargo_before_and_after():
    """
    Display cargo information before starting mission
    """
    print("📦 CURRENT CARGO STATUS:")
    cargo.display_cargo_hold()
    print()


if __name__ == "__main__":
    try:
        # Show current cargo status
        display_cargo_before_and_after()
        
        # Execute the selling mission
        success = sell_all_nuclear_waste()
        
        if success:
            print("\n✅ Nuclear waste selling mission completed successfully!")
        else:
            print("\n❌ Nuclear waste selling mission failed!")
            
    except KeyboardInterrupt:
        print("\n🛑 Mission interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")