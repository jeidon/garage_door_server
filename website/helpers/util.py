import datetime, calendar, math, zipfile, os, re, pytz, smtplib, hashlib
from django.conf import settings
from django.utils.timezone import utc

def sendEmail( recipient, subject, body ):
    FROM = settings.EMAIL_ACCESS['email']
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login( settings.EMAIL_ACCESS['email'], settings.EMAIL_ACCESS['password'] )
        server.sendmail(FROM, TO, message)
        server.close()
        print( 'successfully sent the mail' )
    except:
        print( "failed to send mail" )


def xlist( ary ):
    return list(ary) if ary is not None else []


def xtuple( tup ):
    return tuple(tup) if tup is not None else tuple()


def xstr( s, none='' ):
    return str(s) if s is not None else none


def xint( s, none=0, undefined=None ):
    try:
      if s == "undefined":
        return undefined
      return int(s) if s is not None and s != 'NaN' else none
    except ValueError:
        #Floating points and trailing letters wont fool me!!!
        m = re.search('^[-+]?[0-9]+', s)
        if m:
            return int(m.group(0))

        #can't go any further
        return none
    except TypeError:
        return none


def xfloat( s, none=0.0, undefined=None ):
    try:
        if s == "undefined":
            return undefined
        f = float(s) if s is not None and s != 'NaN' else none
        if math.isnan(f):
            return none
        return f
    except ValueError:
        #trailing letters wont fool me!!!
        m = re.search('^[-+]?[0-9]*\.?[0-9]+', s )
        if m:
            return float(m.group(0))

        #Can't go any further
        return none
    except TypeError:
        return none


def xbool( s, none=False, undefined=False ):
    #Are we string? try to figure out what that means
    if isinstance( s, str ):
        s = s.lower()
        if s == 'true':
            return True
        elif s == 'none' or s == 'null':
            return none
        elif s == 'undefined':
            return undefined
        else:
            return False

    #Special case none
    elif s is None:
        return none
    else:
        return bool(s)


# Cap a value between the given bounds
def cap( val, high, low=None ):
    if not low:
        low = -high
    if val > high:
        val = high
    elif val < low:
        val = low

    return val


# Provide a timezone
def toTimezone( tz=None ):
    timezone = utc
    if tz is not None:
        try:
            timezone = pytz.timezone(str(tz))
        except pytz.UnknownTimeZoneError:
            pass

    return timezone


# Return the hour differnce between two timezones
def tzToTz( to_tz, from_tz=None ): # None means UTC
    return round((unixNow(None, to_tz) - unixNow(None, from_tz)) / 3600000) # Hours


# Get the current time
def timeNow( ms=None, tz=None ):
    # Give the user their info
    ts = datetime.datetime.now( toTimezone(tz) )
    if ms:
        return ts + datetime.timedelta(milliseconds=xint(ms))
    else:
        return ts


# Convert a time to different timezone
def timeToTz( ts, tz ):
    return ts + datetime.timedelta(hours=tzToTz( tz )) - datetime.timedelta(hours=tzToTz("UTC", ts.tzinfo))


# Convert a time into epoch format
def timeToUnix( ts ):
    #print("%d == %d" % (int(ts.timestamp() * 1000.0), int(calendar.timegm( ts.timetuple()) * 1000)))

    return int(ts.timestamp() * 1000.0) if ts else 0
    #return (float(calendar.timegm( ts.timetuple())) * 1000.0) if ts else 0


# Current time in epoch format
def unixNow( ms=None, tz=None ):
    return timeToUnix( timeNow( ms, tz ) )


# Convert a time to different timezone
def unixToTz( unix, tz, from_tz="UTC" ):
    return unix + (tzToTz( tz ) - tzToTz("UTC", from_tz)) * 3600000


# Convert an epoch format into time
def unixToTime( ms, tz=None ):
    timezone = toTimezone(tz)
    return datetime.datetime.fromtimestamp( xfloat(ms) / 1000.0 ).replace(tzinfo=timezone)


def deltaToSeconds( d, digits=None ):
    ts = d.days * 86400000.0 + float(d.seconds) + float(d.microseconds / 1000.0)
    if digits:
        return round( math.fabs( ts ), digits )
    else:
        return math.fabs( ts )


def humanDate( date=None, add_sec=0, force_hours=False, force_full=False ):
    if date is None:
        date = timeNow()

    if isinstance( date, datetime.datetime ):
        return date.strftime( "%m/%d/%Y %I:%M:%S%p" )
    elif isinstance( date, datetime.timedelta ):
        date = int( deltaToSeconds( date ))

    # Return the delta
    date = int(date) + add_sec
    if date >= 3600 or force_full:
        return "%d:%02d:%02d" % (int(date / 3600), int((date / 60) % 60), int(date % 60))
    elif date >= 60:
        if force_hours:
            return "00:%02d:%02d" % (int((date / 60) % 60), int(date % 60))
        else:
            return "%d:%02d" % (int((date / 60) % 60), int(date % 60))
    elif date > 1:
        return "%d seconds" % int(date % 60)
    elif date == 1:
        return "%d second" % int(date % 60)
    else:
        return '0'


def createHash( arg1=None, arg2=None ):
    # Default args
    if arg1 is None:
        arg1 = unixNow()
    if arg2 is None:
        arg2 = settings.SECRET_KEY

    # Do hashing
    m = hashlib.sha256()
    m.update( xstr(arg1).encode('utf-8', 'ignore') )
    m.update( xstr(arg2).encode('utf-8', 'ignore') )
    return m.hexdigest()
