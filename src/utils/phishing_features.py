import asyncio
import re
import socket
import ssl
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse

import aiohttp
import dns.resolver
import tldextract
import whois
from bs4 import BeautifulSoup
from cachetools import TTLCache
from logger.logger import logger

FEATURE_NAMES = [
    "having_ip_address",
    "url_length",
    "shortining_service",
    "having_at_symbol",
    "double_slash_redirecting",
    "prefix_suffix",
    "having_sub_domain",
    "sslfinal_state",
    "domain_registeration_length",
    "favicon",
    "port",
    "https_token",
    "request_url",
    "url_of_anchor",
    "links_in_tags",
    "sfh",
    "submitting_to_email",
    "abnormal_url",
    "redirect",
    "on_mouseover",
    "rightclick",
    "popupwidnow",
    "iframe",
    "age_of_domain",
    "dnsrecord",
    "web_traffic",
    "page_rank",
    "google_index",
    "links_pointing_to_page",
    "statistical_report",
    "result",
]


class PhishingFeatureExtractor:
    """Optimized class for extracting phishing detection features from URLs"""

    def __init__(self, use_api=True, verify_ssl=True, cache_ttl=3600):
        """
        Initialize the feature extractor

        Args:
            use_api (bool): Whether to use external APIs
            verify_ssl (bool): Whether to verify SSL certificates
            cache_ttl (int): Cache TTL in seconds
        """
        self.use_api = use_api
        self.verify_ssl = verify_ssl
        self.shortening_services = [
            "bit.ly",
            "goo.gl",
            "tinyurl.com",
            "t.co",
            "is.gd",
            "shorte.st",
            "ow.ly",
            "buff.ly",
            "tiny.cc",
            "lnkd.in",
        ]
        self.cache = TTLCache(maxsize=1000, ttl=cache_ttl)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.session = None

    async def __aenter__(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110"
            },
            timeout=aiohttp.ClientTimeout(total=10),
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
        self.executor.shutdown(wait=True)

    async def extract_features(self, url):
        """
        Extract features from a URL for phishing detection.

        Args:
            url (str): The URL to analyze

        Returns:
            list: Feature values in the order defined by FEATURE_NAMES
        """
        features = OrderedDict((feature, -1) for feature in FEATURE_NAMES)

        # Normalize and parse URL
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        try:
            parsed_url = urlparse(url)
            extract_result = tldextract.extract(url)
            domain = f"{extract_result.domain}.{extract_result.suffix}"
            subdomain = extract_result.subdomain
            logger.info(f"Analyzing URL: {url}, Domain: {domain}")
        except Exception as e:
            logger.error(f"URL parsing error: {str(e)}")
            return list(features.values())

        # Basic URL-based features
        features.update(self._extract_url_features(url, parsed_url, domain, subdomain))

        # Asynchronous feature extraction
        async with self:
            tasks = [
                self._check_ssl_certificate(domain),
                self._check_domain_info(domain),
                self._fetch_webpage_features(url, domain, parsed_url),
            ]
            if self.use_api:
                tasks.extend(
                    [
                        self._check_web_traffic(domain),
                        self._check_page_rank(domain),
                        self._check_google_safebrowsing(url),
                        self._check_backlinks(domain),
                        self._check_phishtank(url),
                    ]
                )

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for result, feature_names in [
                (results[0], ["sslfinal_state"]),
                (
                    results[1],
                    ["domain_registeration_length", "age_of_domain", "dnsrecord"],
                ),
                (
                    results[2],
                    [
                        "favicon",
                        "port",
                        "https_token",
                        "request_url",
                        "url_of_anchor",
                        "links_in_tags",
                        "sfh",
                        "submitting_to_email",
                        "abnormal_url",
                        "redirect",
                        "on_mouseover",
                        "rightclick",
                        "popupwidnow",
                        "iframe",
                    ],
                ),
                (results[3] if self.use_api else -1, ["web_traffic"]),
                (results[4] if self.use_api else -1, ["page_rank"]),
                (results[5] if self.use_api else -1, ["google_index"]),
                (results[6] if self.use_api else -1, ["links_pointing_to_page"]),
                (results[7] if self.use_api else -1, ["statistical_report"]),
            ]:
                if isinstance(result, Exception):
                    logger.error(f"Feature extraction error: {str(result)}")
                elif isinstance(result, dict):
                    features.update(result)
                else:
                    for name in feature_names:
                        features[name] = result

        return [features[feature] for feature in FEATURE_NAMES]

    def _extract_url_features(self, url, parsed_url, domain, subdomain):
        """Extract features that don't require network calls"""
        features = {}

        # 1. having_ip_address
        ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        ipv6_pattern = r"^[0-9a-fA-F:]+$"
        features["having_ip_address"] = (
            1
            if re.match(ip_pattern, parsed_url.netloc)
            or re.match(ipv6_pattern, parsed_url.netloc)
            else -1
        )

        # 2. url_length
        url_len = len(url)
        features["url_length"] = -1 if url_len < 54 else 0 if url_len <= 75 else 1

        # 3. shortining_service
        features["shortining_service"] = (
            1 if any(service in domain for service in self.shortening_services) else -1
        )

        # 4. having_at_symbol
        features["having_at_symbol"] = 1 if "@" in url else -1

        # 5. double_slash_redirecting
        path_and_query = parsed_url.path + (
            "?" + parsed_url.query if parsed_url.query else ""
        )
        features["double_slash_redirecting"] = 1 if "//" in path_and_query else -1

        # 6. prefix_suffix
        features["prefix_suffix"] = 1 if "-" in domain else -1

        # 7. having_sub_domain
        features["having_sub_domain"] = (
            -1 if not subdomain else 0 if subdomain.count(".") == 0 else 1
        )

        # 18. abnormal_url
        features["abnormal_url"] = 1 if domain not in url else -1

        return features

    async def _check_ssl_certificate(self, domain):
        """Check SSL certificate in a separate thread"""

        def sync_check():
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        return 1 if ssock.getpeercert().get("notAfter") else -1
            except Exception as e:
                logger.info(f"SSL check error for {domain}: {str(e)}")
                return -1

        return await asyncio.get_event_loop().run_in_executor(self.executor, sync_check)

    async def _check_domain_info(self, domain):
        """Check domain registration, age, and DNS records"""
        features = {}

        # WHOIS lookup (cached)
        cache_key = f"whois_{domain}"
        if cache_key in self.cache:
            domain_info = self.cache[cache_key]
        else:
            try:
                domain_info = await asyncio.get_event_loop().run_in_executor(
                    self.executor, lambda: whois.whois(domain)
                )
                self.cache[cache_key] = domain_info
            except Exception as e:
                logger.info(f"WHOIS error for {domain}: {str(e)}")
                domain_info = None

        # Domain registration length and age
        if domain_info and domain_info.creation_date and domain_info.expiration_date:
            creation_date = (
                domain_info.creation_date[0]
                if isinstance(domain_info.creation_date, list)
                else domain_info.creation_date
            )
            expiration_date = (
                domain_info.expiration_date[0]
                if isinstance(domain_info.expiration_date, list)
                else domain_info.expiration_date
            )
            registration_length = (expiration_date - creation_date).days
            domain_age = (datetime.now() - creation_date).days
            features["domain_registeration_length"] = (
                -1 if registration_length <= 365 else 1
            )
            features["age_of_domain"] = -1 if domain_age <= 180 else 1
        else:
            features["domain_registeration_length"] = -1
            features["age_of_domain"] = -1

        # DNS record
        try:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: dns.resolver.resolve(domain, "A")
            )
            features["dnsrecord"] = 1
        except Exception:
            features["dnsrecord"] = -1

        return features

    async def _fetch_webpage_features(self, url, domain, parsed_url):
        """Fetch and analyze webpage content"""
        features = {}

        try:
            async with self.session.get(url, ssl=self.verify_ssl) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")

                # Batch DOM-based feature extraction
                features.update(
                    {
                        "favicon": self._check_favicon(soup, domain, parsed_url),
                        "port": (
                            1
                            if parsed_url.port is None
                            or parsed_url.port in [80, 443, 21, 22]
                            else -1
                        ),
                        "https_token": 1 if "https" in domain else -1,
                        "request_url": self._analyze_external_resources(
                            soup, domain, "img", "src"
                        ),
                        "url_of_anchor": self._analyze_anchor_tags(soup, domain),
                        "links_in_tags": self._analyze_external_resources_in_tags(
                            soup, domain
                        ),
                        "sfh": self._analyze_form_actions(soup, domain),
                        "submitting_to_email": self._check_email_submission(soup),
                        "redirect": (
                            -1
                            if len(response.history) == 0
                            else 0
                            if len(response.history) == 1
                            else 1
                        ),
                        "on_mouseover": (
                            1
                            if "onmouseover" in html.lower()
                            and (
                                "window.location" in html.lower()
                                or "window.status" in html.lower()
                            )
                            else -1
                        ),
                        "rightclick": (
                            1
                            if any(
                                p in html.lower()
                                for p in [
                                    "event.button==2",
                                    'oncontextmenu="return false"',
                                    "oncontextmenu=",
                                ]
                            )
                            else -1
                        ),
                        "popupwidnow": (
                            1
                            if any(
                                p in html.lower()
                                for p in ["window.open(", "alert(", "prompt("]
                            )
                            else -1
                        ),
                        "iframe": 1 if soup.find("iframe") else -1,
                    }
                )
        except Exception as e:
            logger.error(f"Webpage fetch error for {url}: {str(e)}")

        return features

    def _check_favicon(self, soup, domain, parsed_url):
        """Check if favicon is from the same domain"""
        favicon_tags = soup.find_all("link", rel=lambda x: x and "icon" in x.lower())
        if not favicon_tags:
            return -1
        for tag in favicon_tags:
            if tag.get("href", "").startswith(("http", "//")):
                favicon_domain = tldextract.extract(tag["href"]).registered_domain
                if favicon_domain == domain:
                    return 1
        return -1

    def _analyze_external_resources(self, soup, domain, tag_name, attr_name):
        """Analyze external resources ratio"""
        tags = soup.find_all(tag_name)
        if not tags:
            return -1
        external = sum(
            1
            for tag in tags
            if tag.get(attr_name, "").startswith("http")
            and tldextract.extract(tag[attr_name]).registered_domain != domain
        )
        ratio = external / len(tags)
        return -1 if ratio < 0.22 else 0 if ratio <= 0.61 else 1

    def _analyze_anchor_tags(self, soup, domain):
        """Analyze anchor tags"""
        a_tags = soup.find_all("a")
        if not a_tags:
            return -1
        suspicious = sum(
            1
            for a in a_tags
            if a.get("href", "") in ["#", "javascript:void(0)"]
            or "javascript:" in a.get("href", "")
            or (
                a.get("href", "").startswith("http")
                and tldextract.extract(a["href"]).registered_domain != domain
            )
        )
        ratio = suspicious / len(a_tags)
        return -1 if ratio < 0.31 else 0 if ratio <= 0.67 else 1

    def _analyze_external_resources_in_tags(self, soup, domain):
        """Analyze external resources in meta, script, link tags"""
        tags = soup.find_all(["meta", "script", "link"])
        if not tags:
            return -1
        suspicious = sum(
            1
            for tag in tags
            if (tag.get("src", "") or tag.get("href", "")).startswith("http")
            and tldextract.extract(tag.get("src") or tag.get("href")).registered_domain
            != domain
        )
        ratio = suspicious / len(tags)
        return -1 if ratio < 0.17 else 0 if ratio <= 0.81 else 1

    def _analyze_form_actions(self, soup, domain):
        """Analyze form actions"""
        forms = soup.find_all("form")
        if not forms:
            return -1
        for form in forms:
            action = form.get("action", "")
            if action in ["", "about:blank"]:
                return 0
            if (
                action.startswith("http")
                and tldextract.extract(action).registered_domain != domain
            ):
                return 1
        return -1

    def _check_email_submission(self, soup):
        """Check for email submission"""
        if (
            soup.select('a[href^="mailto:"]')
            or any(
                "mailto:" in form.get("action", "") for form in soup.find_all("form")
            )
            or any(
                "mail(" in script.text
                for script in soup.find_all("script")
                if script.text
            )
        ):
            return 1
        return -1

    async def _check_web_traffic(self, domain):
        """Mock web traffic check"""
        return -1  # Replace with actual API call in production

    async def _check_page_rank(self, domain):
        """Mock page rank check"""
        return -1  # Replace with actual API call in production

    async def _check_google_safebrowsing(self, url):
        """Mock Google Safe Browsing check"""
        return -1  # Replace with actual API call in production

    async def _check_backlinks(self, domain):
        """Mock backlinks check"""
        return -1  # Replace with actual API call in production

    async def _check_phishtank(self, url):
        """Mock PhishTank check"""
        return -1  # Replace with actual API call in production


class PhishingDetector:
    """Class for detecting phishing URLs"""

    def __init__(self, model_path=None, use_api=True, verify_ssl=True):
        self.feature_extractor = PhishingFeatureExtractor(use_api, verify_ssl)
        self.model = None
        if model_path:
            self._load_model(model_path)

    def _load_model(self, model_path):
        logger.info(f"Model loading not implemented: {model_path}")

    async def extract_features_only(self, url):
        """Extract features without prediction"""
        features = await self.feature_extractor.extract_features(url)
        return dict(zip(FEATURE_NAMES, features))


async def get_features(url):
    """Main function for command line usage"""
    logger.info("Starting feature extraction")
    detector = PhishingDetector(use_api=True, verify_ssl=True)
    features = await detector.extract_features_only(url)
    fea = []
    for i, (name, value) in enumerate(features.items()):
        if name == "result":
            continue
        fea.append(value)

    return fea
