class CruiseController:
  def __init__(self):
    self.mapping = self.__get_mappings()
    self.rule_base = self.__get_rules()
    self.speed_mf = self.__get_speed_mf()
    self.acc_mf = self.__get_acc_mf()
    self.throttle_vals = self.__get_throttle_vals()
    self.throttle_base = self.throttle_vals['PL'] - self.throttle_vals['ZE']

  def __get_mappings(self):
    return {
        'NL': 0, # Negative Large
        'NM': 1, # Negative Medium
        'ZE': 2, # Zero
        'PM': 3, # Positive Medium
        'PL': 4  # Positive Large
    }

  def __get_rules(self):
    return [
            ['PL', 'PL', 'PL', 'PM', 'ZE'],
            ['PL', 'PL', 'PM', 'ZE', 'NM'],
            ['PL', 'PM', 'ZE', 'NM', 'NL'],
            ['PM', 'ZE', 'NM', 'NL', 'NL'],
            ['ZE', 'NM', 'NL', 'NL', 'NL'],
    ]

  def __get_speed_mf(self):
    return {
        'NL': lambda x : 1 if x < -100 else (0 if x > -50 else -0.02*x - 1),
        'NM': lambda x : 0 if x < -100 or x > 0 else (0.02*x + 2 if x < -50 else -0.02*x),
        'ZE': lambda x : 0 if abs(x) > 50 else (0.02*x + 1 if x < 0 else -0.02*x + 1),
        'PM': lambda x : 0 if x > 100 or x < 0 else (-0.02*x + 2 if x > 50 else 0.02*x),
        'PL': lambda x : 1 if x > 100 else (0 if x < 50 else 0.02*x - 1)
    }

  def __get_acc_mf(self):
    return {
        'NL': lambda x : 1 if x < -40 else (0 if x > -20 else -0.05*x - 1),
        'NM': lambda x : 0 if x < -40 or x > 0 else (0.05*x + 2 if x < -20 else -0.05*x),
        'ZE': lambda x : 0 if abs(x) > 20 else (0.05*x + 1 if x < 0 else -0.05*x + 1),
        'PM': lambda x : 0 if x > 40 or x < 0 else (-0.05*x + 2 if x > 20 else 0.05*x),
        'PL': lambda x : 1 if x > 40 else (0 if x < 20 else 0.05*x - 1)
    }

  def __get_throttle_vals(self):
    return {
        'NL': -20,
        'NM': -10,
        'ZE':   0,
        'PM':  10,
        'PL':  20
    }

  def __crisp_to_fuzzy(self, val, mf):
    fuzzy_values = []
    for x, myu_x in mf.items():
      if myu_x(val) > 0: fuzzy_values.append((x, myu_x(val)))
    return fuzzy_values

  def __fuzzify(self, speed_diff, acc):
    return self.__crisp_to_fuzzy(speed_diff, self.speed_mf), self.__crisp_to_fuzzy(acc, self.acc_mf)

  def __apply_rule_base(self, speed, acc):
    throttle_fuzzy = []
    for s in speed:
      for a in acc:
        i, j = self.mapping[s[0]], self.mapping[a[0]]
        throttle_fuzzy.append((self.rule_base[i][j], min(s[1], a[1])))
    return throttle_fuzzy

  def __get_throttle_area(self, x):
    y = self.throttle_base * x
    return 0.5 * (self.throttle_base - (1 - x) * y)

  def __defuzzify(self, throttle_fuzzy):
    areas = []
    for tf in throttle_fuzzy:
      areas.append((self.throttle_vals[tf[0]], self.__get_throttle_area(tf[1])))
    throttle = 0
    total_area = 0
    for a in areas:
      throttle += a[0] * a[1]
      total_area += a[1]
    return throttle / total_area

  def get_throttle(self, speed_diff, acc):
    speed_fuzzy, acc_fuzzy = self.__fuzzify(speed_diff, acc)
    throttle_fuzzy = self.__apply_rule_base(speed_fuzzy, acc_fuzzy)
    throttle = self.__defuzzify(throttle_fuzzy)
    print(f'throttle is {throttle}')
    return throttle