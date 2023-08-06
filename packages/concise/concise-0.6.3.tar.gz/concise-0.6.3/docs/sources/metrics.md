`concise.metrics` provides a masked version of `keras.metrics` for classification (mask value = -1) and introduces additional metrics. ***Note:*** Be careful when using the additional metrics (`f1`, `precision`, ...). For those, the average accross minibatches is namely not equal to the metric evaluated on the whole dataset.

## Available metrics

### contingency_table


```python
contingency_table(y, z)
```


Note:  if y and z are not rounded to 0 or 1, they are ignored

----

### sensitivity


```python
sensitivity(y, z)
```

----

### specificity


```python
specificity(y, z)
```

----

### fpr


```python
fpr(y, z)
```

----

### fnr


```python
fnr(y, z)
```

----

### precision


```python
precision(y, z)
```

----

### fdr


```python
fdr(y, z)
```

----

### accuracy


```python
accuracy(y, z)
```

----

### f1


```python
f1(y, z)
```

----

### mcc


```python
mcc(y, z)
```

----

### cat_acc


```python
cat_acc(y, z)
```

----

### var_explained


```python
var_explained(y_true, y_pred)
```


Fraction of variance explained.

