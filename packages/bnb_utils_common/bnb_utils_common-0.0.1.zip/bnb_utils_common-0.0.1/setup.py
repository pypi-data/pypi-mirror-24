from distutils.core import setup

setup(
    name="bnb_utils_common",
    version="0.0.1",
    author="Bnb team",
    author_email="neo.niu@nokia.com",
    description="tool to convert logs to dataframe.",
	long_description=open('README.rst').read(),
    license='BSD License',
	platforms=["all"],
    url = 'https://github.com/10177591/spamVSham/invitations',
    py_modules = ['read_config','log2_df','file_downloader','html_parser','log2_dataframe'], 
)