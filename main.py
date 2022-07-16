class CalendarModel(QAbstractItemModel):
	def __init__(self, year=datetime.today().year, parent=None):
		super().__init__(parent)
		
		self.backbrace = QCalendar()
		self.skeleton = []
		self.finger = QDate()
		self.year = int(year)
		for month in range(12):
			self.skeleton.append([{} for day in range(self.backbrace.daysInMonth(month+1, self.year))])
		self.array = np.array(self.skeleton, dtype=object)
		
	def dataFor(self, month, day):
		self.finger.setDate(self.year, month, day)
		return self.array[month][day]
	
	def nth_day(self, day_num):
		start_date = date(self.year, 1, 1)
		res_date = start_date + timedelta(days=int(day_num) - 1)
		return QDate(self.year, res_date.month, res_date.day)
	
	def to_datetime(self, month=None, day=None):
		if month and day:
			return QDate(self.year, month, day).toPython()
		else:
			return QDate(self.finger).toPython()
		
	def nth_dayData(self, day_num):
		start_date = date(self.year, 1, 1)
		res_date = start_date + timedelta(days=int(day_num) - 1)
		self.dataFor(res_date.month, res_date.day)
		
	def day_of_week(self, month=None, day=None):
		if month and day:
			return QDate(self.year, month, day).dayOfWeek()
		else:
			return self.finger.dayOfWeek()
		
	def data(self, index, role):
		month = index.column()
		day = index.row()
		if role in self.array[month][day].keys():
			return self.array[month][day][role]
		else:
			return False
