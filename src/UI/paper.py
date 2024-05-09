
class Paper:
   def __init__(self, title, url, year, authors, isOpenAccess,paperId,openAccessPdf):
      self.paperId = paperId
      self.title = title
      self.url = url 
      self.year = year 
      self.authors = [name['name'] for name in authors]
      self.isOpenAcess = isOpenAccess
      self.openAccessPdf = openAccessPdf['url'] if openAccessPdf and isOpenAccess  else None
    
   def __str__(self) -> str:
       return f'''
       title: {self.title}\n
       nurl: {self.url}\n
       year: {self.year}\n
       authors: {', '.join(self.authors)}\n
       OpenAcess: {'Yes' if self.isOpenAcess else 'No'}\n
       PDFURL: {self.openAccessPdf}
       '''