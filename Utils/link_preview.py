"""Port of src/Utils/link-preview.ts — get_url_info (link preview generation).

Fetches link preview info for a URL using the stdlib (no `link-preview-js` npm dep).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..WAProto import WAProto as proto
from .messages import prepare_wa_message_media

THUMBNAIL_WIDTH_PX = 192


def _get_compressed_jpeg_thumbnail(url, opts):
    from .messages_media import extract_image_thumb, to_buffer

    fetch_opts = opts.get('fetchOpts') or {}
    headers = fetch_opts.get('headers') or {}
    timeout = (fetch_opts.get('timeout') or 3000) / 1000.0
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        buf = resp.read()
    return extract_image_thumb(buf, opts.get('thumbnailWidth') or THUMBNAIL_WIDTH_PX)


def _fetch_html(url, fetch_opts):
    """Fetch + parse a URL into (title, description, images, final_url)."""
    headers = dict(fetch_opts.get('headers') or {})
    headers.setdefault('User-Agent', 'Mozilla/5.0 (compatible; Baileys/1.0)')
    timeout = (fetch_opts.get('timeout') or 3000) / 1000.0
    req = urllib.request.Request(url, headers=headers)
    final_url = url
    html = ''
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        final_url = resp.geturl()
        raw = resp.read(2_000_000)
        ctype = resp.headers.get('Content-Type', '')
        try:
            html = raw.decode('utf-8', errors='replace')
        except Exception:
            html = raw.decode('latin-1', errors='replace')
        if ctype and 'html' not in ctype.lower():
            return None
    return final_url, html


def _extract_meta(html):
    import re

    title = None
    description = None
    images = []
    og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
    if og_title:
        title = og_title.group(1)
    tw_title = re.search(r'<meta[^>]+name=["\']twitter:title["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
    if not title and tw_title:
        title = tw_title.group(1)
    if not title:
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
        title = m.group(1).strip() if m else None

    og_desc = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
    if og_desc:
        description = og_desc.group(1)
    tw_desc = re.search(r'<meta[^>]+name=["\']twitter:description["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
    if not description and tw_desc:
        description = tw_desc.group(1)

    for m in re.finditer(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']*)["\']', html, re.I):
        images.append(m.group(1))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I):
        images.append(m.group(1))
    return title, description, images


async def get_url_info(text, opts=None):
    """Given a piece of text, checks for any URL present, generates a link preview.

    Returns None if the fetch failed or no URL was found.
    """
    opts = opts or {
        'thumbnailWidth': THUMBNAIL_WIDTH_PX,
        'fetchOpts': {'timeout': 3000},
    }
    try:
        import re

        match = re.search(r'https?://[^\s<>"\']+', text)
        if not match:
            return None
        url = match.group(0)

        fetch_opts = opts.get('fetchOpts') or {}
        parsed = _fetch_html(url, fetch_opts)
        if not parsed:
            return None
        final_url, html = parsed
        title, description, images = _extract_meta(html)
        if not title:
            return None

        image = images[0] if images else None
        url_info = {
            'canonical-url': final_url,
            'matched-text': text,
            'title': title,
            'description': description,
            'originalThumbnailUrl': image,
        }

        if opts.get('uploadImage'):
            from .messages import _message_to_plain_dict

            result = await prepare_wa_message_media(
                {'image': {'url': image}} if image else {'image': {}},
                {
                    'upload': opts['uploadImage'],
                    'mediaTypeOverride': 'thumbnail-link',
                    'options': fetch_opts,
                },
            )
            url_info['jpegThumbnail'] = result.get('jpegThumbnail')
            url_info['highQualityThumbnail'] = result
        else:
            try:
                if image:
                    buf = _get_compressed_jpeg_thumbnail(image, opts)
                    url_info['jpegThumbnail'] = buf
            except Exception as error:
                logger = opts.get('logger')
                if logger is not None:
                    logger.debug({'err': getattr(error, 'stack', None), 'url': url}, 'error in generating thumbnail')

        return url_info
    except Exception as error:
        message = str(error)
        if 'receive a valid' not in message:
            raise error
    return None
