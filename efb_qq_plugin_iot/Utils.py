import logging
import tempfile

import requests


def download_user_avatar(uid: str) -> tempfile:
    url = "https://q1.qlogo.cn/g?b=qq&nk={}&s=0".format(uid)
    return download_file(url)


def download_group_avatar(uid: str) -> tempfile:
    url = "https://p.qlogo.cn/gh/{}/{}/".format(uid, uid)
    return download_file(url)


def download_file(url: str, retry: int = 3) -> tempfile:
    """
    A function that downloads files from given URL
    Remember to close the file once you are done with the file!

    :param retry: The max retries before giving up
    :param url: The URL that points to the file
    """
    count = 1
    while True:
        try:
            file = tempfile.NamedTemporaryFile()
            r = requests.get(url, stream=True, timeout=10)
            r.raise_for_status()  # Replace this with better error handling.

            for chunk in r.iter_content(1024):
                file.write(chunk)
        except Exception as e:
            logging.getLogger(__name__).warning(f"Error occurred when downloading {url}. {e}")
            if count >= retry:
                logging.getLogger(__name__).warning(f"Maximum retry reached. Giving up.")
                raise e
            count += 1
        else:
            break
    return file


def process_quote_text(text: str, max_length: int) -> str:
    """
    Simple wrapper for processing quoted text

    :param text: Original text
    :param max_length: The max length before the string are truncated
    :return: Processed text
    """
    qt_txt = "%s" % text
    if max_length > 0:
        tgt_text = qt_txt[:max_length]
        if len(qt_txt) >= max_length:
            tgt_text += "…"
        tgt_text = "「%s」" % tgt_text
    elif max_length < 0:
        tgt_text = "「%s」" % qt_txt
    else:
        tgt_text = ""
    return tgt_text


def iot_at_user(uin: int):
    return f'[ATUSER({uin})]'
