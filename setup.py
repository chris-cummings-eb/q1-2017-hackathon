from setuptools import setup

setup(
    name="eb_automation_lib",
    version="0.0.1",
    description="library for running workflow automations using Apple's OSA",
    url="",
    author="Chris Cummings",
    author_email="ccummings@eventbrite.com",
    license="MIT",
    packages=["eb_automation_lib"],
    install_requires=[
        "pyobjc",
        "eventbrite",
        "flask"
    ],
    zip_safe=False
)
