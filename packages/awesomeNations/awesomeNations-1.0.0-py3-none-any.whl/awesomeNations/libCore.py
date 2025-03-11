from awesomeNations.exceptions import HTTPError
import requests
from customMethods import parse_xml_to_dictionary, check_nationstates_api_ratelimit
import time
from configuration import DEFAULT_HEADERS

class ApiConnection():
    instances_limit = 1
    instances_num = 0
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.instances_num += 1
        if cls.instances_num > cls.instances_limit:
            raise RuntimeError(f"{cls.__name__}: Max connection instances reached.")
        return instance

    def __init__(self,
                 user_agent: str = None,
                 session: bool = False,
                 request_timeout: tuple | int = (10, 5),
                 ratelimit_sleep = True,
                 ratelimit_reset_time = 30,
                 api_version = 12,
                 ):
        self.session = session
        self.request_timeout = request_timeout
        self.user_agent = user_agent
        self.ratelimit_sleep = ratelimit_sleep
        self.ratelimit_reset_time = ratelimit_reset_time
        self.ratelimit_remaining = None
        self.ratelimit_requests_seen = None
        self.api_version = api_version

        self.CurrentConnectionSession = requests.Session()

    def check_api_ratelimit(self) -> None:
        if self.ratelimit_sleep:
            limit_remaining = self.ratelimit_remaining
            reset_delay = self.ratelimit_reset_time
            if limit_remaining <= 1:
                time.sleep(reset_delay + 1)

    def fetch_api_data(self, url: str = 'https://www.nationstates.net/', query_parameters: None = None, stream: bool = False) -> dict:
        url += f"&v={self.api_version}"
        if self.session:
            response = self.CurrentConnectionSession.get(url, headers=self.user_agent, timeout=self.request_timeout, params=query_parameters)
        else:
            response = requests.get(url, headers=self.user_agent, timeout=(10, 5), stream=stream)

        if response.status_code != 200:
            raise HTTPError(response.status_code)
        
        ratelimit_remaining: str | None = response.headers.get("Ratelimit-remaining")
        # ratelimit_requests_seen: str | None = response.headers.get("X-ratelimit-requests-seen")
        
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        # self.ratelimit_requests_seen = int(ratelimit_requests_seen) if ratelimit_requests_seen else None

        parsed_response = parse_xml_to_dictionary(response.text)
        check_nationstates_api_ratelimit(self.ratelimit_remaining, self.ratelimit_reset_time)
        # self.check_api_ratelimit()
        return parsed_response

    def fetch_html_data(self, url: str = 'https://www.nationstates.net/', query_parameters: None = None, stream: bool = False) -> str:
        if self.session:
            response = self.CurrentConnectionSession.get(url, headers=self.user_agent, timeout=self.request_timeout, params=query_parameters)
        else:
            response = requests.get(url, headers=self.user_agent, timeout=(10, 5), stream=stream)

        if response.status_code != 200:
            raise HTTPError(response.status_code)

        return response.text


if __name__ == "__main__":
    wrapper = ApiConnection(DEFAULT_HEADERS)
    response = wrapper.fetch_api_data("https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia968756")
    
    print(response)