# Caption generator application built with microservices

To repozytorium dotyczy projektu aplikacji generującej opisy do zdjęć. Aplikacja umożliwia generowanie opisów za pomocą przetrenowanych modeli z biblioteki transformers.

https://github.com/piotrulo022/Caption-generator/assets/76213314/6f64147d-5da3-4782-87df-1db7e02c5b12


Projekt został opracowany w Python i składa się z trzech mikroserwisów - aplikacji UI napisanej w środowisku streamlit, mikroserwisu backend dostarczającego narzędzia do predykcji oraz bazy danych przechowującej zapisane przez uzytkownika predykcje. Aplikacja jest skonteneryzowana dockerem.

Każdy z mikroserwisów został osobno opisany w folderach.
<div style="text-align:center">

  ![captioning-architecture](https://github.com/piotrulo022/Caption-generator/assets/76213314/e1b8f9e8-59a7-4708-b545-f4b5b575cd68)

</div>
