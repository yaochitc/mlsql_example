from __future__ import absolute_import
from pyspark.ml.linalg import VectorUDT, Vectors
import pickle
import os
import python_fun



def predict(index, s):
    items = [i for i in s]
    modelPath = pickle.loads(items[1])[0] + "/model.pkl"

    if not hasattr(os, "mlsql_models"):
        setattr(os, "mlsql_models", {})
    if modelPath not in os.mlsql_models:
        print("Load sklearn model %s" % modelPath)
        os.mlsql_models[modelPath] = pickle.load(open(modelPath, "rb"))

    model = os.mlsql_models[modelPath]
    rawVector = pickle.loads(items[0])
    feature = VectorUDT().deserialize(rawVector)
    y = model.predict([feature.toArray()])
    return [VectorUDT().serialize(Vectors.dense(y))]

python_fun.udf(predict)