
import re

class getDesiredLinks():
    def __init__(self, listOfKeyWords, links):

        self.listOfKeyWords = listOfKeyWords
        self.links = links

        print(links)

        return None

    def getLinks(self):
        pattern = ''
        for item in self.listOfKeyWords:
            item = item.replace(' ','-')
            pattern = pattern+'{}|'.format(item)

        pattern = pattern[:-1]

        desired_links = []

        for link in self.links:

            if len(re.findall(r'{}'.format(pattern), link))>0:
                desired_links.append(link)
            else:
                pass

        return desired_links
