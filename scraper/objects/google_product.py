class GoogleProduct:
    def __init__(self, productDiv):
        self.url = None
        self.imageUrl = None
        self.title = productDiv.find('a').get_text()
        self.price = None
        self.rating = 0
        self.reviewCount = 0
        self.store = None
        self.pricePercentile = None
        self.ratingPercentile = None
        self.reviewCountPercentile = None
        self.calculatedValue = None

        self.url = productDiv.find('a').get('href')
        if 'http://www.google.com' not in self.url and 'https://www.google.com' not in self.url:
            self.url = 'https://www.google.com' + self.url

        try:
            self.price = float(productDiv.find('span', class_='HRLxBb').get_text()[1:])
        except:
            self.price = None

        try:
            self.imageUrl = productDiv.find('div', class_='eUQRje').find('img').get('src')
        except:
            self.imageUrl = None

        try:
            self.rating = productDiv.find('div', class_='DApVsf')['aria-label']
            self.rating = self.rating.split()
            self.rating = float(self.rating[0])
        except:
            self.rating = 0

        try:
            potentialReviewTexts = productDiv.find('div', class_='d1BlKc').find_all()
            self.reviewCount = potentialReviewTexts[len(potentialReviewTexts) - 1]['aria-label']
            self.reviewCount = self.reviewCount.split()
            self.reviewCount = int(self.reviewCount[0])
        except:
            self.reviewCount = 0

        try:
            detailDivs = productDiv.find_all('div', class_='dD8iuc')
            self.store = productDiv.find_all('div', class_='dD8iuc')[len(detailDivs) - 1].get_text()
            self.store = self.store.split()
            self.store = self.store[2:]
            self.store = (' ').join(self.store)
        except:
            self.store = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

    def calculatePercentile(self, key, rank, dataCount):
        setattr(self, key, 100 * (rank / dataCount))

    def calculateValue(self, priceWeight, ratingWeight, reviewCountWeight):
        priceVal = priceWeight * self.pricePercentile
        ratingVal = ratingWeight * self.ratingPercentile
        reviewCountVal = reviewCountWeight * self.reviewCountPercentile

        self.calculatedValue = priceVal + ratingVal + reviewCountVal
