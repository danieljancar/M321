import navigation
import energy
import communication as comm
import cargo_hold as cargo


def get_resource_amount(resource_code):
    """
    Get the amount of a specific resource in cargo hold
    """
    cargo_data = cargo.get_cargo_hold()
    if "error" in cargo_data:
        print(f"❌ Error getting cargo data: {cargo_data['error']}")
        return 0
    return cargo_data["hold"]["resources"].get(resource_code, 0)


def travel_position_and_sell_nuclear_waste(x, y):
    """
    Travel to position and sell all nuclear waste (W) - following the same pattern as other scripts
    """
    nuclear_waste_amount = get_resource_amount("W")
    
    if nuclear_waste_amount <= 0:
        print("ℹ️  No nuclear waste (W) to sell!")
        return
    
    print(f"💰 Selling {nuclear_waste_amount} units of nuclear waste (W)")
    
    # Travel to position
    navigation.travel_position_until_recive(x, y)
    
    # Get the station at this position and sell
    station_name = list(comm.get_near_station().json()["stations"])[0]
    comm.sell(station_name, "W", nuclear_waste_amount)
    
    print(f"✅ Sold {nuclear_waste_amount} nuclear waste at {station_name}")


def sell_all_nuclear_waste_at_nuku():
    """
    Simple mission to sell all nuclear waste at Nuku station
    """
    print("🚀 Selling all nuclear waste at Nuku Station")
    
    energy.set_limit_normal()
    
    # Nuku station coordinates
    nuku_x = -96486
    nuku_y = -80625
    
    # Show current amount
    current_amount = get_resource_amount("W")
    print(f"📦 Current nuclear waste: {current_amount}")
    
    if current_amount > 0:
        travel_position_and_sell_nuclear_waste(nuku_x, nuku_y)
        
        # Show updated amount
        remaining = get_resource_amount("W")
        print(f"📦 Remaining nuclear waste: {remaining}")
        print("🎉 Mission complete!")
    else:
        print("❌ No nuclear waste to sell!")


if __name__ == "__main__":
    sell_all_nuclear_waste_at_nuku()