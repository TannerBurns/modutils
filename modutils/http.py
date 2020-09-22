import logging

from functools import partial
from requests import Session, Response
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
from smtplib import SMTP
from typing import Union, Text
from bs4 import BeautifulSoup
from re import findall

from modutils.decorators import aiobulk


class BaseSession(Session):
    retries: int
    verbose: bool

    def __init__(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16,
                 resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None):
        """initialize BaseSession

        :param max_retries: maximum amount of retries if non resolved status code found
        :param pool_connections: number of pool connection; default 16
        :param pool_maxsize: max number of connections in pool; default 16
        :param resolve_status_codes: extra status codes to resolve; default None
        :param verbose: more verbose logging output if response fails; default False
        :param auth: basic auth username and password tuple; default None
        """
        super().__init__()
        adapters = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                    max_retries=max_retries)
        self.mount("https://", adapters)
        self.mount('http://', adapters)
        self.retries = max_retries
        self.verbose = verbose
        self.resolve_status_codes = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 400, 401, 404]
        if isinstance(resolve_status_codes, int):
            self.resolve_status_codes.append(resolve_status_codes)
        elif isinstance(resolve_status_codes, list):
            for sc in resolve_status_codes:
                if isinstance(sc, int):
                    self.resolve_status_codes.append(sc)

        if auth:
            self.auth = HTTPBasicAuth(*auth)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.session_logger = logging.getLogger(name='BaseSession')
        self._log_msg_fmt = '{method}, {scheme}, {host}, {path}, {content_size}, {user_agent}, {status_code}'


    def log_response(self, response: Response) -> None:
        """log each requests/response from resolver"""
        self.session_logger.info(self._log_msg_fmt.format(
            scheme=response.url.split("://")[0], host=response.url.split('/')[2], method=response.request.method,
            path=response.request.path_url, status_code=response.status_code, content_size=len(response.content),
            user_agent=response.request.headers.get("User-Agent", "Unknown")))
        if response.status_code >= 300 and self.verbose:
            self.session_logger.error(f'RESPONSE: {response.text}')

    def session_request(self, request: partial) -> Response:
        """attempt to resolve a requests with an invalid status code

        if the status code of the requests is not one to resolve:
            Default:  [200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 400, 401, 404]
        the requests will be sent up to max_retries or until receiving an accepted status_code

        :param request: partial requests function to be used to attempt and resolve a valid response

        :return: response from the requests
        """
        attempt = 1
        resp = request()
        while attempt <= self.retries and resp.status_code not in self.resolve_status_codes:
            resp = request()
            attempt += 1
        self.log_response(resp)
        return resp

    def get(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session get
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).get, url, **kwargs))

    def head(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session head
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).head, url, **kwargs))

    def delete(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session delete
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).delete, url, **kwargs))

    def patch(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session patch
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).patch, url, **kwargs))

    def post(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session post
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).post, url, **kwargs))

    def put(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session put
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self.session_request(partial(super(BaseSession, self).put, url, **kwargs))


class BaseAsyncSession(BaseSession):

    def __init__(self, *args, **kwargs):
        """initialize BaseAsyncSession

        :param args: list of args
        :param kwargs: dict of named args
        """
        if 'pool_maxsize' not in kwargs:
            kwargs.update({'pool_maxsize': 32})
        if 'pool_connections' not in kwargs:
            kwargs.update({'pool_connections': 32})
        super().__init__(*args, **kwargs)


    @aiobulk
    def get(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession get
            aiobulk added self.get.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).get(url, ** kwargs)

    @aiobulk
    def head(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession head
            aiobulk added self.head.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).head(url, ** kwargs)

    @aiobulk
    def delete(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession delete
            aiobulk added self.delete.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).delete(url, ** kwargs)

    @aiobulk
    def patch(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession patch
            aiobulk added self.patch.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).patch(url, ** kwargs)

    @aiobulk
    def post(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession post
            aiobulk added self.post.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).post(url, ** kwargs)

    @aiobulk
    def put(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of BaseSession put
            aiobulk added self.put.bulk

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return super(BaseSession, self).put(url, ** kwargs)


class Email(object):

    def __init__(self, smtp_server, smtp_port, from_address: str = None,
                 authentication_required: bool = False, auth_username: str = None, auth_password: str = None):
        self.host = smtp_server
        self.port = smtp_port
        self.from_address = from_address
        self.smtp_session = SMTP(host=self.host, port=self.port)
        self.smtp_session.starttls()
        if authentication_required:
            if not auth_username:
                raise ValueError(f'{"auth_username"!r} cannot be NoneType if {"authentication_required"!r} is True')
            if not auth_password:
                raise ValueError(f'{"auth_password"!r} cannot be NoneType if {"authentication_required"!r} is True')
            self.smtp_session.login(auth_username, auth_password)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.email_logger = logging.getLogger(name='Mailer')
        self.log_msg_fmt = 'From: {from_address}, To: {to_addresses}, CC: {cc_addresses}, {subject}, ' \
                           'attachments: {attach_len}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp_session.quit()

    def send(self, subject: str, body: str, to_address_list: list, cc_address_list: list = None,
             from_address: str = None, encoding: str = 'html', logo_images: list = None,
             file_attachments: list = None) -> dict:
        """

        :param subject: Subject string for email, required
        :param body: Message content for email, required
        :param to_address_list: addresses to send email to, required
        :param cc_address_list: addresses to cc on email, default: None
        :param from_address: address to send email from, default: None, will use self.from_address if one was given
        :param encoding: encoding for body, default: html
        :param logo_images: list of paths to images to use for logos, default: None
        :param file_attachments: list of paths to attachments for email, default: None

        :return: dict
        """
        assert isinstance(to_address_list, list)
        email_from = from_address or self.from_address
        if not email_from:
            raise ValueError(f'{"email_from"!r} cannot be NoneType if {"from_address"!r} is not set.')

        email = MIMEMultipart()
        email['From'] = email_from
        email['To'] = ', '.join(to_address_list)
        email['Date'] = formatdate(localtime=True)
        if cc_address_list:
            assert isinstance(cc_address_list, list)
            email['Cc'] = ', '.join(cc_address_list)

        email['Subject'] = subject
        email.attach(MIMEText(body, encoding, 'utf-8'))

        if logo_images:
            for lpath in logo_images:
                with open(lpath, 'rb') as fin:
                    email.attach(MIMEImage(fin.read()))
        if file_attachments:
            for fpath in file_attachments:
                filename = basename(fpath)
                with open(fpath, 'rb') as fin:
                    attachment = MIMEApplication(fin.read(), Name=filename)
                    attachment['Content-Disposition'] = f'attachment; filename={filename}'
                    email.attach(attachment)

        full_address_list = to_address_list
        if cc_address_list:
            full_address_list.extend(cc_address_list)
        self.email_logger.info(self.log_msg_fmt.format(from_address=email_from,
                                                       to_addresses=', '.join(to_address_list),
                                                       cc_addresses=', '.join(cc_address_list)
                                                       if cc_address_list else 'None', subject=subject,
                                                       attach_len=len(file_attachments)
                                                       if file_attachments else 0
            )
        )
        return self.smtp_session.sendmail(email_from, full_address_list, email.as_string())


def urlscraper(url: str, pattern: str, regex:bool=False) -> list:
    """urlscraper is a simple method to scrape information from a url based on a given string pattern

    :param url: the url to run pattern against
    :param pattern: the string representation of the pattern
    :param regex: flag for using a pattern as regex or string compare

    :return: list of strings that matched or contained pattern
    """
    matches: list = []
    resp = BaseSession().get(url, headers={'User-Agent': 'Chrome Python3'})
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        if regex:
            matches.extend([match for text in soup.stripped_strings for match in findall(pattern, text)])
        else:
            matches.extend([text for text in soup.stripped_strings if pattern in text])
    return list(set(matches))

