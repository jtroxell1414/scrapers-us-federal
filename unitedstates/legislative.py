from pupa.scrape import Scraper, Person, Membership, Organization
from pupa.utils import make_psuedo_id

import yaml

CURRENT_LEGISLATORS = ("https://raw.githubusercontent.com/"
                       "unitedstates/congress-legislators/"
                       "master/legislators-current.yaml")


class UnitedStatesLegislativeScraper(Scraper):

    def yamlize(self, url):
        resp = self.urlopen(url)
        return yaml.safe_load(resp)

    def scrape_current_legislators(self):
        people = self.yamlize(CURRENT_LEGISLATORS)
        for person in people:
            name = person['name']['official_full']
            who = Person(name=name)
            who.add_source(url=CURRENT_LEGISLATORS,
                           note="unitedstates project on GitHub")

            for term in person.get('terms', []):
                start_date = term['start']
                end_date = term['end']
                state = term['state']
                type_ = term['type']
                district = term.get('district', None)
                party = term.get('party', None)

                chamber = {'rep': 'lower',
                           'sen': 'upper',}[type_]

                role = {'rep': 'Representative',
                        'sen': 'Senator',}[type_]

                if district:
                    membership = Membership(
                        role=role,
                        label="%s for District %s" % (role, district),
                        start_date=start_date,
                        end_date=end_date,
                        person_id=who._id,
                        organization_id=make_psuedo_id(
                            classification="legislature",
                            chamber=chamber))
                    yield membership

                if party:
                    membership = Membership(
                        role='member',
                        start_date=start_date,
                        end_date=end_date,
                        person_id=who._id,
                        organization_id=make_psuedo_id(
                            classification="party",
                            name=party))
                    yield membership

            for key, value in person.get('id', {}).items():
                who.add_identifier(str(value), scheme=key)

            yield who

    def scrape(self):
        yield from self.scrape_current_legislators()
