# OSTW-action-parser
Генерирует библиотеку из методов для последующего использования в ostw-скриптах

Сгенерированные методы предназначаются для использования в скриптах взамен встроенных действий. 
Они имеют упрощенную сигнатуру благодаря отсутствию параметра Reevaluation. Вместо него, 
указание параметров для постоянного обновления осуществляется с помощью того, передан ли этот параметер как статичный тип, либо 
же как лямбда-функция, возвращающая этот тип. 

Это позволяет не только немного упроститиь вызов действий, но и делает код более логичным и последовательным, исключая 
все ситуации, в которой выражение, которое по идее должно вычисляться один раз при передаче как аргумент, 
вычисляется повторно внутри действия, ломая логику языка. Теперь всегда, когда необходимо вычислять выражение много раз, 
его нужно передать, обернутым в лямбда-фукцнию, которую уже логично вычислять множество раз.

На каждое встроенное действие, поддерживающее Reevaluation, в сгенерированной библиотеке содержится множество перегрузок,
отличающихся сигнатурой аргументов и покрывающих все возможные комбинации параметров для обновления, а ткаже добавляющих
новые полезные перегрузки и аргументы, позволяющие, к примеру, передавать в качестве аргумента вместо лямбда-функции без параметров
лямда-функцию, принимающую игрока, и возвращающую значения, зависящее от этого игрока (в обычном ostw такое приходится достигать засчет 
использования LocalPlayer - функции, также ломающей логику кода тем, что ее значение не вычисляется при вызове, а толкьо внутри действия)
