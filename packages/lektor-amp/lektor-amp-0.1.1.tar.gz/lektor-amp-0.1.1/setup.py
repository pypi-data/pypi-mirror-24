from setuptools import setup

setup(
    name='lektor-amp',
    version='0.1.1',
    description='Create an amp version of your website.',
    author=u'Matthias Rebel',
    author_email='webmaster@rebeling.net',
    license='MIT',
    url='https://github.com/rebeling/lektor-amp',
    py_modules=['lektor_amp'],
    entry_points={
        'lektor.plugins': [
            'amp = lektor_amp:AmpPlugin',
        ]
    }
)
