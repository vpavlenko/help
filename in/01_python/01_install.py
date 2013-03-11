{% section "Инструменты" %}

{% subsection "Интерпретатор Python" %}
Питон &mdash; интерпретируемый язык: вам не нужно компилировать программы, вы просто запускаете код на выполнение, 
скармливая его интерпретатору:
{% program "no-highlight" %}
$ cat > hello_world.py
print('Hello, world!')
$ python3 hello_world.py
Hello, world!
{% endprogram %}

Python постоянно развивается. В 2008 году вышла версия Python 3, с тех пор весь мир постепенно переходит на неё.
Языки Python 2 и Python 3 не имеют ни прямой, ни обратной совместимости, хотя очень похожи. Мы рекомендуем вам 
изучать третью версию.

В стандартную поставку unix-подобных ОС обычно входит интерпретатор Python <b>версии 2</b>. Если не предпринимать
специальных действий, то команда <code>python</code> в терминале вызывает именно интерпретатор версии 2.

<a href="http://python.org/download/">Скачайте и установите свежую версию Python 3.</a>

Интерпретатор можно использовать не только для выполения скриптов. Можно запустить его в интерактивном режиме,
и тогда он будет построчно выполнять команды, которые вы будете ему вводить.
{% program "no-highlight" %}
$ python3
Python 3.3.0 (default, Jan  7 2013, 03:13:42) 
[GCC 4.6.3] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 6 * 7
42
>>> a = 42
>>> b = a - 13
>>> b
29
{% endprogram %}

{% endsubsection %}

{% subsection "ipython3" %}
Интерактивный режим стандартного интерпретатора не слишком удобен: например, в нем не поддерживается автодополнение 
по клавише Tab. Существуют интерпретаторы-обёртки с расширенной функциональностью. 
Например, интерпретатор ipython3. В Ubuntu его можно установить командой
{% program "no-highlight" %}
$ sudo apt-get install ipython3
{% endprogram %}

<a href="http://ipython.org/ipython-doc/stable/install/install.html">Информация по установке на другие ОС.</a>
{% endsubsection %}

{% subsection "Sublime Text" %}
Для редактирования кода на Питоне достаточно простого текстового редактора с подсветкой. Мы рекомендуем вам
редактор <a href="http://www.sublimetext.com/">Sublime Text</a> как относительно свободный и довольно приятный на ощупь.
{% endsubsection %}

{% subsection "Среды разработки" %}
Для пошаговой отладки программ на Питоне желательно иметь какую-нибудь среду разработки. 
Мы советуем вам присмотреться к <a href="http://wingware.com/">Wing IDE</a> и к 
<a href="http://www.jetbrains.com/pycharm/">PyCharm</a>. 
Версия <a href="http://wingware.com/downloads/wingide-101/4.1.12-1/binaries">Wing IDE 101</a> распространяется бесплатно.
PyCharm и продвинутые версии Wing IDE имеют trial-период.

Фанатам консольных отладчиков сообщаем, что для Питона имеется отладчик pdb3. Впрочем,
он менее удобен, нежели gdb для языка Си.
{% endsubsection %}

{% subsection "Guake Terminal" %}
В качестве удобного терминала для GNOME мы рекомендуем Guake terminal. В Ubuntu его можно установить командой
{% program "no-highlight" %}
$ sudo apt-get install guake-terminal
{% endprogram %}

Терминал появляется и исчезает по нажатию F12.
{% endsubsection %}

{% endsection %}