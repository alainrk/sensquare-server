import mgrs

'''
@zone, Full coord mgrs (1m precision, even though granularity then will cut)
@granularity, How many "bit" (0-5 => 100km-1m) in 2 last part of mgrs save for match
@coord, Full coord mgrs to check belonging to @zone

Granularity:
0 -> 100.000 m
1 -> 10.000 m
2 -> 1.000 m
3 -> 100 m
4 -> 10 m
5 -> 1 m

Zone given =        "32T PQ 12345 12345"
Coord given =       "32T PQ 12389 12389"
granularity 10m =>      4 (1234* 1234*)     DOES NOT MATCH
granularity 1000m =>    2 (12*** 12***)     MATCH
'''
def belongto(zone, coord, granularity):
    # Division in "32T PQ 12345 12345"
    gridsq_zone, bigsq_zone, x_zone, y_zone = zone[:3], zone[3:5], zone[5:10], zone[10:15]
    gridsq_coord, bigsq_coord, x_coord, y_coord = coord[:3], coord[3:5], coord[5:10], coord[10:15]
    return gridsq_zone == gridsq_coord and \
            bigsq_zone == bigsq_coord and \
            x_zone[0:granularity] == x_coord[0:granularity] and \
            y_zone[0:granularity] == y_coord[0:granularity]

print(belongto("32TPQ1234512345", "32TPQ1238912389", 4)) # False
print(belongto("32TPQ1234512345", "32TPQ1238912389", 2)) # True
