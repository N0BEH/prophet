# prophet

Le code actuel utilise une méthode de prévision basée sur la bibliothèque Prophet, qui est une procédure de prévision pour les données de séries temporelles basée sur un modèle additif où les tendances non linéaires sont ajustées avec la saisonnalité annuelle, hebdomadaire et quotidienne, plus les effets des jours fériés. C'est une méthode de prévision très efficace et populaire pour les séries temporelles.

Dans le contexte actuelle, cela signifie que si l'afflux de candidats a des tendances ou des motifs périodiques (par exemple, un certain jour de la semaine ou une certaine heure de la journée), alors la méthode actuelle serait en mesure de capter ces tendances et de faire une prévision en conséquence.

[Documentation de Prophet](https://facebook.github.io/prophet/)

![alt text](https://github.com/N0BEH/prophet/blob/main/prophet.gif?raw=true)

### Installation

```bash
pip install prophet
pip install matplotlib
pip install pyyaml
pip install pandas
```

### Prédictions : 

![alt text](https://github.com/N0BEH/prophet/blob/main/pred1.png?raw=true)
![alt text](https://github.com/N0BEH/prophet/blob/main/pred2.png?raw=true)