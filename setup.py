from setuptools import setup
import sys

if len(sys.argv) == 1:  # if this script was called without arguments
    sys.argv.append("install")
    sys.argv.append("--user")

github_url = "https://github.com/xioTechnologies/ximu3csv"

setup(name="ximu3csv",
      version="0.1.2",
      description="x-IMU3 CSV",
      long_description="See [github](" + github_url + ") for documentation and examples.",
      long_description_content_type='text/markdown',
      url=github_url,
      author="x-io Technologies Limited",
      author_email="info@x-io.co.uk",
      license="MIT",
      py_modules=["ximu3csv"])
