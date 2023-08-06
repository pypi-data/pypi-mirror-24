import requests


class Result:
    def __init__(self):
        self.url = None
        self.page_title = None
        self.status_code = None
        self.score = None

        self.stats = {
            'numberof': {
                'resources': None,
                'hosts': None,
                'js': None,
                'css': None,
            }
        }

        self.results = {}


class PageSpeedWrapper:
    def __init__(self, api_key):
        self.api_key = api_key

    def run(self, url):
        response = requests.get('https://www.googleapis.com/pagespeedonline/v2/runPagespeed', params={'key': self.api_key, 'url': url}).json()

        # Create Result object
        result = Result()

        # Start to pull result data
        result.page_title = response.get('title')
        result.url = response.get('id')
        result.status_code = response.get('responseCode')
        result.score = response.get('ruleGroups', {}).get('SPEED', {}).get('score')

        result.stats['numberof']['resources'] = response.get('pageStats', {}).get('numberResources')
        result.stats['numberof']['hosts'] = response.get('pageStats', {}).get('numberHosts')
        result.stats['numberof']['js'] = response.get('pageStats', {}).get('numberJsResources')
        result.stats['numberof']['css'] = response.get('pageStats', {}).get('numberCssResources')

        result.results = []

        for key in response.get('formattedResults').get('ruleResults'):
            v = response.get('formattedResults').get('ruleResults')[key]

            result_builder = {'id': key}

            result_builder['name'] = v.get('localizedRuleName')
            result_builder['impact'] = v.get('ruleImpact')

            if not v.get('summary'):
                raise Exception('Error running test \'summary\' key not found on the API result, run again.')

            result_builder.update(self.__link_replace(v.get('summary')))

            if v.get('urlBlocks'):
                urlblocks = []

                for item in v.get('urlBlocks', []):
                    urlblock = {}

                    header = item.get('header')

                    urlblock.update(self.__link_replace(header))
                    urlblock.update(self.__url_replace(item.get('urls', [])))

                    urlblocks += [urlblock]

                result_builder.update({'blocks': urlblocks})

            result.results += [result_builder]

        return result

    def __link_replace(self, block):
        result_builder = {}

        result_builder['summary'] = block.get('format')

        for arg in block.get('args', []):
            if arg.get('key') == 'LINK':
                result_builder['summary'] = result_builder['summary'].replace('{{BEGIN_LINK}}', '').replace('{{END_LINK}}', '')

                result_builder['link'] = arg.get('value')
            else:
                result_builder['summary'] = result_builder['summary'].replace('{{' + arg.get('key') + '}}', arg.get('value'))

        return result_builder

    def __url_replace(self, block):
        result_builder = []

        for url in block:
            result = {}

            res = url.get('result')

            result['summary'] = res.get('format')

            for arg in res.get('args', []):
                result['summary'] = result['summary'].replace('{{' + arg.get('key') + '}}', arg.get('value'))

                result[arg.get('key').lower()] = arg.get('value')

            result_builder += [result]

        return {'urls': result_builder}
