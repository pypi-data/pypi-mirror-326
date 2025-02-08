# coding: utf-8

"""
    Notion API

    Hello and welcome!  To make use of this API collection collection as it's written, please duplicate [this database template](https://www.notion.so/8e2c2b769e1d47d287b9ed3035d607ae?v=dc1b92875fb94f10834ba8d36549bd2a).  ﻿Under the `Variables` tab, add your environment variables to start making requests. You will need to [create an integration](https://www.notion.so/my-integrations) to retrieve an API token. You will also need additional values, such as a database ID and page ID, which can be found in your Notion workspace or from the database template mentioned above.  For our full documentation, including sample integrations and guides, visit [developers.notion.com](https://developers.notion.com/)﻿.  Please note: Pages that are parented by a database _must_ have the same properties as the parent database. If you are not using the database template provided, the request `body` for the page endpoints included in this collection should be updated to match the properties in the parent database being used. See documentation for [Creating a page](https://developers.notion.com/reference/post-page) for more information.  To learn more about creating an access token, see our [official documentation](https://developers.notion.com/reference/create-a-token) and read our [Authorization](https://developers.notion.com/docs/authorization#step-3-send-the-code-in-a-post-request-to-the-notion-api) guide.  Need more help? Join our [developer community on Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)﻿.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "notion-beta-ti"
VERSION = "0.0.1"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil >= 2.8.2",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Notion API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Notion API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    Hello and welcome!  To make use of this API collection collection as it&#39;s written, please duplicate [this database template](https://www.notion.so/8e2c2b769e1d47d287b9ed3035d607ae?v&#x3D;dc1b92875fb94f10834ba8d36549bd2a).  ﻿Under the &#x60;Variables&#x60; tab, add your environment variables to start making requests. You will need to [create an integration](https://www.notion.so/my-integrations) to retrieve an API token. You will also need additional values, such as a database ID and page ID, which can be found in your Notion workspace or from the database template mentioned above.  For our full documentation, including sample integrations and guides, visit [developers.notion.com](https://developers.notion.com/)﻿.  Please note: Pages that are parented by a database _must_ have the same properties as the parent database. If you are not using the database template provided, the request &#x60;body&#x60; for the page endpoints included in this collection should be updated to match the properties in the parent database being used. See documentation for [Creating a page](https://developers.notion.com/reference/post-page) for more information.  To learn more about creating an access token, see our [official documentation](https://developers.notion.com/reference/create-a-token) and read our [Authorization](https://developers.notion.com/docs/authorization#step-3-send-the-code-in-a-post-request-to-the-notion-api) guide.  Need more help? Join our [developer community on Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)﻿.
    """,  # noqa: E501
    package_data={"notion_beta_ti": ["py.typed"]},
)