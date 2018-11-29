import validators
    
def validate_url(url):
    """
    Checks if the url string parameter follows a valid URL format,
    also appending the link scheme if missing.
    It returns the URL itself with its scheme or
    None if the parameter URL has an invalid format.
    """
    schemeSeparatorIndex = url.find("://");
    if (schemeSeparatorIndex < 3):
        # Adding default missing scheme for user.
        url = "http://" + url;
        
    if (not validators.url(url)):
        return None;
        
    return url;

def debugPrint(url):
    print("Test URL: '{0}', returned URL if valid: '{1}'".format(url, validate_url(url)));
        
if __name__ == "__main__":
    debugPrint("www.site.com");
    debugPrint("www.site.com.br");
    debugPrint("http://www.site.com.br/Rio/Python.html");
    debugPrint("https://www.site.com.br/Rio/Python.html&id=33");
    debugPrint("http://www.site.com");
    debugPrint("s.site.com");
    debugPrint("http://www.sitecom");
    debugPrint("htatp://www.site.com");
    debugPrint("htatpwwwsitecom");
    debugPrint("http://www.foo.bar./");
    debugPrint("http:///a");
    debugPrint("http://www.site.com?q=Spaces should be encoded");