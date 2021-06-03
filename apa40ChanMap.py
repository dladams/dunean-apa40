from apa_mapping import APA_MAP

def getApa40Channels(spla):
  apamap = APA_MAP()
  print( apamap.APA)
  achs, xchs, uchs, vchs = apamap.apa_mapping()
  if spla == 'x': return xchs
  if spla == 'u': return uchs
  if spla == 'v': return vchs
  return []

def getApa40ChannelsMap():
  apamap = APA_MAP()
  print( apamap.APA)
  achs, xchs, uchs, vchs = apamap.apa_mapping()
  out = {
    'x': xchs,
    'u': uchs,
    'v': vchs
  }
  return out

def test_getApa40Channels():
  print(getApa40Channels('x'))
