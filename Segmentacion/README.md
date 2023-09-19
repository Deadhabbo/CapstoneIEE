# Segmentacion

Los codigos son metodos de segmentacion. 
- Al no tener claro cuales pueden funcionar de mejor manera, hay 3 tipos de segmentacion:
1. Por color en el archivo "deteccion_rojo6.py"
2. Por threshold global que es simplemente definir un umbral y detectar para arriba o abajo (incluye filtros para una mejor segmentacion)
3. Por segmentacion OTSU que es una segmentacion automatica 

Actualmente la mejor manera que encontre para hacerlo es el usado en deteccion_rojo6.py ya que ahi incluso calibro la camara antes de empezar a detectar, cosa que dependiendo dee la luz igual se ajuste al ambiente. Es el mas completo, pero podriamos mezclar tecnicas en un futuro