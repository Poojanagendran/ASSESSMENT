class Environment:
    def __init__(self):
        environment = "amsin"
        # environment = input("Please enter the environment [amsin or ams or betams] ").strip().lower()

        domains = {
            'ams': {
                'domain': 'https://ams.hirepro.in',
                'pearson_domain': 'https://vet.hirepro.in',
                'eu_domain': 'https://euapp.hirepro.ai',
                'cocubes_domain': 'https://assessccbs.hirepro.in',
                'talentlens_domain': 'https://talentlens.hirepro.in'

            },
            'live': {
                'domain': 'https://ams.hirepro.in',
                'pearson_domain': 'https://vet.hirepro.in',
                'eu_domain': 'https://euapp.hirepro.ai',
                'cocubes_domain': 'https://assessccbs.hirepro.in',
                'talentlens_domain': 'https://talentlens.hirepro.in'
            },
            'betaams': {
                'domain': 'https://betaams.hirepro.in',
                'pearson_domain': 'https://betavet.hirepro.in',
                'eu_domain': 'https://betavet.hirepro.in',
                'cocubes_domain': 'https://stgassessccbs.hirepro.in',
                'talentlens_domain': 'https://ams.hirepro.in'
            },
            'beta': {
                'domain': 'https://betaams.hirepro.in',
                'pearson_domain': 'https://betavet.hirepro.in',
                'eu_domain': 'https://betavet.hirepro.in',
                'cocubes_domain': 'https://stgassessccbs.hirepro.in',
                'talentlens_domain': 'https://ams.hirepro.in'
            },
            'amsin': {
                'domain': 'https://amsin.hirepro.in',
                'pearson_domain': 'https://pearsonstg.hirepro.in',
                'eu_domain': 'https://euamsin.hirepro.in',
                'cocubes_domain': 'https://qaassesscocubes.hirepro.in',
                'talentlens_domain': 'https://talentlensstg.hirepro.in'
            },
            'mumbai': {
                'domain': 'https://amsin.hirepro.in',
                'pearson_domain': 'https://pearsonstg.hirepro.in',
                'eu_domain': 'https://euamsin.hirepro.in',
                'cocubes_domain': 'https://qaassesscocubes.hirepro.in',
                'talentlens_domain': 'https://talentlensstg.hirepro.in'
            }
        }

        if environment in domains:
            domain_info = domains[environment]
            self.domain = domain_info['domain']
            self.pearson_domain = domain_info['pearson_domain']
            self.eu_domain = domain_info['eu_domain']
            self.cocubes_domain = domain_info['cocubes_domain']
            self.talentlens_domain = domain_info['talentlens_domain']
        else:
            print("Please enter the proper domain")


env_obj = Environment()
