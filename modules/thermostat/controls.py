def simple(logdata, setpoint, diff):
  recent = logdata[-1]
  action = None
  if (recent['temp'] - setpoint) > diff:
    action = (True, False)
  elif (setpoint - recent['temp']) > diff:
    action = (False, True)
  else:
    action = (False, False)
  return action

def pd(logdata, setpoint, diff):
  pterm = 0.5
  dterm = 0.5
  recent = logdata[-1]
  secondrecent = logdata[-2]
  timediff = recent['time'] - secondrecent['time']
  tempdiff = recent['temp'] - secondrecent['temp']
  perror = recent['temp'] - setpoint
  derror = tempdiff / timediff
  error = pterm*perror + dterm*derror
  action = None
  if error > diff:
    action = (True, False)
  elif error < (diff*-1):
    action = (False, True)
  else:
    action = (False, False)
  return action

def pid(logdata, setpoint, diff):
  pterm = 0.5
  iterm = 0.1
  dterm = 0.5
  recent = logdata[-1]
  secondrecent = logdata[-2]
  timediff = recent['time'] - secondrecent['time']
  tempdiff = recent['temp'] - secondrecent['temp']
  numentries = len(logdata)
  isum = 0
  for i in logdata:
    isum += (i['temp'] - setpoint)
  ierror = isum / numentries
  perror = recent['temp'] - setpoint
  derror = tempdiff / timediff
  error = pterm*perror + iterm*ierror + dterm*derror
  action = None
  if error > diff:
    action = (True, False)
  elif error < (diff*-1):
    action = (False, True)
  else:
    action = (False, False)
  return action
