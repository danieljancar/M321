import navigation
import energy
import communication as comm
import cargo_hold as cargo


def display_all_resources():
    """
    Display all resources in cargo hold to find the exact name for nuclear waste
    """
    print("📦 ALL RESOURCES IN CARGO HOLD:")
    cargo_data = cargo.get_cargo_hold()
    
    if "error" in cargo_data:
        print(f"❌ Error getting cargo data: {cargo_data['error']}")
        return {}
    
    resources = cargo_data["hold"]["resources"]
    print("Resources found:")
    for resource_name, amount in resources.items():
        print(f"  '{resource_name}': {amount}")
    
    print("\nCredits:", cargo_data["hold"]["credits"])
    print("Free space:", cargo_data["hold"]["hold_free"])
    print("Total capacity:", cargo_data["hold"]["hold_size"])
    
    return resources


def get_resource_amount(resource_code):
    """
    Get the amount of a specific resource in cargo hold
    """
    cargo_data = cargo.get_cargo_hold()
    if "error" in cargo_data:
        print(f"❌ Error getting cargo data: {cargo_data['error']}")
        return 0
    return cargo_data["hold"]["resources"].get(resource_code, 0)


def find_nuclear_waste():
    """
    Try to find nuclear waste by checking common names
    """
    resources = display_all_resources()
    
    # Common possible names for nuclear waste
    possible_names = ["W", "NUCLEAR_WASTE", "WASTE", "NUCLEAR", "NW", "nuclear_waste", "Nuclear Waste", "waste"]
    
    print("\n🔍 SEARCHING FOR NUCLEAR WASTE...")
    found_waste = {}
    
    for name in possible_names:
        if name in resources and resources[name] > 0:
            found_waste[name] = resources[name]
            print(f"✅ Found potential nuclear waste: '{name}' = {resources[name]}")
    
    if not found_waste:
        print("❌ No nuclear waste found with common names")
        print("💡 Check the resource list above for the exact name")
    
    return found_waste


def travel_position_and_sell_nuclear_waste(x, y, waste_name):
    """
    Travel to position and sell all nuclear waste
    """
    nuclear_waste_amount = get_resource_amount(waste_name)
    
    if nuclear_waste_amount <= 0:
        print(f"ℹ️  No {waste_name} to sell!")
        return
    
    print(f"💰 Selling {nuclear_waste_amount} units of {waste_name}")
    
    # Travel to position
    navigation.travel_position_until_recive(x, y)
    
    # Get the station at this position and sell
    station_name = list(comm.get_near_station().json()["stations"])[0]
    comm.sell(station_name, waste_name, nuclear_waste_amount)
    
    print(f"✅ Sold {nuclear_waste_amount} {waste_name} at {station_name}")


def sell_all_nuclear_waste_at_nuku():
    """
    Find and sell all nuclear waste at Nuku station
    """
    print("🚀 NUCLEAR WASTE DETECTION AND SELLING MISSION")
    print("=" * 50)
    
    energy.set_limit_normal()
    
    # First, let's see what's actually in the cargo
    waste_found = find_nuclear_waste()
    
    if not waste_found:
        print("\n❌ No nuclear waste detected!")
        print("💡 Please check the resource list above and manually update the script")
        return
    
    # Nuku station coordinates
    nuku_x = -96486
    nuku_y = -80625
    
    # Sell each type of waste found
    for waste_name, amount in waste_found.items():
        print(f"\n🎯 Processing {waste_name}: {amount} units")
        travel_position_and_sell_nuclear_waste(nuku_x, nuku_y, waste_name)
        
        # Show updated amount
        remaining = get_resource_amount(waste_name)
        print(f"📦 Remaining {waste_name}: {remaining}")
    
    print("\n🎉 Mission complete!")


if __name__ == "__main__":
    sell_all_nuclear_waste_at_nuku()