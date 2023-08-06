#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doc
"""

from __future__ import print_function
import os
from os.path import join
import jinja2
try:
    from .util import make_dir, make_file
    from .template import TC
    from .pkg import textfile
except:
    from docfly.util import make_dir, make_file
    from docfly.template import TC
    from docfly.pkg import textfile


class Article(object):
    """

    :param path: xxx/index.rst

    **中文文档**


    """

    def __init__(self, title, path):
        self.title = title
        self.path = path

    def __repr__(self):
        return "Article(title=%r)" % (self.title,)


class DocTree(object):
    """A DocTree structure following
    :ref:`Sanhe Sphinx standard <Sanhe_sphinx_doc_project_style_guide>`.
    """
    content_file = "_content.rst"

    def __init__(self, dir_path, content_file="_content.rst"):
        self.content_file = content_file
        if self.is_doc_dir(dir_path) is False:
            raise Exception
        self.dir_path = dir_path

    def is_doc_dir(self, dir_path):
        """

        **中文文档**

        检测该目录是否符合 :ref:`Sanhe Sphinx 文档标准 <Sanhe_sphinx_doc_project_style_guide>`:

        - 文件目录下是否有一个 ``content.rst`` 文件。
        """
        if os.path.exists(join(dir_path, self.content_file)):
            return True
        else:
            return False

    def get_doc_dir_list(self, dir_path):
        """

        **中文文档**

        获得文件夹中的所有子文档文件夹, 使用 :meth:`DocTree.is_doc_dir` 中的
        判断准则。
        """
        dir_list = list()
        for path in os.listdir(dir_path):
            abspath = join(dir_path, path)
            if self.is_doc_dir(abspath):
                dir_list.append(abspath)
        return dir_list

    @staticmethod
    def get_title(abspath):
        """

        **中文文档**

        从一个.rst文件中, 找到顶级标题。也就是第一个 ``====`` 上面一行。如果没有
        ``====``, 那么 ``----`` 也行。
        """
        lastline = None
        for line in textfile.readlines(abspath, strip="both"):
            if (line == "=" * len(line)) and (len(line) >= 1):
                return lastline.strip()
            else:
                lastline = line

        lastline = None
        for line in textfile.readlines(abspath, strip="both"):
            if (line == "-" * len(line)) and (len(line) >= 1):
                print("Warning, this document doesn't have '======' header, "
                      "But having a `------` header!")
                return lastline.strip()
            else:
                lastline = line

        return None

    def process(self, dir_path, table_of_content_header):
        """

        **中文文档**

        处理一个文件夹。
        """
        article_list = list()

        for sub_dir_path in self.get_doc_dir_list(dir_path):
            abspath = join(sub_dir_path, self.content_file)
            title = DocTree.get_title(abspath)
            path = os.path.basename(sub_dir_path) + "/index.rst"
            article = Article(title=title, path=path)
            article_list.append(article)

        # read content from content.rst
        content = textfile.read(join(dir_path, self.content_file))

        # replace ``.. articles::`` directives
        content = content.replace(
            ".. articles::",
            TC.toc.render(
                header=table_of_content_header,
                article_list=article_list,
            ),
        )

        # write to index.rst
        make_file(join(dir_path, "index.rst"), content)

    def fly(self, table_of_content_header="Table of Content"):
        for current_dir, dir_list, file_list in os.walk(self.dir_path):
            if self.is_doc_dir(current_dir):
                self.process(current_dir, table_of_content_header)
