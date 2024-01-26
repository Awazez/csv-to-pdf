SELECT 
    biblio.title AS 'titre',
    biblio.author AS 'auteur',
    items.location AS 'localisation',
    items.barcode AS 'code barre',
    items.itemcallnumber AS 'cote',
    items.issues AS 'nombre de prets'
FROM 
    items
JOIN 
    biblio ON items.biblionumber = biblio.biblionumber
JOIN 
    biblioitems ON items.biblioitemnumber = biblioitems.biblioitemnumber

WHERE
    items.stocknumber = 1
    AND items.onloan IS NULL             -- Livre non emprunté
    AND items.itemlost = 0               -- Aucune perte
    AND items.damaged = 0                -- Aucun dommage
    AND items.withdrawn = 0              -- Non retiré
    AND NOT EXISTS (
        SELECT *
        FROM branchtransfers
        WHERE
            items.itemnumber = branchtransfers.itemnumber
            AND branchtransfers.datearrived IS NULL
    )                                   -- Pas de transfert en cours
    AND NOT EXISTS (
        SELECT *
        FROM reserves
        WHERE
            items.itemnumber = reserves.itemnumber
            AND reserves.found IN ('W', 'T')
    )                                   -- Pas réservé ou trouvé
ORDER BY 
    items.itemcallnumber ASC