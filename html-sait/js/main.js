function onEntryText(entry) { // создаем функцию наблюдения 
    entry.forEach(change => { 
      if (change.isIntersecting) { // если на экране появляется элемент for__what2 то исполняется скрипт
        if (k==0){
        var typed = new Typed(".mov",{ // создаем класс mov 
            strings: [, "We welcome you, dear visitors of our site. On this page you will learn how to install our application. So, to download the application, we need to go to the HOME tab, Then click on the INSTALL button and the application will start downloading. Next, we go to the browser's download history and install an application called: GreenHouse."] ,
            startDelay: (500), // время перед началом печати текста
            backDelay: (99999999), // время после которого текст начнет стираться (в данном случае никогда)
            typeSpeed: 25, // скорость набора текста
            loop: true,
            })
        k = 1;
      }}
    });
  }
  let optionstext = {
    threshold: [0.5] }; // на сколько процентов на экране должен появиться элемент, что-бы сработал скрипт
  let observertext = new IntersectionObserver(onEntryText, optionstext); // создаем переменную наблюдателя
  let elementstext = document.querySelectorAll('.for__what2'); // создаем переменную за которой нужно наблюдать
  let k = 0; // переменная для исполнение команды 1 раз
  for (let elmtext of elementstext) { // Перебираем элементы
    observertext.observe(elmtext); // метод добавляет элемент в набор целевых элементов
  }


  function onEntry(entry) { // создаем функцию наблюдения 
    entry.forEach(change => {
      if (change.isIntersecting) { // если на экране появляется элемент installing_show то исполняется скрипт
       change.target.classList.add('element-show'); // добавляем класс к элементу (installing_show),(плавное появление надписи)
      }
    });
  }
  
  let options = {
    threshold: [0.5] }; // на сколько процентов на экране должен появиться элемент, что-бы сработал скрипт
  let observer = new IntersectionObserver(onEntry, options); // создаем переменную наблюдателя
  let elements = document.querySelectorAll('.installing_show'); // создаем переменную за которой нужно наблюдать
  for (let elm of elements) { // Перебираем элементы
    observer.observe(elm); // метод добавляет элемент в набор целевых элементов
  }