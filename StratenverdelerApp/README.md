Bloembollen verdeler:
Deze applicatie dient het proces van toewijzen van straten aan kinderen te automatiseren. Ieder kind krijgt een zo dicht mogelijke straat waarbij jongere kinderen het liefst de straten zo dichtbij mogelijk hebben.

Phase 1
    [V] Er kan afstand gemeten worden tussen 2 adressen
    [V] csv met kinderdata wordt omgezet naar kinder objecten
    [V] kinder data adressen worden omgezet naar coordinaten
    [V] lijst met straatnamen worden omgezet naar csv bestand
    [V] straten worden omgezet naar coordinaten
    [V] Kinderen worden in array gezet en gesorteerd op hun leeftijd
    [V] iedere straat van de kinderen worden de afstanden van gemeten met alle straten van hun desbetreffende dorp
    [V] De straten worden verdeeld en toegewezen per kind

Phase 2
    [] straten worden van OSM (nominatim) gehaald ipv de bestaande array van Gennep (dit is een handmatig proces) (https://towardsdatascience.com/retrieving-openstreetmap-data-in-python-1777a4be45bb)
    [] Sta een blacklist toe van straten
    [] Kleine straten met minder dan x adressen worden uit de lijst gefilterd of niet geprioriseerd
    [] De overgebleven straten die overblijven na het indelen van de kinderen worden weergegeven en eventueel toegewezen als 2de of 3de straat aan een kind

Phase 3
    [] Er worden automatisch pdf formulieren gemaakt voor de kinderen

Phase 4
    [V] Een webapplicatie van maken
    [] De applicatie staat verschillende soorten input toe (csv bestand, white/blacklisting van straten, fanatieke kinderen, output source van formulieren en eventuele andere dingen voor het formulier)
    [] Er kan een lijst van fanatieke kinderen gemaakt worden die meerdere straten krijgen toegewezen

Phase 5
    [] Webapplicatie geeft de map weer en de toewijzingen per kind dmv een visualisatie

Phase 6 - optimization
    [] Calculate a total cost of walking and make sure the calculations make the lowest cost total

Sources:
https://towardsdatascience.com/retrieving-openstreetmap-data-in-python-1777a4be45bb

Dependencies:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html