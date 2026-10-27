# Cotizador Megamoto

Cotizador de motos para Megamoto Tigre: contado, tarjeta, prendario Banco Patagonia y anticipo + tarjeta, con el mensaje listo para WhatsApp.

## Como actualizar precios
- `datos/precios.tsv`: una moto por renglon (marca, modelo, lista, lista+patente, contado sin patente, patentamiento, contado patentada GBA), copiado de la hoja "Precios Mur".
- `datos/promo.json`: promo de contado de fin de mes y su fecha de vencimiento.
- El plan prendario esta dentro de `datos/build.py`.
- Despues de cambiar algo: `python3 datos/build.py` regenera `index.html`.

Lo mas facil: pedirselo a Claude ("actualiza el cotizador con la planilla nueva").
