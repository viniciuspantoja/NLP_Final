from query_zip_links import queryZip
from query_key_words import getDesiredLinks

class main():
    def __init__(self, list_of_words, month = 12, year = 2015, day = None):

        self.month = month
        self.year = year
        self.day = day
        self.list_of_words = list_of_words

        return None

    def get_full_links(self):
        if self.day == None:
            print('1')
            final_list = []
            for i in range(31):
                zip_links = queryZip(self.month, self.year, self.day)

                final_list.append(getDesiredLinks(self.list_of_words, zip_links.final()['SOURCEURL'])).getLinks()

            return final_list

        else:
            print('2')
            zip_links = queryZip(self.month, self.year, self.day)
            return getDesiredLinks(self.list_of_words, zip_links.final()['SOURCEURL']).getLinks()
