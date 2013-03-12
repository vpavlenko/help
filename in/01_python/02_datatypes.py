{% section "Типы данных" %}

{% subsection "Числа: int и float" %}
В Питоне имеется один тип данных для хранения целых чисел неограниченной длины (int)
и один тип данных для 64-битных вещественных чисел (float). Над ними можно выполнять обычные операции,
как в языках с Си-подобным синтаксисом (+, -, *, %, |, &, ^). Кроме того существует операция возведения в степень (**).
Имеются двоичные (префикс 0b), восьмеричные (префикс 0o) и шестнадцатеричные (префикс 0x) литералы. 
Операция деления (/) всегда возвращает тип float.
Целочисленное деление выполняется операцией //.

{% program "python" %}
>>> 2 ** 100
1267650600228229401496703205376
>>> 0b1100 & 0b1010
8
>>> 0b1100 | 0b1010
14
>>> 0xdeadbeef / 3
1245309519.6666667
>>> 0xdeadbeef // 3
1245309519
{% endprogram %}

Преобразования типов в Питоне не осуществляются автоматические. Преобразования объекта some_object
в тип SomeType осуществляются вызовом конструктора SomeType(some_object). 

{% program "python" %}
>>> float(5)
5.0
>>> int(5.2)   # преобразование float -> int идёт с округлением к нулю
5
>>> int(5.8)
5
>>> int(-5.2)
-5
{% endprogram %}

Операции округления вверх/вниз содержатся в модуле math. Для их импорта существует несколько способов.

<u>Способ 1</u>: импорт модуля.
{% program "python" %}
>>> import math
>>> math.floor(5.2)
5
>>> math.ceil(5.8)
6
{% endprogram %}

<u>Способ 2</u>: импорт конкретных функции из модуля.
{% program "python" %}
>>>
>>> math.floor(5.2)
5
>>> math.ceil(5.8)
6
{% endprogram %}
{% endsubsection %}

{% subsection "Строки: str" %}
Строковые литералы записываются в одинарных или тройных апострофах или кавычках. 
В Питоне всё &mdash; объект: числа, строки, функции, классы. Над объектами-строками
определено множество стандартных методов. Строки поддерживают индексацию натуральными числами (с нуля),
а также отрицательными числами (от конца строки к началу). Отдельного типа данных &laquo;символ&raquo;
в Питоне не существует: символ является строкой длины 1.
{% program "python" %}
$ ipython3
s = Python 3.2.3 (default, Oct 19 2012, 19:53:16) 
Type "copyright", "credits" or "license" for more information.

IPython 0.13.1.rc2 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: s = 'abc'

In [2]: t = 'def'

In [3]: s + t
Out[3]: 'abcdef'

In [4]: s[0]
Out[4]: 'a'

In [5]: s[-1]
Out[5]: 'c'

In [6]: s.
s.capitalize    s.expandtabs    s.isalnum       s.islower       s.isupper       
s.maketrans     s.rjust         s.splitlines    s.translate     s.center        
s.find          s.isalpha       s.isnumeric     s.join          s.partition     
s.rpartition    s.startswith    s.upper         s.count         s.format        
s.isdecimal     s.isprintable   s.ljust         s.replace       s.rsplit        
s.strip         s.zfill         s.encode        s.format_map    s.isdigit       
s.isspace       s.lower         s.rfind         s.rstrip        s.swapcase      
s.endswith      s.index         s.isidentifier  s.istitle       s.lstrip        
s.rindex        s.split         s.title         

In [6]: s.capitalize()
Out[6]: 'Abc'

In [7]: s.find('c')
Out[7]: 2

In [8]: s.find('d')
Out[8]: -1

In [9]: len(s)
Out[9]: 3
{% endprogram %}

Строки являются неизменяемыми
объектами: невозможно изменить символ в созданной строке (попробуйте это сделать).

Неявные преобразования из строки в число и из числа в строку не выполняются. При преобразовании 
из строки в число можно указать систему счисления. Также есть специальные функции для преобразования
из числа в двоичное/восьмеричное/шестнадцатеричное представление.

{% program "python" %}
>>> str(5.8)
'5.8'
>>> int('3')
3
>>> float('5.8')
5.8
>>> int('14', 16)
20
>>> int('14', base=16)
20
>>> int('14', base=5)
9
>>> bin(42)
'0b101010'
>>> oct(42)
'0o52'
>>> hex(42)
'0x2a'
{% endprogram %}
{% endsubsection %}

{% subsection "Списки: list" %}
Основной структурой данных для хранения объектов с поддержкой индексации являются списки.
Список &mdash; это расширяемый набор ссылок на объекты в памяти. Вообще, в Питоне нет понятия &laquo;переменная&raquo;,
есть только объекты и имена, хранящие ссылки на объекты.

{% program "python" %}
>>> a = [1, 5.2, 'abcd']
>>> len(a)
3
>>> a[0]
1
>>> a[-1]
'abcd'
{% endprogram %}

Несмотря на название, списки реализованы вовсе не на основе односвязных или двусвязных списков.
Внутри списки представляют собой расширяющийся массив (такой же, как контейнер std::vector в языке <nobr>С++</nobr>).
Поэтому списки поддерживают методы для добавления элементов в конец за <nobr>O(1)</nobr>, а также вставки и добавления
элементов в произвольное место за <nobr>O(n)</nobr>.

{% program "python" %}
>>> a = [1, 5.2, 'abcd']
>>> a.append('def')
>>> a
[1, 5.2, 'abcd', 'def']
>>> a.insert(2, 'new_element')
>>> a
[1, 5.2, 'new_element', 'abcd', 'def']
>>> a.pop(-3)
'new_element'
>>> a
[1, 5.2, 'abcd', 'def']
>>> a.remove('abcd')
>>> a
[1, 5.2, 'def']
>>> a.pop()  # метод pop() без аргументов удаляет и возвращает последний элемент списка
'def'
>>> a
[1, 5.2]
{% endprogram %}

В Питоне многие методы работают над семейством схожих объектов. Например, строки и списки в Питоне &mdash;
это последовательности. У последовательностей можно узнавать длину методом len(), последовательности
можно складывать знаком + (конкатенация) и умножать на число (конкатенация, повторенная k раз). Также
можно выбирать куски последовательности с помощью механизма срезов.

{% program "python" %}
>>> [1, 2, 3] + [4, 5, 6]
[1, 2, 3, 4, 5, 6]
>>> [1, 2, 3] * 4
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> a = [0] * 10  # создание пустого одномерного массива
>>> a
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>>> a = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
>>> a[1:4]   # срез с первого по четвертый элемент, исключая правую границу
[11, 12, 13]
>>> a[2:]    # срез со второго элемента до конца
[12, 13, 14, 15, 16, 17, 18, 19]
>>> a[:5]    # срез от начала до пятого элемента исключительно
[10, 11, 12, 13, 14]
>>> a[:-3]   # индексы в срезах могут быть отрицательными
[10, 11, 12, 13, 14, 15, 16]
>>> a[2:8:2] # третий необязательный параметр: шаг среза
[12, 14, 16]
>>> a[::2]
[10, 12, 14, 16, 18]
>>> a[::-1]  # простой способ развернуть список
[19, 18, 17, 16, 15, 14, 13, 12, 11, 10]
>>> s = 'abcde'
>>> s[::-1]  # всё это работает и над строками
'edcba'
{% endprogram %}

Как уже говорилось, строки являются неизменяемым типом данных. Если нам нужно часто работать с символами строки,
то можно поступить так: сначала преобразовать строку в список, потом провести необходимые изменения, а потом 
обратно собрать строку из списка строк.

{% program "python" %}
>>> s = 'abcde'
>>> a = list(s)
>>> a
['a', 'b', 'c', 'd', 'e']
>>> a[2] = 'k'
>>> a.append('f')
>>> a
['a', 'b', 'k', 'd', 'e', 'f']
>>> ''.join(a)
'abkdef'
>>> ', '.join(a)
'a, b, k, d, e, f'
{% endprogram %}

Для создания списков на основе других последовательностей существует механизм генераторов (list comprehensions).
Синтаксис наиболее частого варианта использования: 
<br><code>[выражение <b>for</b> переменная <b>in</b> последовательность <b>if</b> условие]</code>
<br>Для получения последовательности подряд идущих чисел можно использовать функцию range(). 
range(last) порождает возрастающую последовательность от 0 до last - 1. 
Функция range(first, last[, step]) порождает последовательность от first до last - 1 с шагом step.

{% program "python" %}
[]

{% endprogram %}

Двумерные массивы

collections.deque

{% endsubsection %}

{% subsection "Множества: set" %}
{% endsubsection %}

{% subsection "Словари: dict" %}
{% endsubsection %}

{% endsection %}