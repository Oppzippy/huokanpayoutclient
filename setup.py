#!/usr/bin/env python3

from distutils.core import setup
import setuptools

setup(
    name="huokanpayoutclient",
    version="1.1.1",
    description="Search logs from the Huokan Payout addon for World of Warcraft.",
    author="Oppzippy",
    author_email="oppzippy@gmail.com",
    license="UNLICENSED",
    packages=setuptools.find_packages(),
    install_requires=["SLPP"],
    entry_points={
        "gui_scripts": ["huokanpayoutclient=huokanpayoutclient.entrypoints.main:main"]
    },
    include_package_data=True,
    data_files=[("huokanpayoutclient", ["huokanpayoutclient/logo.ico"])],
)
