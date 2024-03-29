# -*- coding: utf-8 -*-
"""
Created on 05/07/2023 16:43
@author: GiovanniMINGHELLI, Lu6D
"""
import joblib
import numpy as np
import os
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sources.data_pipeline.data_pipeline import global_transformer, next_events, history
from sources.utils.utils import calculate_odds, get_last_model, get_root


class Model:
    def __init__(self):
        self.accuracy = None

    def modelling(self):
        # Étape 1 : Préparation des données d'entraînement et de validation
        train_set, val_set = global_transformer(history()), global_transformer(next_events())

        X, y = train_set.drop('winner_is', axis=1), train_set['winner_is']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Étape 2 : Recherche des meilleurs hyperparamètres
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 5, 10],
            'min_samples_split': [2, 5, 10]}

        grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=5)
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        # Étape 3 : Évaluation du meilleur modèle
        print(classification_report(y_test, best_model.predict(X_test)))
        accuracy = accuracy_score(y_test, best_model.predict(X_test))
        self.accuracy = accuracy

        # Étape 4 : Prédiction et calcul des cotes
        results = val_set.copy()
        output = results[['player1_rank', 'player2_rank', 'atp_difference']]
        probas = best_model.predict_proba(results)
        odds = np.vectorize(calculate_odds)(probas)

        output['classe'], output['proba'] = best_model.predict(results), probas.round(2).tolist()
        output['odds'] = odds.round(2).tolist()

        # Étape 5 : Suppresion de l'ancien modèle
        last_model = get_last_model()
        if last_model is not None:
            os.remove(last_model)


        # Étape 6 : Enregistrement des résultats et du modèle
        output.to_csv(os.path.join(get_root(), 'database.nosync', 'predicted_table.csv'),
                       mode='a', header=False, index=False)

        # Ajouter la colonne des sr:match_id
        model_path = os.path.join(get_root(), 'ml_models', f'model_rf_.joblib')
        joblib.dump(value=best_model, filename=model_path)
        # Save the model using protocol 3
        # with open(f'model_rf_.pkl', 'wb'):
        # pickle.dump(best_model, f'model_rf_.pkl', protocol=3)

    # Load the model
    #       with open('model_filename.pkl', 'rb') as file:
    #   loaded_model = pickle.load(file)
    def get_accuracy(self):
        return self.accuracy


if __name__ == '__main__':
    mon_model = Model()
    mon_model.modelling()
