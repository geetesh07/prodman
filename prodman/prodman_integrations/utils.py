import base64
import hashlib
import hmac
from urllib.parse import urlparse

import nts
from nts import _


def validate_webhooks_request(doctype, hmac_key, secret_key="secret"):
	def innerfn(fn):
		settings = nts.get_doc(doctype)

		if nts.request and settings and settings.get(secret_key) and not nts.flags.in_test:
			sig = base64.b64encode(
				hmac.new(
					settings.get(secret_key).encode("utf8"), nts.request.data, hashlib.sha256
				).digest()
			)

			if nts.request.data and not sig == bytes(nts.get_request_header(hmac_key).encode()):
				nts.throw(_("Unverified Webhook Data"))
			nts.set_user(settings.modified_by)

		return fn

	return innerfn


def get_webhook_address(connector_name, method, exclude_uri=False, force_https=False):
	endpoint = f"prodman.prodman_integrations.connectors.{connector_name}.{method}"

	if exclude_uri:
		return endpoint

	try:
		url = nts.request.url
	except RuntimeError:
		url = "http://localhost:8000"

	url_data = urlparse(url)
	scheme = "https" if force_https else url_data.scheme
	netloc = url_data.netloc

	server_url = f"{scheme}://{netloc}/api/method/{endpoint}"

	return server_url


def get_tracking_url(carrier, tracking_number):
	# Return the formatted Tracking URL.
	tracking_url = ""
	url_reference = nts.get_value("Parcel Service", carrier, "url_reference")
	if url_reference:
		tracking_url = nts.render_template(url_reference, {"tracking_number": tracking_number})
	return tracking_url
