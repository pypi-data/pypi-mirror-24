
## Initializing filters on known motifs

In the scenario where data is scarse, it is often useful to initialize the filters of the first convolutional layer to some known position weights matrices (PWM's). That way, the model already starts with a parameter configuration much closer to the 'right' one.

Concise provides access to 2 PWM databases:

- transcription factors from ENCODE (2067 PWMs)
- rna-binding proteins from ATtrACT (1583 PWMs).

### Find the motif of interest

Each PWM database is provided as a module under `concise.data`. It provides two functions:

- `concise.data.<db>.get_metadata()` - returns a pandas.DataFrame with metadata information about each PWM 
- `concise.data.<db>.get_pwm_list()` - given a list of PWM ids, return a list with `concise.utils.pwm.PWM` instances

#### Metadata tables


```python
%matplotlib inline
import matplotlib.pyplot as plt
```


```python
# RBP PWM's
from concise.data import attract

dfa = attract.get_metadata()
dfa
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PWM_id</th>
      <th>Gene_name</th>
      <th>Gene_id</th>
      <th>Mutated</th>
      <th>Organism</th>
      <th>Motif</th>
      <th>Len</th>
      <th>Experiment_description</th>
      <th>Database</th>
      <th>Pubmed</th>
      <th>Experiment_description.1</th>
      <th>Family</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>519</td>
      <td>3IVK</td>
      <td>3IVK</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>GAAACA</td>
      <td>6</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>19965478</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>1</th>
      <td>574</td>
      <td>3IVK</td>
      <td>3IVK</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>UGGG</td>
      <td>4</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>19965478</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2</th>
      <td>464</td>
      <td>4KZD</td>
      <td>4KZD</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>GAAAC</td>
      <td>5</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>24952597</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4879</th>
      <td>1396</td>
      <td>HNRNPAB</td>
      <td>ENSG00000197451</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>AUAGCA</td>
      <td>6</td>
      <td>In vitro splicing assays</td>
      <td>AEDB</td>
      <td>12426391</td>
      <td>other</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>4880</th>
      <td>1397</td>
      <td>HNRNPA1</td>
      <td>ENSG00000135486</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UAGG</td>
      <td>4</td>
      <td>Immunoprecipitation;U...</td>
      <td>AEDB</td>
      <td>15506926</td>
      <td>UV cross-linking</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>4881</th>
      <td>1398</td>
      <td>PTBP1</td>
      <td>ENSG00000011304</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UUCUUC</td>
      <td>6</td>
      <td>In vivo splicing assa...</td>
      <td>AEDB</td>
      <td>14966131</td>
      <td>UV cross-linking</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
  </tbody>
</table>
<p>4882 rows × 13 columns</p>
</div>




```python
# TF PWM's
from concise.data import encode

dfe = encode.get_metadata()
dfe
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>motif_name</th>
      <th>consensus</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AFP_1</td>
      <td>ATTAACTACAC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AHR::ARNT::HIF1A_1</td>
      <td>TGCGTGCGG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AHR::ARNT_1</td>
      <td>TAAGGGTTGCGTGCCC</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2064</th>
      <td>ZSCAN4_3</td>
      <td>TGCACACACTGAAAA</td>
    </tr>
    <tr>
      <th>2065</th>
      <td>fake_AACGSSAA</td>
      <td>AACGCCAA</td>
    </tr>
    <tr>
      <th>2066</th>
      <td>fake_AAGCSSAA</td>
      <td>AAGCCCAA</td>
    </tr>
  </tbody>
</table>
<p>2067 rows × 2 columns</p>
</div>



Let's choose PUM2 PWM (RBP in Human):


```python
dfa_pum2 = dfa[dfa.Gene_name.str.match("PUM2") & \
               dfa.Organism.str.match("Homo_sapiens")]
dfa_pum2
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PWM_id</th>
      <th>Gene_name</th>
      <th>Gene_id</th>
      <th>Mutated</th>
      <th>Organism</th>
      <th>Motif</th>
      <th>Len</th>
      <th>Experiment_description</th>
      <th>Database</th>
      <th>Pubmed</th>
      <th>Experiment_description.1</th>
      <th>Family</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2603</th>
      <td>503</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAAAUA</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2604</th>
      <td>361</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUACAUC</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2605</th>
      <td>514</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAGAUA</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2613</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAUAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
    <tr>
      <th>2614</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUACAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
    <tr>
      <th>2615</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAGAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
  </tbody>
</table>
<p>13 rows × 13 columns</p>
</div>



#### Visualization - PWM class

The `PWM` class provides a method `plotPWM` to visualize the PWM.


```python
# Visualize the PUM2 Motifs from different experiments
from concise.utils.pwm import PWM
dfa_pum2_uniq = dfa_pum2[["Experiment_description", "PWM_id"]].drop_duplicates()
pwm_list = attract.get_pwm_list(dfa_pum2_uniq.PWM_id)
```


```python
for i, pwm in enumerate(pwm_list):
    print("PWM_id:", pwm.name, "; Experiment_description:", dfa_pum2_uniq.Experiment_description.iloc[i])
    pwm.plotPWM(figsize=(3,1))
```

    PWM_id: 503 ; Experiment_description: X-RAY DIFFRACTION



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_1.png)


    PWM_id: 361 ; Experiment_description: X-RAY DIFFRACTION



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_3.png)


    PWM_id: 514 ; Experiment_description: X-RAY DIFFRACTION



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_5.png)


    PWM_id: 116 ; Experiment_description: RIP-chip



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_7.png)


    PWM_id: 129 ; Experiment_description: genome-wide in vivo immunoprecipitation



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_9.png)


    PWM_id: 107 ; Experiment_description: PAR-clip



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_11_11.png)


We can select the PWM with id 129.


```python
pwm_list = [pwm for pwm in pwm_list if pwm.name == "129"]
```


```python
pwm_list
```




    [PWM(name: 129, consensus: TGTAAATA)]



### Initialize the conv filters with PWM values


```python
import concise.layers as cl
import keras.layers as kl
import concise.initializers as ci
import concise.regularizers as cr
from keras.callbacks import EarlyStopping
from concise.preprocessing import encodeDNA
from keras.models import Model, load_model
from keras.optimizers import Adam
```


```python
# get the data
def load(split="train", st=None):
    dt = pd.read_csv("../data/RBP/PUM2_{0}.csv".format(split))
    # DNA/RNA sequence
    xseq = encodeDNA(dt.seq) # list of sequences -> np.ndarray
    # response variable
    y = dt.binding_site.as_matrix().reshape((-1, 1)).astype("float")
    return {"seq": xseq}, y

train, valid, test = load("train"), load("valid"), load("test")

# deduce sequence length
seq_length = train[0]["seq"].shape[1]
```


```python
# define the model
def model(train, filters=1, kernel_size=9, pwm_list=None, lr=0.001):
    seq_length = train[0]["seq"].shape[1]
    if pwm_list is None:
        kinit = "glorot_uniform"
        binit = "zeros"
    else:
        kinit = ci.PSSMKernelInitializer(pwm_list, add_noise_before_Pwm2Pssm=True)
        binit = "zeros"
        
    # sequence
    in_dna = cl.InputDNA(seq_length=seq_length, name="seq")
    x = cl.ConvDNA(filters=filters, 
                   kernel_size=kernel_size, 
                   activation="relu",
                   kernel_initializer=kinit,
                   bias_initializer=binit,
                   name="conv1")(in_dna)
    x = kl.AveragePooling1D(pool_size=4)(x)
    x = kl.Flatten()(x)
    
    x = kl.Dense(units=1)(x)
    m = Model(in_dna, x)
    m.compile(Adam(lr=lr), loss="binary_crossentropy", metrics=["acc"])
    return m
```

**TODO** - check if this is true

`ci.PSSMKernelInitializer` will set the filters of the first convolutional layer to the values of the position-specific scoring matrix (PSSM):

$$ pssm_{ij} = log \frac{pwm_{ij}}{b_j} \;,$$

where $b_j$ is the background probability of observing base $j$.

We add gaussian noise to each individual filter. Let's visualize the filters:


```python
# create two models: with and without PWM initialization
m_rand_init = model(train, filters=3, pwm_list=None) # random initialization
m_pwm_init = model(train, filters=3, pwm_list=pwm_list) # motif initialization
```


```python
print("Random initialization:")
m_rand_init.get_layer("conv1").plot_weights(figsize=(3, 1.2))
```

    Random initialization:
    filter index: 0



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_22_1.png)


    filter index: 1



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_22_3.png)


    filter index: 2



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_22_5.png)



```python
print("Known PWM initialization:")
m_pwm_init.get_layer("conv1").plot_weights(figsize=(3, 1.2))
```

    Known PWM initialization:
    filter index: 0



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_23_1.png)


    filter index: 1



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_23_3.png)


    filter index: 2



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_23_5.png)



```python
# train the models
m_rand_init.fit(train[0], train[1], epochs=50, validation_data=valid, 
                verbose=2,
                callbacks=[EarlyStopping(patience=5)])
```

    Train on 17713 samples, validate on 4881 samples
    Epoch 1/50
    1s - loss: 0.5931 - acc: 0.7957 - val_loss: 0.5082 - val_acc: 0.7992
    Epoch 2/50
    0s - loss: 0.5023 - acc: 0.7958 - val_loss: 0.4885 - val_acc: 0.7990
    Epoch 3/50
    0s - loss: 0.4868 - acc: 0.7957 - val_loss: 0.4794 - val_acc: 0.7996
    Epoch 4/50
    0s - loss: 0.4795 - acc: 0.7960 - val_loss: 0.4728 - val_acc: 0.8009
    Epoch 5/50
    0s - loss: 0.4770 - acc: 0.7962 - val_loss: 0.4739 - val_acc: 0.8009
    Epoch 6/50
    0s - loss: 0.4712 - acc: 0.7969 - val_loss: 0.4646 - val_acc: 0.8027
    Epoch 7/50
    0s - loss: 0.4633 - acc: 0.7976 - val_loss: 0.4533 - val_acc: 0.8023
    Epoch 8/50
    0s - loss: 0.4495 - acc: 0.8011 - val_loss: 0.4353 - val_acc: 0.8062
    Epoch 9/50
    0s - loss: 0.4372 - acc: 0.8051 - val_loss: 0.4322 - val_acc: 0.8031
    Epoch 10/50
    0s - loss: 0.4335 - acc: 0.8090 - val_loss: 0.4270 - val_acc: 0.8033
    Epoch 11/50
    0s - loss: 0.4313 - acc: 0.8107 - val_loss: 0.4381 - val_acc: 0.8144
    Epoch 12/50
    0s - loss: 0.4245 - acc: 0.8113 - val_loss: 0.4390 - val_acc: 0.8193
    Epoch 13/50
    0s - loss: 0.4229 - acc: 0.8142 - val_loss: 0.4412 - val_acc: 0.8211
    Epoch 14/50
    0s - loss: 0.4212 - acc: 0.8197 - val_loss: 0.4392 - val_acc: 0.8170
    Epoch 15/50
    1s - loss: 0.4213 - acc: 0.8186 - val_loss: 0.4231 - val_acc: 0.8136
    Epoch 16/50
    0s - loss: 0.4143 - acc: 0.8128 - val_loss: 0.4152 - val_acc: 0.8144
    Epoch 17/50
    0s - loss: 0.4042 - acc: 0.8187 - val_loss: 0.4173 - val_acc: 0.8230
    Epoch 18/50
    0s - loss: 0.4012 - acc: 0.8206 - val_loss: 0.4192 - val_acc: 0.8267
    Epoch 19/50
    0s - loss: 0.3969 - acc: 0.8253 - val_loss: 0.4221 - val_acc: 0.8265
    Epoch 20/50
    0s - loss: 0.3967 - acc: 0.8252 - val_loss: 0.4586 - val_acc: 0.8099
    Epoch 21/50
    0s - loss: 0.3958 - acc: 0.8270 - val_loss: 0.4133 - val_acc: 0.8279
    Epoch 22/50
    1s - loss: 0.3943 - acc: 0.8297 - val_loss: 0.4174 - val_acc: 0.8343
    Epoch 23/50
    0s - loss: 0.3929 - acc: 0.8332 - val_loss: 0.4083 - val_acc: 0.8345
    Epoch 24/50
    1s - loss: 0.3922 - acc: 0.8362 - val_loss: 0.4548 - val_acc: 0.8332
    Epoch 25/50
    1s - loss: 0.4078 - acc: 0.8284 - val_loss: 0.3994 - val_acc: 0.8351
    Epoch 26/50
    1s - loss: 0.3853 - acc: 0.8356 - val_loss: 0.4018 - val_acc: 0.8345
    Epoch 27/50
    1s - loss: 0.3874 - acc: 0.8376 - val_loss: 0.3942 - val_acc: 0.8273
    Epoch 28/50
    1s - loss: 0.3897 - acc: 0.8374 - val_loss: 0.3974 - val_acc: 0.8381
    Epoch 29/50
    0s - loss: 0.3908 - acc: 0.8398 - val_loss: 0.4013 - val_acc: 0.8414
    Epoch 30/50
    0s - loss: 0.3853 - acc: 0.8425 - val_loss: 0.3985 - val_acc: 0.8365
    Epoch 31/50
    0s - loss: 0.3830 - acc: 0.8431 - val_loss: 0.4076 - val_acc: 0.8451
    Epoch 32/50
    0s - loss: 0.3821 - acc: 0.8464 - val_loss: 0.4185 - val_acc: 0.8427
    Epoch 33/50
    0s - loss: 0.3815 - acc: 0.8468 - val_loss: 0.4057 - val_acc: 0.8441





    <keras.callbacks.History at 0x7f931353ca90>




```python
m_pwm_init.fit(train[0], train[1], epochs=50, validation_data=valid, 
                verbose=2,
                callbacks=[EarlyStopping(patience=5)])
```

    Train on 17713 samples, validate on 4881 samples
    Epoch 1/50
    1s - loss: 0.7954 - acc: 0.7628 - val_loss: 0.6350 - val_acc: 0.8007
    Epoch 2/50
    1s - loss: 0.5508 - acc: 0.8014 - val_loss: 0.5144 - val_acc: 0.8052
    Epoch 3/50
    1s - loss: 0.4755 - acc: 0.8117 - val_loss: 0.4871 - val_acc: 0.8070
    Epoch 4/50
    1s - loss: 0.4426 - acc: 0.8165 - val_loss: 0.4316 - val_acc: 0.8181
    Epoch 5/50
    0s - loss: 0.4269 - acc: 0.8230 - val_loss: 0.4251 - val_acc: 0.8242
    Epoch 6/50
    0s - loss: 0.4154 - acc: 0.8299 - val_loss: 0.4145 - val_acc: 0.8269
    Epoch 7/50
    1s - loss: 0.4081 - acc: 0.8354 - val_loss: 0.4077 - val_acc: 0.8312
    Epoch 8/50
    1s - loss: 0.4012 - acc: 0.8396 - val_loss: 0.4032 - val_acc: 0.8361
    Epoch 9/50
    1s - loss: 0.3920 - acc: 0.8436 - val_loss: 0.3972 - val_acc: 0.8379
    Epoch 10/50
    0s - loss: 0.3872 - acc: 0.8465 - val_loss: 0.4085 - val_acc: 0.8408
    Epoch 11/50
    1s - loss: 0.3837 - acc: 0.8480 - val_loss: 0.4049 - val_acc: 0.8406
    Epoch 12/50
    1s - loss: 0.3769 - acc: 0.8508 - val_loss: 0.3960 - val_acc: 0.8478
    Epoch 13/50
    1s - loss: 0.3782 - acc: 0.8534 - val_loss: 0.3968 - val_acc: 0.8496
    Epoch 14/50
    1s - loss: 0.3726 - acc: 0.8567 - val_loss: 0.3929 - val_acc: 0.8531
    Epoch 15/50
    0s - loss: 0.3694 - acc: 0.8573 - val_loss: 0.3876 - val_acc: 0.8521
    Epoch 16/50
    1s - loss: 0.3655 - acc: 0.8575 - val_loss: 0.3900 - val_acc: 0.8543
    Epoch 17/50
    1s - loss: 0.3616 - acc: 0.8585 - val_loss: 0.3946 - val_acc: 0.8552
    Epoch 18/50
    1s - loss: 0.3602 - acc: 0.8602 - val_loss: 0.3943 - val_acc: 0.8578
    Epoch 19/50
    1s - loss: 0.3573 - acc: 0.8617 - val_loss: 0.3855 - val_acc: 0.8640
    Epoch 20/50
    1s - loss: 0.3582 - acc: 0.8626 - val_loss: 0.3925 - val_acc: 0.8595
    Epoch 21/50
    1s - loss: 0.3556 - acc: 0.8653 - val_loss: 0.3857 - val_acc: 0.8627
    Epoch 22/50
    0s - loss: 0.3515 - acc: 0.8669 - val_loss: 0.3849 - val_acc: 0.8631
    Epoch 23/50
    0s - loss: 0.3611 - acc: 0.8667 - val_loss: 0.3852 - val_acc: 0.8638
    Epoch 24/50
    0s - loss: 0.3541 - acc: 0.8663 - val_loss: 0.3822 - val_acc: 0.8636
    Epoch 25/50
    0s - loss: 0.3500 - acc: 0.8678 - val_loss: 0.3952 - val_acc: 0.8640
    Epoch 26/50
    0s - loss: 0.3442 - acc: 0.8690 - val_loss: 0.3917 - val_acc: 0.8644
    Epoch 27/50
    1s - loss: 0.3409 - acc: 0.8703 - val_loss: 0.3974 - val_acc: 0.8654
    Epoch 28/50
    0s - loss: 0.3397 - acc: 0.8704 - val_loss: 0.3954 - val_acc: 0.8652
    Epoch 29/50
    0s - loss: 0.3382 - acc: 0.8718 - val_loss: 0.3983 - val_acc: 0.8646
    Epoch 30/50
    0s - loss: 0.3376 - acc: 0.8711 - val_loss: 0.3884 - val_acc: 0.8650





    <keras.callbacks.History at 0x7f93132961d0>



### Test-set performance


```python
import concise.eval_metrics as cem
```


```python
# performance on the test-set
# Random initialization
print("Random intiailzation auPR:", cem.auprc(test[1], m_rand_init.predict(test[0])))
# PWM initialization
print("Known PWM initialization auPR:", cem.auprc(test[1], m_pwm_init.predict(test[0])))
```

    Random intiailzation auPR: 0.635598660178
    Known PWM initialization auPR: 0.724295058122


### Filter visualization


```python
m_rand_init.get_layer("conv1").plot_weights(plot_type="motif_pwm_info", figsize=(3, 1.2))
```

    filter index: 0



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_30_1.png)


    filter index: 1



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_30_3.png)


    filter index: 2



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_30_5.png)



```python
m_pwm_init.get_layer("conv1").plot_weights(plot_type="motif_pwm_info", figsize=(3, 1.2))
```

    filter index: 0



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_31_1.png)


    filter index: 1



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_31_3.png)


    filter index: 2



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_31_5.png)


## Benefits of motif initialization

- Interpretatbility
  - we can use fewer filters and know that the major effect will be captured by the first filters
    - handy when studying the model parameters
- Better predictive performance
- More stable training
