#!/usr/bin/env python
# crate_anon/crateweb/extra/serve.py

"""
===============================================================================
    Copyright (C) 2015-2017 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.
===============================================================================
"""

import os
from typing import Union
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.http.response import HttpResponseBase
from django.utils.encoding import smart_str


# =============================================================================
# File serving
# =============================================================================

# I thought this function was superseded by django-filetransfers:
# http://nemesisdesign.net/blog/coding/django-private-file-upload-and-serving/
# https://www.allbuttonspressed.com/projects/django-filetransfers
# ... but it turns out that filetransfers.api.serve_file uses a file object,
# not a filename. Not impossible, but never mind.

def add_http_headers_for_attachment(response: HttpResponse,
                                    offered_filename: str = None,
                                    content_type: str = None,
                                    as_attachment: bool = False,
                                    as_inline: bool = False,
                                    content_length: int = None) -> None:
    """
    Add HTTP headers to a Django response class object.

    as_attachment: if True, browsers will generally save to disk.
        If False, they may display it inline.
        http://www.w3.org/Protocols/rfc2616/rfc2616-sec19.html
    as_inline: attempt to force inline (only if not as_attachment)
    """
    if offered_filename is None:
        offered_filename = ''
    if content_type is None:
        content_type = 'application/force-download'
    response['Content-Type'] = content_type
    if as_attachment:
        prefix = 'attachment; '
    elif as_inline:
        prefix = 'inline; '
    else:
        prefix = ''
    fname = 'filename=%s' % smart_str(offered_filename)
    response['Content-Disposition'] = prefix + fname
    if content_length is not None:
        response['Content-Length'] = content_length


def serve_file(path_to_file: str,
               offered_filename: str = None,
               content_type: str = None,
               as_attachment: bool = False,
               as_inline: bool = False) -> HttpResponseBase:
    """
    Serve up a file from disk.
    Two methods:
    (a) serve directly
    (b) serve by asking the web server to do so via the X-SendFile directive.
    """
    # http://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files  # noqa
    # https://docs.djangoproject.com/en/dev/ref/request-response/#telling-the-browser-to-treat-the-response-as-a-file-attachment  # noqa
    # https://djangosnippets.org/snippets/365/
    if offered_filename is None:
        offered_filename = os.path.basename(path_to_file) or ''
    if settings.XSENDFILE:
        response = HttpResponse()
        response['X-Sendfile'] = smart_str(path_to_file)
        content_length = os.path.getsize(path_to_file)
    else:
        response = FileResponse(open(path_to_file, mode='rb'))
        content_length = None
    add_http_headers_for_attachment(response,
                                    offered_filename=offered_filename,
                                    content_type=content_type,
                                    as_attachment=as_attachment,
                                    as_inline=as_inline,
                                    content_length=content_length)
    return response
    # Note for debugging: Chrome may request a file more than once (e.g. with a
    # GET request that's then marked 'canceled' in the Network tab of the
    # developer console); this is normal:
    #   http://stackoverflow.com/questions/4460661/what-to-do-with-chrome-sending-extra-requests  # noqa


def serve_buffer(data: bytes,
                 offered_filename: str = None,
                 content_type: str = None,
                 as_attachment: bool = True,
                 as_inline: bool = False) -> HttpResponse:
    """
    Serve up binary data from a buffer.
    Options as for serve_file().
    """
    response = HttpResponse(data)
    add_http_headers_for_attachment(response,
                                    offered_filename=offered_filename,
                                    content_type=content_type,
                                    as_attachment=as_attachment,
                                    as_inline=as_inline,
                                    content_length=len(data))
    return response


# =============================================================================
# Simpler versions
# =============================================================================

def add_download_filename(response: HttpResponse, filename: str) -> None:
    # https://docs.djangoproject.com/en/1.9/howto/outputting-csv/
    add_http_headers_for_attachment(response)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filename)


def file_response(data: Union[bytes, str],  # HttpResponse encodes str if req'd
                  content_type: str,
                  filename: str) -> HttpResponse:
    response = HttpResponse(data, content_type=content_type)
    add_download_filename(response, filename)
    return response
