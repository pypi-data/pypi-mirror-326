# coding: utf-8

"""
    Notion API

    Hello and welcome!  To make use of this API collection collection as it's written, please duplicate [this database template](https://www.notion.so/8e2c2b769e1d47d287b9ed3035d607ae?v=dc1b92875fb94f10834ba8d36549bd2a).  ﻿Under the `Variables` tab, add your environment variables to start making requests. You will need to [create an integration](https://www.notion.so/my-integrations) to retrieve an API token. You will also need additional values, such as a database ID and page ID, which can be found in your Notion workspace or from the database template mentioned above.  For our full documentation, including sample integrations and guides, visit [developers.notion.com](https://developers.notion.com/)﻿.  Please note: Pages that are parented by a database _must_ have the same properties as the parent database. If you are not using the database template provided, the request `body` for the page endpoints included in this collection should be updated to match the properties in the parent database being used. See documentation for [Creating a page](https://developers.notion.com/reference/post-page) for more information.  To learn more about creating an access token, see our [official documentation](https://developers.notion.com/reference/create-a-token) and read our [Authorization](https://developers.notion.com/docs/authorization#step-3-send-the-code-in-a-post-request-to-the-notion-api) guide.  Need more help? Join our [developer community on Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)﻿.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from notion_beta_ti.api.blocks_api import BlocksApi


class TestBlocksApi(unittest.TestCase):
    """BlocksApi unit test stubs"""

    def setUp(self) -> None:
        self.api = BlocksApi()

    def tearDown(self) -> None:
        pass

    def test_v1_blocks_id_children_get(self) -> None:
        """Test case for v1_blocks_id_children_get

        Retrieve block children
        """
        pass

    def test_v1_blocks_id_children_patch(self) -> None:
        """Test case for v1_blocks_id_children_patch

        Append block children
        """
        pass

    def test_v1_blocks_id_delete(self) -> None:
        """Test case for v1_blocks_id_delete

        Delete a block
        """
        pass

    def test_v1_blocks_id_get(self) -> None:
        """Test case for v1_blocks_id_get

        Retrieve a block
        """
        pass

    def test_v1_blocks_id_patch(self) -> None:
        """Test case for v1_blocks_id_patch

        Update a block
        """
        pass


if __name__ == '__main__':
    unittest.main()
