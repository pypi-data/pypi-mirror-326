from awesomeNations.exceptions import RegionNotFound
from awesomeNations.configuration import DEFAULT_PARSER
from awesomeNations.seleniumScrapper import get_dynamic_source
from awesomeNations.sharedMethods import request, format_text
from bs4 import BeautifulSoup as bs
from typing import Iterator

def check_if_region_exists(region_name: str) -> None:
    url: str = f'https://www.nationstates.net/region={region_name}'
    response: dict = request(parser='html.parser', url=url)
    soup: bs = response
    error_p = soup.find('p', class_="error")

    if error_p:
        raise RegionNotFound(region_name)

def embassy_generator(url: str, default_embassies_output: None) -> Iterator:
    source: str = get_dynamic_source(url, '//*[contains(concat( " ", @class, " " ), concat( " ", "divindent", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mcollapse", " " ))]')
    try:
        soup: bs = bs(source, DEFAULT_PARSER)

        divindents: bs = soup.find_all('div', class_='divindent')
        embassy_table: bs = divindents[3].find('table', class_='shiny wide embassies mcollapse')

        for n, d in zip(embassy_table.find_all('td', class_='bigleft'), embassy_table.find_all('td', class_='')):
            name = n.get_text()
            duration = d.get_text()
            if str(name[0]).isnumeric():
                split: list = name.split(' ')
                split.pop(0)
                name = ' '.join(split)
            yield {'region': name, 'duration': duration}
    except:
        yield default_embassies_output

def scrape_world_census(url: str):
    try:
        response = request(parser='lxml', url=url)
        soup: bs = response

        region_rank: list = []

        rank_table = soup.find('table', class_='shiny ranks nationranks mcollapse').find_all('tr')
        rank_table.pop(0)

        rank_elements = [td.find_all('td', limit=2) for td in rank_table]
        for td in rank_elements:
            nation = td[1].get_text()
            region_rank.append(nation)
        
        page = soup.find('div', id='regioncontent')
        paragraphs = page.find_all('p', limit=2)

        description: str = paragraphs[0].get_text()
        region_world_rank: str = paragraphs[1].get_text()
        return {'title': page.find('h3').get_text(), 'description': description, 'region_world_rank': region_world_rank, 'rank': region_rank}
    except:
        return None

class R:
    def __init__(self, region_name: str):
        self.region_name = region_name
    
    def exists(self) -> bool:
        region_name: str = self.region_name
        url: str = f'https://www.nationstates.net/region={region_name}'
        response: bs = request(parser='lxml', url=url)
        error_p = response.find('p', class_="error")

        if error_p:
            return False
        else:
            return True

    def overview(self):
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        url: str = f'https://www.nationstates.net/region={formatted_name}'
        response: dict = request(parser='lxml', url=url)
        soup: bs = response

        founder: str = None
        governor: str = None
        category: str = None
        wa_delegate: str = None
        last_wa_update: str = None
        region_flag: str = None
        region_banner: str = None

        region_cover = soup.find('div', class_='regioncover')

        flag_cover = region_cover.find('img')
        if flag_cover:
            if flag_cover.has_attr('src'):
                region_flag = f'https://www.nationstates.net{flag_cover.attrs['src']}'
            elif flag_cover.has_attr('data-cfsrc'):
                region_flag = f'https://www.nationstates.net{flag_cover.attrs['data-cfsrc']}'
        banner_source = region_cover.attrs['style'].replace('background-image:url', '').replace('(', '').replace(')', '')
        region_banner = f'https://www.nationstates.net{banner_source}'

        region_content = soup.find('div', id='regioncontent')
        paragraphs: list = region_content.find_all('p', limit=4)
        for text in paragraphs:
            content: str = text.get_text().strip()
            if 'Feeder' in content or 'Sinker' in content or 'Frontier' in content:
                category = content
            if 'Last WA Update' in content:
                last_wa_update = content
            if 'Governor' in content:
                governor = content
            if 'WA Delegate' in content:
                wa_delegate = content
            if 'Founder' in content:
                founder = content

        overview = dict(category=category, governor=governor, wa_delegate=wa_delegate, last_wa_update=last_wa_update, founder=founder, region_flag=region_flag, region_banner=region_banner)
        return overview

    def world_census(self, censusid: tuple | list) -> Iterator:
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        for id in censusid:
            url: str = f'https://www.nationstates.net/page=list_nations/censusid={id}/region={formatted_name}'

            world_census: dict = scrape_world_census(url)
            yield world_census

    def activity(self, filter: str):
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        url: str = f'https://www.nationstates.net/page=activity/view=region.{formatted_name}/filter={filter}'
        source: str = get_dynamic_source(url, '//*[@id="reports"]/ul')

        events = None

        if not source == None:        
            soup: bs = bs(source, DEFAULT_PARSER)
            reports = soup.find('div', class_='clickabletimes').find('ul')
            events = (li.get_text() for li in reports.find_all('li'))
            return events
        return events

    def embassies(self) -> Iterator:
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        default_embassies_output: None = None
        url: str = f'https://www.nationstates.net/page=region_admin/region={formatted_name}'
        embassies: Iterator = embassy_generator(url, default_embassies_output)
        return embassies