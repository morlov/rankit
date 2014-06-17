import hmac

secret = 'jd;d*hskJ7lsjbGSdjsLuhsnh!jusjdsklLHFs'

def make_secure_val(s):
    return "%s|%s" % (s, hmac.new(secret, s).hexdigest())

def check_secure_val(h):
    if h:
        val = h.split('|')[0]
        if h == make_secure_val(val):
            return val