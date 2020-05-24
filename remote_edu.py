from google.cloud import speech_v1
import io
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

# WATSON ASSISTANT
__version__ = '4.4.1'

if sys.argv[-1] == 'publish':
    # test server
    os.system('python setup.py register -r politest')
    os.system('python setup.py sdist upload -r politest')

    # production server
    os.system('python setup.py register -r pypy')
    os.system('python setup.py sdist upload -r pypy')
    sys.exit()

try:
    from pypandoc import convert_file


    def read_md(f):
        return convert_file(f, 'rst')


    print('warning: pypandoc module not found, '
          'could not convert Markdown to RST')


    def read(f):
        return open(f, 'rb').read().decode(encoding='utf-8')
    # read_md = lambda f: open(f, 'rb').read().decode(encoding='utf-8')
except:
    class PyTest(TestCommand):
        def __init__(self, dist, **kw):
            super().__init__(dist, **kw)
            self.test_suite = True
            self.test_args = ['--strict', '--verbose', '--tb=long', 'test']


    def finalize_options(self):
        TestCommand.finalize_options(self)


    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def pyTest(args):
    pass


setup(name='ibm-watson',
      version=__version__,
      description='Client library to use the IBM Watson Services',
      license='Apache 2.0',
      install_requires=['requests>=2.0, <3.0', 'python_dateutil>=2.5.3', 'websocket-client==0.48.0',
                        'ibm_cloud_sdk_core==1.5.1'],
      tests_require=['responses', 'pytest', 'python_dotenv', 'pytest-rerunfailures', 'tox'],
      cmdclass={'test': pyTest},
      author='IBM Watson',
      author_email='watdevex@us.ibm.com',
      packages=['ibm_watson'],
      long_description=read_md('README.md'),
      include_package_data=True,
      keywords='language, vision, question and answer' +
               ' tone_analyzer, natural language classifier,' +
               ' text to speech, language translation, ' +
               'language identification, concept expansion, machine translation, ' +
               'personality insights, message resonance, watson developer cloud, ' +
               ' wdc, watson, ibm, dialog, user modeling,' +
               'tone analyzer, speech to text, visual recognition',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Libraries :: Application '
          'Frameworks',
      ],
      zip_safe=True
      )


# VIDEO transcribe

def sample_recognize(local_file_path, model):
    client = speech_v1.SpeechClient()
    language_code = "en-US"
    config = {"model": model, "language_code": language_code}
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    video = {"content": content}

    response = client.recognize(config, video)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--local_file_path", type=str, default="resources/hello.wav")
    parser.add_argument("--model", type=str, default="phone_call")
    args = parser.parse_args()

    convert_file(args.local_file_path, args.model)


# AUDIO transcribe

def recognize(storage_uri, model):
    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/hello.wav'
    # model = 'phone_call'

    # The language of the supplied audio
    language_code = "en-US"
    config = {"model": model, "language_code": language_code}
    audio = {"uri": storage_uri}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


# [END speech_transcribe_model_selection_gcs]
def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri", type=str, default="gs://cloud-samples-data/speech/hello.wav"
    )
    parser.add_argument("--model", type=str, default="phone_call")
    args = parser.parse_args()

    recognize(args.storage_uri, args.model)
