from sklearn.tree import DecisionTreeClassifier
import joblib

X = [[40],[55],[70],[85]]
y = ["ITI","Diploma","Engineering","Medical"]

model = DecisionTreeClassifier()
model.fit(X,y)

joblib.dump(model,"career_model.pkl")
print("Model trained")