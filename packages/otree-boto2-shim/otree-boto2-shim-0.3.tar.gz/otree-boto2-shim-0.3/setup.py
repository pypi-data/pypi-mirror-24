from setuptools import setup, find_packages

setup(
	name="otree-boto2-shim",
	version='0.3',
	description="Shim package so that boto2 imports don't fail when using oTree.",
    url='http://www.otree.org',
	author='Chris',
	author_email='chris@otree.org',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
)
