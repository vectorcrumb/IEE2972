# Codigo Telescopio

A continuacion se detalla todo el codigo creado para el control del espejo primario del telescopio, junto a las funcionalidades por implementar y/o testear. Este texto no ha sido revisado para faltas ortograficas y no incluye tildes intencionalmente.

Para leer una version formateada de este documento (sin problemas de renderizado de MathJax), ver este [link](http://htmlpreview.github.io/?https://github.com/twbs/bootstrap/blob/gh-pages/2.3.2/index.html).

## Modelo de cinematica inversa

El modelo de cinematica inversa es generado mediante una red neuronal entrenada en MATLAB, la cual toma 1M de muestras de puntos aleatorios factibles en el espacio de estado del sistema y calcula el punto focal en el espacio correspondiente a cada punto.

Un vector de espacio de estado, $\vec{x}$, consiste de 3 elementos, cada uno detallando la altura de un actuador distinto (recordar que el espejo es controlado mediante 3 actuadores prismaticos). Estos 3 valores determinan la componente z de los 3 puntos con los cuales se calcula el plano equivalente del espejo primario.

El modelo de cinematica directa toma un punto del espacio de estados, genera 3 puntos en el espacio que indican la posicion del final de cada actuador, calcula un plano 3D y el punto focal correspondiente (un punto con elevacion igual a la distancia focal, desde el centro de los 3 puntos que componen el plano equivalente del espejo primario) y entrega dos valores, $\vec{dp}$ y $\theta$. El primero es el vector formado entre el punto focal del plano original (los 3 actuadores en su posicion de origen) y el punto focal del punto siendo evaluado. El segundo valor es la diferencia de angulo entre los vectores formado entre el centro de los planos y los puntos focales correspondientes. En el caso del vector formado por los 3 actuadores en sus posiciones de origen, este tiene solo valor en la componente z (es totalmente vertical).

El codigo correspondiente a esta seccion se encuentra en `nn_train/`.

## Entrenamiento de cinematica inversa

El modelo de cinematica inversa es entrenado por 1M de muestras, generadas a partir de 1M de puntos de espacio de estado factibles, provenientes de una distribucion uniforme. Los puntos son pasados por el modelo de cinematica directa, resultando en vectores $\vec{dp}=\vec{y}$. El modelo DK representa la transformacion $\vec{y} = DK(\vec{x})$. Nos interesa conocer la transformacion inversa, $IK = DK^{-1}$, tal que podamos tomar vectores $\vec{dp}$ y transformarlos a vectores de espacio de estado. Con las 1M de pares de puntos, se entrena una NN con 1 capa oculta de 20 neuronas. Adicionalmente, los pares de puntos se dividen 70%/10%/20% para entrenamiento, validacion y prueba.

MATLAB genera una NN, la cual almacena directamente con sus coeficientes en una funcion .m. Luego, se emplea el generador de codigo C para transformar este codigo a su equivalente en C.

El codigo correspondiente a esta seccion se encuentra en `nn_train/nn_func_cgen`.

## Ejecucion de modelo de cinematica inversa

La primera version del modelo IK corre mediante argumentos de comando de linea. El codigo C compilado espera 3 argumentos representando un vector $\vec{dp}$ y retorna un vector de espacio de estado, con cada componente separada por un caracter `'\n'`. Esta manera de llamar la NN claramente no es la optima, pues sufre un bottleneck con velocidades de escritura a STDIN y STDOUT, tanto por parte de C como de Python.

El codigo correspondiente a esta seccion se encuentra en `rpi/nn`. Esta carpeta contiene el codigo fuente y el programa compilado para correr en ARM (Raspberry Pi 3). Adicionalmente, en `rpi/nn/nn_c_backup` se encuentra el resto del codigo fuente, con el cual se puede compilar los archivos anteriores.

**IMPORTANTE:** El codigo fuente y compilado provienen de un modelo de IK antiguo, el cual no cuenta con las dimensiones del mecanismo real. Se debe reentrenar el modelo IK en MATLAB.

## Control de motores stepper

El control de motores stepper se realiza mediante los pines GPIO de la RPi3 (Raspberry Pi 3) y la libreria `RPi.GPIO`. Adicionalmente, se escribieron un par de clases auxiliares, `Stepper` y `StepperSystem`, ubicadas al interior de `StepperControls.py`. Estas clases representan un motor y un conjunto de motores, respectivamente. `Stepper` actua como un wrapper de alto nivel para las funciones GPIO necesarias para hacer andar el driver stepper, mientras que `StepperSystem` permite agrupar multiples objetos `Stepper` y moverlos simultaneamente sin necesidad de implementar threading para cada motor.

Actualmente el movimiento de los 3 motores consiste en mover los 3 en conjunto a la misma velocidad. A medida que cada motor alcanza la meta de pasos, se van deteniendo. El movimiento de los motores se realiza mediante una funcion blocking. Esta funcion itera a medida que sigan existiendo pasos por dar y se mueve un paso a la vez cada motor, antes de volver a evaluar si se debe seguir moviendo.

El codigo correspondiente a esta seccion se encuentra en `rpi/control`.

**IMPORTANTE:** La funcionalidad para mover los motores se encuentra implementado, sin embargo no se ha verificado que los calculos previos (DK, IK) esten correctos.

## Deteccion de punto laser

La deteccion del punto laser se realiza mediante la RPi Cam. El algoritmo de deteccion actual consiste en realizar un suavizado gaussiano con un kernel de 4x4 sobre la imagen del punto convertida a escala de grises. Luego, se encuentran las coordenadas del punto de mayor intensidad en la imagen y se forma una ROI de 100x100 pixeles alrededor de dicho punto. A esa ROI se calculan los momentos, para finalmente determinar el centroide del punto laser. Un punto de falla posible es al momento de tomar la ROI de la imagen, donde no se verifica que todos los indices se encuentren dentro de rango de la imagen. Una solucion sencilla al problema seria un try-catch block buscando un IndexValueError, y en caso de detectar uno, se acota correspondiente el tamaño de la ROI.

El codigo de esta seccion se encuentra en `rpi/vision`. Aqui existe `take_pics.py`, un script que toma 5 imagenes de la RPi Cam para poder probar el algoritmo con `detect_dot.py`. El script en `rt_dot.py` contiene el mismo algoritmo de `detect_dot.py` pero contenido en un loop infinito para procesar en tiempo real.

## Funcionalidad por implementar
- Actualizar dimensiones de modelo DK
- Reentrenar modelo IK nuevo
- Implementar codigo C de modelo de IK como un modulo en el codigo Python
- Agregar algoritmo de vision a codigo Python
- Encontrar alguna manera de generar valores de Z para puntos 2D entregados por algoritmo de vision. Sin estos puntos, puede confundirse la NN del modelo de IK.