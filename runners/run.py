from soccerway_runner import Soccerway
from transfermarkt_clubs_runner import TransfermarktClubs
from transfermarkt_details_clubs_runner import TransfermarktDetailedClubs
from transfermarkt_leagues_runner import TransfermarktLeagues
from transfermarkt_qualifiers_runner import TransfermarktQualifiers
from uefa_coefficients_runner import UefaCoefficients
from uefa_european_cups_runner import UefaEuropeanCups

UefaCoefficients().run()
TransfermarktLeagues().run()
TransfermarktClubs().run()
TransfermarktDetailedClubs().run()
Soccerway().run()
TransfermarktQualifiers().run()
UefaEuropeanCups().run()
