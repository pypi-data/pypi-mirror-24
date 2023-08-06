Global evaluation metrics. Similar to `concise.metrics` or `keras.metrics` but implemented with numpy and intended to be used on the *whole dataset* after training the model. Many evaluation metrics (AUC, F1, ...) namely can't be expressed as an average over minibatches and are hence not implemented in `keras.metrics` (see [this](https://github.com/fchollet/keras/issues/5794) discussion).

***Note:*** All the metrics mask values -1 for classification and `np.nan` for regression.

## Available evaluation metrics

### auc


```python
auc(y, z, round=True)
```

----

### auprc


```python
auprc(y, z)
```

----

### accuracy


```python
accuracy(y, z, round=True)
```

----

### tpr


```python
tpr(y, z, round=True)
```

----

### tnr


```python
tnr(y, z, round=True)
```

----

### mcc


```python
mcc(y, z, round=True)
```

----

### f1


```python
f1(y, z, round=True)
```

----

### cat_acc


```python
cat_acc(y, z)
```


Categorical accuracy

----

### cor


```python
cor(y, z)
```


Compute Pearson correlation coefficient.

----

### kendall


```python
kendall(y, z, nb_sample=100000)
```

----

### mad


```python
mad(y, z)
```

----

### rmse


```python
rmse(y, z)
```

----

### rrmse


```python
rrmse(y, z)
```

----

### mse


```python
mse(y_true, y_pred)
```

----

### ermse


```python
ermse(y_true, y_pred)
```


Exponentiated root-mean-squared error

----

### var_explained


```python
var_explained(y_true, y_pred)
```


Fraction of variance explained.

