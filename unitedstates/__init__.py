from pupa.scrape import Jurisdiction, Organization

# scrapers
from .legislative import UnitedStatesLegislativeScraper
from .bill import UnitedStatesBillScraper
from .committee import UnitedStatesCommitteeScraper

class UnitedStates(Jurisdiction):
    classification = 'government'
    division_id = 'ocd-division/country:us'

    name = 'United States Federal Government'
    url = 'http://usa.gov/'

    parties = [
        {"name": "Republican",},
        {"name": "Democratic",},
        {"name": "Independent",},
    ]

    scrapers = {
        "congress": UnitedStatesLegislativeScraper,
        "bills": UnitedStatesBillScraper,
        "committees": UnitedStatesCommitteeScraper
    }

    def get_organizations(self):
        legislature = Organization("United States Congress",
                                   classification='legislature')
        yield legislature