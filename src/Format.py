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
