from Require import *


class CalendarModel(QAbstractItemModel):
	def __init__(self, year=datetime.today().year, parent=None):
		super().__init__(parent)
		
		self.backbrace = QCalendar()
		self.skeleton = []
		self.finger = QDate()
		self.year = int(year)
		for month in range(12):
			self.skeleton.append([{} for day in range(self.backbrace.daysInMonth(month + 1, self.year))])
		self.array = np.array(self.skeleton, dtype=object)
		self.subdivision = QTreeView().model()
		self.model_role = Qt.UserRole + 2001
	
	def dataFor(self, month, day, role=None):
		self.finger.setDate(self.year, month, day)
		if role:
			return self.array[month][day][role]
		else:
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
	
	def rowCount(self, parent):
		return 31
	
	def columnCount(self, parent):
		return 12
	
	def get_finger(self):
		return self.finger
	
	def get_fingerDate(self):
		return self.finger.getDate()
	
	def setData(self, index, value, role):
		month = index.column()
		day = index.row()
		self.array[month][day][role] = value
	
	def days_inMonth(self, month):
		if month <= len(self.array):
			return len(self.array[month - 1])
		else:
			return False
		
	def index(self, row, column, parentIndex=QModelIndex()):
		if len(self.array) >= row:
			if len(self.array[row]) >= column:
				return self.createIndex(row, column)
		return QModelIndex()
		
	def get_node(self, index):
		if index.isValid():
			node = index.internalPointer()
			if node:
				return node
		return self.array
	
	def parent(self, index):
		node = self.get_node(index)
		parentNode = node.getParent()
		if parentNode == self.array:
			return QModelIndex()
		return self.createIndex(parentNode.row(), parentNode.column(), parentNode)
	
	def setupChildren(self, month, day):
		self.array[month][day][self.model_role] = QStandardItem()
	
	def addChild(self, month, day, content, title=None):
		if self.model_role in self.array[month][day]:
			pass
		else:
			self.setupChildren(month, day)
		e = QStandardItem()
		if title:
			e.setData(title, Qt.UserRole)
		e.setData(content, Qt.DisplayRole)
		self.array[month][day][self.model_role].setChild(self.array[month][day][self.model_role].rowCount(), e)
				
	def getChildren(self, month, day):
		if self.model_role in self.array[month][day]:
			return [{'title': self.dataFor(month, day, self.model_role).child(a).data(Qt.UserRole), 'text': self.dataFor(month, day, self.model_role).child(a).data(Qt.DisplayRole)} for a in range(self.array[month][day][self.model_role].rowCount())]
