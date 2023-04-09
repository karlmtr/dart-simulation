# Dart Simulation

## How to run it 

1. Install the dependencies : `pip install -r requirements.txt`
2. Comment/decomment the functions in `main.py`
3. Run the simulation : `python3 main.py`

## Aide-mémoire
### Conversions :

polaire -> cartésien

- $x = r\cos(\theta)$
- $y = r \sin(\theta)$

cartésien -> polaire

- $r = \sqrt{x^2 + y^2}$
- $\theta = \arctan(\frac{y}{x})$

### Cible
Chaque secteur représente un angle de 18 degrés.

- Bande des doubles et triples : 8 mm
- Diamètre du centre : 12.7 mm -> Rayon : 6.35 mm
- Diamètre du demi-centre : 31.8 mm -> Rayon : 15.9 mm
- Rayon du cercle extérieur de la couronne des doubles : 170 mm
- Rayon du cercle extérieur de la couronne des triples : 107.4 mm
- Diamètre total de la cible : 451 cm. -> Rayon :  2255 mm
- Epaisseur des fils : minimum 1.6 mm, max : 1.8 mm

Référence :  [https://fr.wikipedia.org/wiki/Fl%C3%A9chettes](https://fr.wikipedia.org/wiki/Fl%C3%A9chettes) (Wikipédia)
