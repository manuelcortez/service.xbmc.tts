# -*- coding: utf-8 -*-
import xbmc
import guitables
import windowparser
import skintables

class WindowReaderBase:
	ID = None
	def __init__(self,win_id=None):
		self._reset(win_id)

	def _reset(self,win_id):
		self.winID = win_id
		self.init()
		
	def init(self): pass

	def getName(self): return guitables.getWindowName(self.winID)

	def getHeading(self): return None

	def getWindowTexts(self): return None

	def getControlDescription(self,controlID): return None

	def getControlText(self,controlID):
		text = xbmc.getInfoLabel('System.CurrentControl').decode('utf-8')
		return (text,text)

	def getSecondaryText(self): return None
		
	def getItemExtraTexts(self,controlID): return None
	
	def getWindowExtraTexts(self):
		texts = guitables.getExtraTexts(self.winID)
		if not texts: texts = windowparser.getWindowParser().getWindowTexts()
		return texts or None
	
	def getMonitoredText(self,isSpeaking=False): return None
	
	def close(self): pass

class DefaultWindowReader(WindowReaderBase):
	ID = 'default'
	def getHeading(self):
		return xbmc.getInfoLabel('Control.GetLabel(1)').decode('utf-8') or u''
	
	def getWindowTexts(self):
		return guitables.getWindowTexts(self.winID)
	
	def getControlDescription(self,controlID):
		return skintables.getControlText(self.winID, controlID) or u''
		
	def getControlText(self,controlID):
		if not controlID: return (u'',u'')
		text = xbmc.getInfoLabel('ListItem.Title')
		if not text: text = xbmc.getInfoLabel('Container({0}).ListItem.Label'.format(controlID))
		if not text: text = xbmc.getInfoLabel('Control.GetLabel({0})'.format(controlID))
		if not text: text = xbmc.getInfoLabel('System.CurrentControl')
		if not text: return (u'',u'')
		compare = text + xbmc.getInfoLabel('ListItem.StartTime'.format(controlID)) + xbmc.getInfoLabel('ListItem.EndTime'.format(controlID))
		return (text.decode('utf-8'),compare)
	
	def getSecondaryText(self):
		return guitables.getListItemProperty(self.winID)
		
	def getItemExtraTexts(self,controlID):
		text = guitables.getItemExtraTexts(self.winID)
		if not text: text = xbmc.getInfoLabel('ListItem.Plot').decode('utf-8')
		if not text: text = xbmc.getInfoLabel('Container.ShowPlot').decode('utf-8')
		if not text: text = xbmc.getInfoLabel('ListItem.Property(Artist_Description)').decode('utf-8')
		if not text: text = xbmc.getInfoLabel('ListItem.Property(Album_Description)').decode('utf-8')
		if not text: text = xbmc.getInfoLabel('ListItem.Property(Addon.Description)').decode('utf-8')
		if not text: text = guitables.getSongInfo()
		if not text:
			text = windowparser.getWindowParser().getListItemTexts(controlID)
			current = self.getControlText(controlID)[0]
			if text:
				while current in text: text.pop(text.index(current))
				
		if not text: return None
		if not isinstance(text,(list,tuple)): text = [text]
		return text