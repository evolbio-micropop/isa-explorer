__author__ = 'agbeltran'

import requests
from urllib.parse import urljoin
import zipfile

class CrossRefCient:

    CROSS_REF_API_BASE_URL = "http://api.crossref.org"
    TIMEOUT = 5

    def getURLPiecesWorksByScientificData(self):
        ScientificDataISSN = "2052-4463"
        r = requests.get(urljoin(self.CROSS_REF_API_BASE_URL, "/journals/"+ScientificDataISSN+"/works?rows=1000"), timeout=self.TIMEOUT)
        json_result = r.json()
        total_results = json_result["message"]["total-results"]
        items = json_result["message"]["items"]
        print("total_results ", total_results)
        url_pieces = []
        for item in items:
            sdata_identifer = item["alternative-id"][0]
            article_number = sdata_identifer[9:]
            accepted_year = sdata_identifer[5:9]
            published_year = item["deposited"]["date-parts"][0][0]
            url_pieces.append( ( published_year, accepted_year, article_number, sdata_identifer) )
        return url_pieces

def download(url, file_name):
    # get request
    response = requests.get(url)
    if response.status_code == 404:
        return response.status_code
    # open in binary mode
    with open(file_name, "wb") as file:
        # write to file
        file.write(response.content)
    file.close()
    return response.status_code

if __name__ == "__main__":
    client = CrossRefCient()
    url_pieces_array = client.getURLPiecesWorksByScientificData()
    for url_pieces in url_pieces_array:
        url = 'http://www.nature.com/article-assets/npg/sdata/{0}/sdata{1}{2}/isa-tab/sdata{1}{2}-isa1.zip'.format(*url_pieces)
        print(url)
        file_name = './data/{}-isa1.zip'.format(url_pieces[3])
        status_code = download(url, file_name)
        if status_code!=404:
            print("downloaded...", url_pieces[3])
            zip_ref = zipfile.ZipFile(file_name, 'r')
            zip_ref.extractall("./data/"+url_pieces[3])
            zip_ref.close()


# case where accepted_year differs from published_year
# http://www.nature.com/articles/sdata201575
# http://www.nature.com/article-assets/npg/sdata/2016/sdata201575/isa-tab/sdata201575-isa1.zip
# sdata201575 --> accepted year
# deposited 2016  --> published year