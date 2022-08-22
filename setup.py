from setuptools import setup

github_url = "https://github.com/xioTechnologies/ximu3csv"

setup(name="ximu3csv",
      version="0.1.4",
      description="x-IMU3 CSV",
      long_description="See [github](" + github_url + ") for documentation and examples.",
      long_description_content_type='text/markdown',
      url=github_url,
      author="x-io Technologies Limited",
      author_email="info@x-io.co.uk",
      license="MIT",
      classifiers=["Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10"],  # versions shown by pyversions badge in README
      py_modules=["ximu3csv"])
