# Geogebra-Solver
Рисуем и решаем геометрию за вас.
<br>
<h3><b><a href='http://geogebra0drawer.pythonanywhere.com/'>Наша домашняя страница</a></b></h3>

<h2>Инструкция для пользователя:</h2>

Поле ввода условия расположено в верхней половине экрана, сюда вводится текстовое условие задачи в соответствии с
<a href='http://geogebra0drawer.pythonanywhere.com/instruction'>инструкцией по вводу</a>.

Далее нажав кнопку **Анализ**, сгенерируется описание задачи на нашем внутреннем языке ввода.

Чтобы перейти к решению нажмите **Решить**.

Перед вами появится поле с чертежом и колонка с вопросом задачи, ответом и фактами, из которых он следует.

У каждого факта есть кнопки **show** и **why**.
<br><br>
При нажатии кнопки **show** на чертеже будет подсвечен объект или отношение, описанные этим фактом.
<br><br>
При нажатии кнопки **why** в списке фактов будут подсвечены факты из которых следует данный факт, а также в блоке факта появится его текстовое описание.
<br><br>
_Примечание: если факт является условием задачи, то вместо кнопки **why** у факта будет деактивированная кнопка  **task**_
<br><br>

_**Дополнительная информация**_
<br>
В мобильной версии так же присутствует кнопка **Увеличить чертёж**, которая позволяет увеличить поле рисунку, если его стандартного размера недостаточно.
<br>
<h2>Инструкция для запуска:</h2>
Для того чтобы локально запустить весь проект достаточно запустить файл `flask_server.py` в директории `web`.