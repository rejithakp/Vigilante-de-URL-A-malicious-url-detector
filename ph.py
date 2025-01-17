def getrank():
    import re
    f_csv = open('C:\\Users\\user\\Documents\\Phishing-URL-Detector-master\\static\\top-1m.csv')
    csv_data = f_csv.read()
    f_csv.close()
    lines = csv_data.split("\n")
    domain_list=[]
    for line in lines:
        try:
            url = line.split(",")[1]
            url = re.sub('^www\.', '', url)
            domain_list.append(url)
        except:
            continue

    print(domain_list)

    rank=-1
    url="http://www.google.com"
    from urllib.parse import urlparse
    ''' getrank returns the alexa rank of the domain of the given URL, or -1 if it is over 1M'''
    parsed_url = urlparse(url)

    domain = parsed_url.netloc
    domain = re.sub('^www\.', '', domain)
    if domain in domain_list:
        print(domain_list.index(domain)+1)
        rank=domain_list.index(domain)+1

    return rank


# import urlli
# import os
# import zipfile
# import re
# from urllib.request import urlopen
# class Alexa:
#     '''
#     this class provides access to the Alexa ranking of URLs
#     usage: create a new instance of this class (ranker = Alexa()) and use the getrank method
#     '''
#     __domain_list = []
#
#     def __init__(self):
#         try:
#             # download the file
#             f = open('top-1m.zip', 'wb')
#             opener = urllib.build_opener()
#             opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#             file = opener.open('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip').read()
#             f.write(file)
#             f.close()
#             # unzip it
#             current_dir = os.getcwd()
#             zip = zipfile.ZipFile(r'top-1m.zip')
#             zip.extractall(current_dir)
#             # read the alexa ranking
#             f_csv = open('top-1m.csv')
#             csv_data = f_csv.read()
#             f_csv.close()
#             lines = csv_data.split("\n")
#             for line in lines:
#                 try:
#                     url = line.split(",")[1]
#                     url = re.sub('^www\.', '', url)
#                     self.__domain_list.append(url)
#                 except:
#                     continue
#         except:
#             raise
#
#     def getrank(self, url):
#         ''' getrank returns the alexa rank of the domain of the given URL, or -1 if it is over 1M'''
#         parsed_url = urlparse.urlparse(url)
#         if parsed_url.scheme == '':
#             return self.getrank('http://' + url)
#         domain = parsed_url.netloc
#         domain = re.sub('^www\.', '', domain)
#         if domain in self.__domain_list:
#             return self.__domain_list.index(domain) + 1
#         return -1
# import os
# import zipfile
#
# class Alexa:
#     '''
#     this class provides access to the Alexa ranking of URLs
#     usage: create a new instance of this class (ranker = Alexa()) and use the getrank method
#     '''
#     __domain_list = []
#
#     def __init__(self):
#         try:
#             # download the file
#             f = open('top-1m.zip', 'wb')
#             opener = urllib.build_opener()
#             opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#             file = opener.open('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip').read()
#             f.write(file)
#             f.close()
#             # unzip it
#             current_dir =os.getcwd()
#             zip = zipfile.ZipFile(r'top-1m.zip')
#             zip.extractall(current_dir)
#             # read the alexa ranking
#             f_csv = open('top-1m.csv')
#             csv_data = f_csv.read()
#             f_csv.close()
#             lines = csv_data.split("\n")
#             for line in lines:
#                 try:
#                     url = line.split(",")[1]
#                     url = re.sub('^www\.', '', url)
#                     self.__domain_list.append(url)
#                 except:
#                     continue
#         except:
#             raise
#
#     def getrank(self, url):
#         ''' getrank returns the alexa rank of the domain of the given URL, or -1 if it is over 1M'''
#         parsed_url = urlparse.urlparse(url)
#         if parsed_url.scheme == '':
#             return self.getrank('http://'+url)
#         domain = parsed_url.netloc
#         domain = re.sub('^www\.', '', domain)
#         if domain in self.__domain_list:
#             return self.__domain_list.index(domain)+1
#         return -1
#
# c=Alexa()
# c.getrank("www.google.com")