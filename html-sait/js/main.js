function onEntryText(entry) {
    entry.forEach(change => {
      if (change.isIntersecting) {
        if (k==0){
        var typed = new Typed(".mov",{
            strings: [, "We welcome you, dear visitors of our site. On this page you will learn how to install our application. So, to download the application, we need to go to the HOME tab, Then click on the INSTALL button and the application will start downloading. Next, we go to the browser's download history and install an application called: GreenHouse."] ,
            startDelay: (500),
            backDelay: (99999999),
            typeSpeed: 25,
            loop: true,
            })
        k = 1;
      }}
    });
  }
  
  let optionstext = {
    threshold: [0.5] };
  let observertext = new IntersectionObserver(onEntryText, optionstext);
  let elementstext = document.querySelectorAll('.for__what2');
  let k = 0;
  for (let elmtext of elementstext) {
    observertext.observe(elmtext);
  }


  function onEntry(entry) {
    entry.forEach(change => {
      if (change.isIntersecting) {
       change.target.classList.add('element-show');
      }
    });
  }
  
  let options = {
    threshold: [0.5] };
  let observer = new IntersectionObserver(onEntry, options);
  let elements = document.querySelectorAll('.installing_show');
  
  for (let elm of elements) {
    observer.observe(elm);
  }