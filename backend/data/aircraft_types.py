"""ICAO aircraft type code → human-readable name."""

AIRCRAFT_TYPES: dict[str, str] = {
    # Boeing 737
    "B731": "Boeing 737-100",
    "B732": "Boeing 737-200",
    "B733": "Boeing 737-300",
    "B734": "Boeing 737-400",
    "B735": "Boeing 737-500",
    "B736": "Boeing 737-600",
    "B737": "Boeing 737-700",
    "B738": "Boeing 737-800",
    "B739": "Boeing 737-900",
    "B73X": "Boeing 737-900ER",
    "B37M": "Boeing 737 MAX 7",
    "B38M": "Boeing 737 MAX 8",
    "B39M": "Boeing 737 MAX 9",
    "B3XM": "Boeing 737 MAX 10",
    # Boeing 757
    "B752": "Boeing 757-200",
    "B753": "Boeing 757-300",
    # Boeing 767
    "B762": "Boeing 767-200",
    "B763": "Boeing 767-300",
    "B764": "Boeing 767-400",
    # Boeing 777
    "B772": "Boeing 777-200",
    "B773": "Boeing 777-300",
    "B77L": "Boeing 777-200LR",
    "B77W": "Boeing 777-300ER",
    # Boeing 787
    "B788": "Boeing 787-8",
    "B789": "Boeing 787-9",
    "B78X": "Boeing 787-10",
    # Boeing 747
    "B741": "Boeing 747-100",
    "B742": "Boeing 747-200",
    "B743": "Boeing 747-300",
    "B744": "Boeing 747-400",
    "B748": "Boeing 747-8",
    # Airbus A220
    "BCS1": "Airbus A220-100",
    "BCS3": "Airbus A220-300",
    "A220": "Airbus A220",
    # Airbus A320 family
    "A318": "Airbus A318",
    "A319": "Airbus A319",
    "A320": "Airbus A320",
    "A321": "Airbus A321",
    "A20N": "Airbus A320neo",
    "A21N": "Airbus A321neo",
    "A19N": "Airbus A319neo",
    "A321": "Airbus A321",
    "A321XLR": "Airbus A321XLR",
    # Airbus A330
    "A332": "Airbus A330-200",
    "A333": "Airbus A330-300",
    "A338": "Airbus A330-800neo",
    "A339": "Airbus A330-900neo",
    # Airbus A340
    "A342": "Airbus A340-200",
    "A343": "Airbus A340-300",
    "A345": "Airbus A340-500",
    "A346": "Airbus A340-600",
    # Airbus A350
    "A359": "Airbus A350-900",
    "A35K": "Airbus A350-1000",
    # Airbus A380
    "A388": "Airbus A380",
    # Embraer E-Jets
    "E170": "Embraer E170",
    "E175": "Embraer E175",
    "E190": "Embraer E190",
    "E195": "Embraer E195",
    "E75L": "Embraer E175-E2",
    "E75S": "Embraer E175",
    "E7W": "Embraer E190-E2",
    # Embraer Regional Jets
    "E135": "Embraer ERJ-135",
    "E145": "Embraer ERJ-145",
    "E140": "Embraer ERJ-140",
    # Bombardier CRJ
    "CRJ1": "Bombardier CRJ-100",
    "CRJ2": "Bombardier CRJ-200",
    "CRJ7": "Bombardier CRJ-700",
    "CRJ9": "Bombardier CRJ-900",
    "CRJX": "Bombardier CRJ-1000",
    "CR7": "Bombardier CRJ-700",
    "CR9": "Bombardier CRJ-900",
    # Bombardier Dash 8 / Q Series
    "DH8A": "Bombardier Q100",
    "DH8B": "Bombardier Q200",
    "DH8C": "Bombardier Q300",
    "DH8D": "Bombardier Q400",
    # ATR
    "AT43": "ATR 42-300",
    "AT45": "ATR 42-500",
    "AT46": "ATR 42-600",
    "AT72": "ATR 72-200",
    "AT73": "ATR 72-210",
    "AT75": "ATR 72-500",
    "AT76": "ATR 72-600",
    # Cessna / Beechcraft
    "C208": "Cessna Caravan",
    "B350": "Beechcraft King Air 350",
    # Saab
    "SF34": "Saab 340",
    "S340": "Saab 340",
    # Fokker
    "F100": "Fokker 100",
    "F70": "Fokker 70",
    # McDonnell Douglas
    "MD11": "MD-11",
    "MD81": "MD-81",
    "MD82": "MD-82",
    "MD83": "MD-83",
    "MD88": "MD-88",
    "MD90": "MD-90",
    "DC10": "DC-10",
    "DC9": "DC-9",
}


def get_aircraft_name(icao_code: str | None) -> str | None:
    if not icao_code:
        return None
    return AIRCRAFT_TYPES.get(icao_code.upper())
