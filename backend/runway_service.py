"""
Estimates whether a flight will be visible from the RDU observation deck.

The observation deck overlooks runway 23R/5L — the longer runway (10,000 ft).
Large mainline jets use this runway; regional jets and turboprops use the
shorter parallel runway 23L/5R, which is not visible from the deck.

Wind direction does NOT affect deck visibility. It determines which end of the
runway aircraft use (heading 23 or 5), but both ends of 23R/5L are the same
physical strip of pavement.

When aircraft type is unknown we fall back to airline identity: mainline
carriers fly large jets; regional affiliates fly small jets/turboprops.
"""

# ICAO type codes for large/mainline aircraft → use the longer runway (visible)
_LARGE_TYPES = {
    # Airbus A220
    "BCS1", "BCS3",
    # Airbus A320 family
    "A318", "A319", "A320", "A321", "A19N", "A20N", "A21N",
    # Airbus A330/A340/A350/A380
    "A332", "A333", "A338", "A339", "A342", "A343", "A345", "A346",
    "A359", "A35K", "A388",
    # Boeing 737
    "B731", "B732", "B733", "B734", "B735", "B736", "B737", "B738",
    "B739", "B73X", "B37M", "B38M", "B39M", "B3XM",
    # Boeing 757/767/777/787/747
    "B752", "B753", "B762", "B763", "B764",
    "B772", "B773", "B77L", "B77W", "B788", "B789", "B78X",
    "B741", "B742", "B743", "B744", "B748",
    # Embraer E190/195 (mainline-size)
    "E190", "E195", "E7W",
    # MD series
    "MD11", "MD81", "MD82", "MD83", "MD88", "MD90", "DC10",
}

# Mainline carriers → large aircraft (visible)
_MAINLINE_AIRLINES = {
    "AA", "DL", "UA", "WN", "B6", "AS", "NK", "F9", "G4", "SY", "HA",
    "BA", "AF", "LH", "KL", "LX", "OS", "IB", "AY", "SK", "TP",
    "AC", "WS", "AM", "CM", "AV", "LA", "JJ", "G3", "AD",
    "EK", "QR", "EY", "TK", "SQ", "CX", "NH", "JL", "KE", "OZ",
    "QF", "NZ", "VA", "AI", "6E",
}

# Regional affiliates → small aircraft (not visible)
_REGIONAL_AIRLINES = {
    "9E", "OH", "MQ", "YX", "OO", "QX", "G7", "ZW", "C5", "AX",
    "YV", "PT", "EV", "CP", "UP",
}


def _is_large(aircraft_icao: str | None, airline_iata: str | None) -> bool | None:
    """True = large (visible), False = small (not visible), None = unknown."""
    if aircraft_icao:
        return aircraft_icao.upper() in _LARGE_TYPES
    if airline_iata:
        code = airline_iata.upper()
        if code in _MAINLINE_AIRLINES:
            return True
        if code in _REGIONAL_AIRLINES:
            return False
    return None


def estimate_visibility(aircraft_icao: str | None, airline_iata: str | None) -> dict:
    result = _is_large(aircraft_icao, airline_iata)
    return {"deck_visible": result}  # True / False / None (unknown)
