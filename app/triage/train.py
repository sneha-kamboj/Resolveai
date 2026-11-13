import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "app/triage/triage_model.joblib"

def main():
    df = pd.read_csv("data/triage_data.csv")
    X = df["text"]
    y = df["intent"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_rate := None) if False else TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", MultinomialNB()),
    ])

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    print("TRAIN", len(X_train), "TEST", len(X_test))
    print("ACCURACY", round(acc, 3))
    print(classification_report(y_test, pred))

    joblib.dump(model, MODEL_PATH)
    print("SAVED", MODEL_PATH)

if __name__ == "__main__":
    main()
