#
# Format conversion routines
#

# Convert number in string format to float 
def StringToFloat(s):

    # Parameter check
    if not s:
        return None
    
    # Remove commas
    s = str(s).replace(",", "")

    # Strip leading dollar sign, if any
    if s[0] == "$":
        s = s[1:]

    try:
        f = float(s)
    except:
        return None

    return f

# Convert float to string, with decimals precision
def FloatToString(f, precision):

    # Parameter check
    if not f:
        return None

    if precision < 0:
        return None

    # Round the number
    f = round(f, precision)
    
    # Truncate to integer
    f_int = int(f)
    if (f_int == f):
        return "{:,}".format(f_int)

    # Print with 2 decimals precision if possible
    if (precision > 2):
        f_rounded2 = round(f, 2)
        if (f_rounded2 == f):
            return "{:,.2f}".format(f_rounded2)

    # Print with 3 decimals precision if possible
    if (precision > 3):
        f_rounded3 = round(f, 3)
        if (f_rounded3 == f):
            return "{:,.3f}".format(f_rounded3)

    # Print with general decimal precision
    fmt = "{:,.%df}" % precision
    return fmt.format(f)
