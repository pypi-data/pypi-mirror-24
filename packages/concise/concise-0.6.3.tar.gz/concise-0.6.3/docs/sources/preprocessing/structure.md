### encodeRNAStructure


```python
encodeRNAStructure(seq_vec, maxlen=None, seq_align='start', W=240, L=160, U=1, tmpdir='/tmp/RNAplfold/')
```


Compute RNA secondary structure with RNAplfold implemented in
Kazan et al 2010, [doi](https://doi.org/10.1371/journal.pcbi.1000832).

__Note__

Secondary structure is represented as the probability
to be in the following states:
- `["Pairedness", "Hairpin loop", "Internal loop", "Multi loop", "External region"]`
See Kazan et al 2010, [doi](https://doi.org/10.1371/journal.pcbi.1000832)
for more information.


__Arguments__

 - __seq_vec__: list of DNA/RNA sequences
 maxlen, seq_align: see `pad_sequences`
 W, Int: span - window length
 L, Int, maxiumm span
 U, Int, size of unpaired region
 - __tmpdir__: Where to store the intermediary files of RNAplfold.

__Note__

Recommended parameters:

- for human, mouse use W, L, u : 240, 160, 1
- for fly, yeast   use W, L, u :  80,  40, 1

__Returns__

np.ndarray of shape `(len(seq_vec), maxlen, 5)`
