import requests
from django.shortcuts import render

def search_weapons(request):
    # Initialize context for template
    context = {}
    if request.method == 'GET':
        # Read filter inputs from GET params
        weapon_class = request.GET.get('weapon_class')    # e.g. "Two Hand Axes"
        damage_type = request.GET.get('damage_type')      # "Physical", "Elemental", "Chaos", or "All"
        min_aps = request.GET.get('min_aps')
        max_aps = request.GET.get('max_aps')
        min_dps = request.GET.get('min_dps')
        max_dps = request.GET.get('max_dps')
        
        # Build Cargoquery API URL
        base_url = "https://www.poewiki.net/w/api.php?action=cargoquery&tables=items,weapons"
        join = "&join_on=items._pageID=weapons._pageID"
        fields = "&fields=items.name,items.class,weapons.attack_speed," \
                 "weapons.physical_dps_range_average,weapons.elemental_dps_range_average," \
                 "weapons.chaos_dps_range_average,weapons.dps_range_average"
        conditions = []
        # Add conditions based on filters
        if weapon_class: 
            conditions.append(f'items.class="{weapon_class}"')
        if min_aps:
            conditions.append(f'weapons.attack_speed>={min_aps}')
        if max_aps:
            conditions.append(f'weapons.attack_speed<={max_aps}')
        # Determine which DPS field to filter on based on damage_type
        dps_field = "weapons.dps_range_average"
        if damage_type == "Physical":
            dps_field = "weapons.physical_dps_range_average"
            conditions.append("weapons.physical_dps_range_average>0")
        elif damage_type == "Elemental":
            dps_field = "weapons.elemental_dps_range_average"
            conditions.append("weapons.elemental_dps_range_average>0")
        elif damage_type == "Chaos":
            dps_field = "weapons.chaos_dps_range_average"
            conditions.append("weapons.chaos_dps_range_average>0")
        if min_dps:
            conditions.append(f'{dps_field}>={min_dps}')
        if max_dps:
            conditions.append(f'{dps_field}<={max_dps}')
        # Join all conditions with AND for the API query
        where_clause = ""
        if conditions:
            where_clause = "&where=" + " AND ".join(conditions)
        # Finalize URL with format=json for direct JSON output
        api_url = f"{base_url}{join}{fields}{where_clause}&format=json"
        
        # Fetch data from the Wiki API
        response = requests.get(api_url)
        data = response.json()  # Parse JSON response
        results = []
        for entry in data.get("cargoquery", []):
            item = entry["title"]
            # Prepare each result (convert numeric strings to float/int as needed)
            results.append({
                "name": item.get("name"),
                "class": item.get("class"),
                "attack_speed": item.get("attack_speed"),
                "physical_dps": item.get("physical_dps_range_average"),
                "elemental_dps": item.get("elemental_dps_range_average"),
                "total_dps": item.get("dps_range_average"),
            })
        context["results"] = results
        context["filters"] = {   # include current filters to refill form, if needed
            "weapon_class": weapon_class or "",
            "damage_type": damage_type or "All",
            "min_aps": min_aps or "",
            "max_aps": max_aps or "",
            "min_dps": min_dps or "",
            "max_dps": max_dps or ""
        }
    return render(request, "weapons/search.html", context)
