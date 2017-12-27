# -*- coding: utf-8 -*-
import re
meal = 'UA asasdas'
mealPattern = re.compile(r'^(\w{1,3})')
search_result = mealPattern.search(meal).group()

print type(search_result)


