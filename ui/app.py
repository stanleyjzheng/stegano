from flask import Flask, request
import os
import re
from google.cloud import storage
import numpy
import cv2
from PIL import Image

import binascii
import collections
import datetime
import hashlib
import sys

from google.oauth2 import service_account
import six
from six.moves.urllib.parse import quote


app = Flask(__name__)


@app.route("/api")
def hello():
    return "hello"


@app.route("/api/encode", methods=["POST"])
def upload():
    if request.method == "POST":
        print("processing....")
        # TODO: insert pytorch function here!
        # image_file = stego_function(request.files["file"])
        image_file = request.files["file"]
        signed_url = upload_blob(image_file)
        img = Image.open(image_file)
        return signed_url


def upload_blob(source_file, bucket_name="stego-upload-bucket"):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    destination_blob_name = (
        re.sub("(\.png|\.jpg)", "", source_file.filename) + "-stego.png"
    )
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file)

    print("File {} uploaded to {}.".format(source_file.filename, destination_blob_name))

    return generate_signed_url(
        "stego-upload-bucket",
        destination_blob_name,
    )


def generate_signed_url(
    bucket_name,
    object_name,
    service_account_file="./My First Project-f0e306c3d916.json",
    subresource=None,
    expiration=604800,
    http_method="GET",
    query_parameters=None,
    headers=None,
):

    if expiration > 604800:
        print("Expiration Time can't be longer than 604800 seconds (7 days).")
        sys.exit(1)

    escaped_object_name = quote(six.ensure_binary(object_name), safe=b"/~")
    canonical_uri = "/{}".format(escaped_object_name)

    datetime_now = datetime.datetime.utcnow()
    request_timestamp = datetime_now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = datetime_now.strftime("%Y%m%d")

    google_credentials = service_account.Credentials.from_service_account_file(
        service_account_file
    )
    client_email = google_credentials.service_account_email
    credential_scope = "{}/auto/storage/goog4_request".format(datestamp)
    credential = "{}/{}".format(client_email, credential_scope)

    if headers is None:
        headers = dict()
    host = "{}.storage.googleapis.com".format(bucket_name)
    headers["host"] = host

    canonical_headers = ""
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k, v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += "{}:{}\n".format(lower_k, strip_v)

    signed_headers = ""
    for k, _ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += "{};".format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'

    if query_parameters is None:
        query_parameters = dict()
    query_parameters["X-Goog-Algorithm"] = "GOOG4-RSA-SHA256"
    query_parameters["X-Goog-Credential"] = credential
    query_parameters["X-Goog-Date"] = request_timestamp
    query_parameters["X-Goog-Expires"] = expiration
    query_parameters["X-Goog-SignedHeaders"] = signed_headers
    if subresource:
        query_parameters[subresource] = ""

    canonical_query_string = ""
    ordered_query_parameters = collections.OrderedDict(sorted(query_parameters.items()))
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe="")
        encoded_v = quote(str(v), safe="")
        canonical_query_string += "{}={}&".format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing '&'

    canonical_request = "\n".join(
        [
            http_method,
            canonical_uri,
            canonical_query_string,
            canonical_headers,
            signed_headers,
            "UNSIGNED-PAYLOAD",
        ]
    )

    canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()

    string_to_sign = "\n".join(
        [
            "GOOG4-RSA-SHA256",
            request_timestamp,
            credential_scope,
            canonical_request_hash,
        ]
    )

    # signer.sign() signs using RSA-SHA256 with PKCS1v15 padding
    signature = binascii.hexlify(
        google_credentials.signer.sign(string_to_sign)
    ).decode()

    scheme_and_host = "{}://{}".format("https", host)
    signed_url = "{}{}?{}&x-goog-signature={}".format(
        scheme_and_host, canonical_uri, canonical_query_string, signature
    )

    return signed_url