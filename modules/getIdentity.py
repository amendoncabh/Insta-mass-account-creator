import random
import logging
import mechanicalsoup

def getRandomIdentity(country = 'it_it', gender = random.choice(["male", "female"])):
    logging.info("Gender: {gender}")
    language, country = country.split('_')
    URL = "https://%s.fakenamegenerator.com/gen-%s-%s-%s.php"%(language, gender, country, country)
    logging.info("Url generated: {}".format(URL))

    browser = mechanicalsoup.StatefulBrowser(
        raise_on_404=True,
        user_agent='MyBot/0.1'
    )

    page = browser.get(URL)

    info_div = page.soup.find(
        "div",
        { 'class': "info" }
    )
    address_div = info_div.soup.find(
        "div",
        { 'class': "address" }
    )
    extra_div = info_div.soup.find(
        "div",
        { 'class': "extra" }
    )
    all_extras = extra_div.soup.find_all(
        "dl",
        {'class': "dl-horizontal"}
    )

    identity = {}

    #Primary Information
    identity['fullname'] = address_div.find("h3").contents[0]
    identity['birthday'] = all_extras[5].find("dd").contents[0]
    identity['e-mail'] = all_extras[8].find("dd").contents[0]
    identity['address'] = address_div.find(
        "div",
        {'class': "adr"}
    ).contents

    logging.info("Identity:", identity)

    #Extra Information
    identity['email-generator'] = all_extras[8].find("dd").find("div").find("a").contents[0]
    return(identity, gender)
