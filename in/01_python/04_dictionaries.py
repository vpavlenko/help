{% section "Множества и словари" %}

{% subsection "Множества: set" %}
{% endsubsection %}

{% subsection "Словари: dict" %}
{% endsubsection %}

{% subsection "collections.defaultdict" %}

{% program "python" "participants/solution_with_dict.py" %}
import csv


f = open('olymp_success.csv', mode='r')
reader = csv.reader(f, delimiter = ',', quotechar = '"')


d = {}

for row in list(reader)[1]:
  print(row)
    nothing, name, subject, olymp_name, diplom, link1, link2, prize, comment, fact, *trash = row 

     if subject in d:
       olymps_for_subject = d[subject]
       if olymp_name in olymps_for_subject:
         olymps_for_subject[olymp_name].append(name)
       else:
         olymps_for_subject.append({olymp_name: [name]})
     else:
       d[subject] = {olymp_name: [name]}

for subject in d:
  print(subject)
  for olymp_name in d[subject]:
    print(olymp_name)
    for name in d[subject][olymp_name]:
      print(name)
{% endprogram %}

{% program "python" "participants/solution_with_defaultdict.py" %}
import csv
from collections import defaultdict

f = open('olymp_success.csv', 'r')
reader = csv.reader(f, delimiter = ',', quotechar = '"')


subjects =  defaultdict(lambda: defaultdict(lambda: []))

for row in reader:
    nothing, name, subject, olymp_name, diplom, link1, link2, prize, comment, fact, *trash =row 
    
    subjects[subject][olymp_name].append([name, diplom]) 
    

res = open('results.html', 'w')

for subject in subjects:
    print(subject, file = res)
    for olympiad in subjects[subject]:
        print(olympiad, file = res)
        print(subjects[subject][olympiad], file=res)

res.close()
f.close()
{% endprogram %}

{% endsubsection %}

{% endsection %}
