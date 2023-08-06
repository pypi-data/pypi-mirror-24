from setuptools import setup,find_packages

setup(
    name='gapi',
    version='1.2.0',
    author='Scott Hendrickson, Josh Montague, Jeff Kolb, Fiona Pigott',
    author_email='des-services@twitter.com',
    packages=['gapi'],
    scripts=['tools/gnip_search.py', 
             'tools/gnip_time_series.py',
             'tools/gnip_filter_analysis.py'],
    package_data={'gapi':['config/job.json']},
    url='https://github.com/tw-ddis/Gnip-Python-Search-API-Utilities',
    download_url='https://github.com/tw-ddis/Gnip-Python-Search-API-Utilities/tags/',
    license='LICENSE.txt',
    description='Simple utilties to explore the Gnip search API',
    install_requires=[
         "tweet_parser >=1.0.5",
         "sngrams >= 0.2.0" ,
         "requests > 2.4.0"
        ],
    extras_require = {
        'timeseries':  ["numpy >= 1.10.1"
                , "scipy >= 0.16.1"
                , "statsmodels >= 0.6.1"
                , "matplotlib >= 1.5.0"
                , "pandas >= 0.17.0"
                ],
        }
    )
