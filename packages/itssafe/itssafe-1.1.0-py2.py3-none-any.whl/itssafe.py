import six
import pytz
import base64
import datetime

ARBITRARY_EPOCH = 1293840000   # number of seconds of 1/1/2011 after 1/1/1970


class BadSignature(Exception):
    pass


class SignatureExpired(Exception):
    pass


def make_hmac_signature(string, key):
    import hmac
    import hashlib
    mac = hmac.new(key.encode('ascii'), string, hashlib.sha1)
    return base64.b64encode(mac.digest())


def get_secs_since_epoch():
    unix_epoch = pytz.utc.localize(datetime.datetime(1970, 1, 1))
    now = pytz.utc.localize(datetime.datetime.utcnow())
    now_in_secs = (now - unix_epoch).total_seconds()
    return now_in_secs - ARBITRARY_EPOCH


def sign(bytes_string, key):
    secs_since_epoch = get_secs_since_epoch()
    encoded_secs_since_epoch = base64.b64encode(six.text_type(secs_since_epoch).encode('ascii'))
    timestamped_data = bytes_string + b'.' + encoded_secs_since_epoch
    signature = make_hmac_signature(timestamped_data, key)
    signed_string = timestamped_data + b'.' + signature
    return signed_string


def unsign(bytes_string, key, max_age=10 * 60):
    timestamped_string, signature_in = bytes_string.rsplit(b'.', 1)
    signature_calced = make_hmac_signature(timestamped_string, key)
    if signature_calced != signature_in:
        raise BadSignature("signature '%s' does not match" % signature_in)
    string_res, timestamp = timestamped_string.rsplit(b'.', 1)
    decoded_timestamp_str = base64.b64decode(timestamp)
    try:
        decoded_timestamp = float(decoded_timestamp_str)
    except ValueError:
        raise BadSignature("timestamp does not decode to a float. timestamp = '%s'" % timestamp)
    secs_since_epoch = get_secs_since_epoch()
    time_diff = secs_since_epoch - decoded_timestamp
    if abs(time_diff) > max_age:
        raise SignatureExpired("decoded timestamp = '%s'; current seconds since epoch = '%s'; current - decoded = '%s'" % (decoded_timestamp, secs_since_epoch, time_diff))
    return string_res


# below functions are helpers for testing and debugging

def datetime_from_secs(secs):
    timestamp = secs + ARBITRARY_EPOCH
    return pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))


def to_chicago_time(a_time):
    chicago = pytz.timezone('America/Chicago')
    return a_time.astimezone(chicago)
