## Running Jupyter Notebook
```sh
$ jupyter notebook
```
### Elements
⬜️ ✅

## References
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<pre>
    * <b>C. Koch and S.Ullman, "Shifts in selective visual attention. Towards the underlying neural circuitry," in <i>Human Neurobiology</i>, 1985.</b>
      * Inspiration from psychology, neuroscience, biology
      * Two stage theory:
         * pre-attentive: parallel process
         * attentive: serial process
      * Feature maps = how conspicuous given location is with respect to a feature
      * Saliency = global measure of conspicuity, combined feature maps
      * Paper assumes existing saliency map has been calculated
      * WTA (winner takes it all) = maximum finding operator, used for finding most active location
         * How does the selection proceed?
         * How to shift focus?
      <img src="https://latex.codecogs.com/gif.latex?y_i&space;=&space;\left\{\begin{matrix}&space;0,&space;&&space;x_i&space;<&space;\underset{j}{\max}&space;\&space;x_j&space;\\&space;f(x_i),&space;&&space;x_i&space;=&space;\underset{j}{\max}&space;\&space;x_j&space;\end{matrix}\right." title="y_i = \left\{\begin{matrix} 0, & x_i < \underset{j}{\max} \ x_j \\ f(x_i), & x_i = \underset{j}{\max} \ x_j \end{matrix}\right." />
      * Non hierarchical shift (WTA)
         <img src="https://latex.codecogs.com/gif.latex?\frac{\mathrm{d}&space;y_i}{\mathrm{d}&space;t}&space;=&space;y_i(x_i&space;-&space;\sum_{j}x_jy_j)&space;\\" title="\frac{\mathrm{d} y_i}{\mathrm{d} t} = y_i(x_i - \sum_{j}x_jy_j) \\" /> = state equation
         <img src="https://latex.codecogs.com/gif.latex?\sum_{j}y_j(t)&space;=&space;1" title="\sum_{j}y_j(t) = 1" /> = discrete probability distribution over outputs
         <img src="https://latex.codecogs.com/gif.latex?\sum_{j}x_jy_j" title="\sum_{j}x_jy_j" /> = average activity of network
         <img src="https://latex.codecogs.com/gif.latex?y_i(t)&space;=&space;\frac{y_i(0)e^{x_it}}{\sum_{j}y_j(0)e^{x_jt}}" title="y_i(t) = \frac{y_i(0)e^{x_it}}{\sum_{j}y_j(0)e^{x_jt}}" /> = solution
      * Hierarchical shift (WTA)
         * given m processors (parallel), image is divided into m regions (regions are indexed)
         * max activation is calculated hierarhically over regions
         <img src="https://latex.codecogs.com/gif.latex?\log_2&space;m" title="\log_2 m" /> = # of steps needed to find most active unit. (binary tree)
      * When most active unit is found, it is decayed (faded) -> new unit will become most active and focus will be shifted
    <b></b>
    <b></b>
    * <b>L. Itti, C. Koch and E. Niebur, "A model of saliency-based visual attention for rapid scene analysis," in <i>IEEE Transactions on Pattern Analysis and Machine Intelligence</i>, 1998.</b>
    * <b>Laurent Itti, Christof Koch, "A saliency-based search mechanism for overt and covert shifts of visual attention," in <i>Vision Research</i>, Volume 40, 2000.</b>
    * <b>P. Burt and E. Adelson, "The Laplacian Pyramid as a Compact Image Code," in <i>IEEE Transactions on Communications</i>, April 1983.</b>
</pre>
</body>
</html>

good references explained in paper http://www.cnbc.cmu.edu/~tai/readings/tom/itti_attention.pdf

## Datasets
[DIPLECS - Autonomous Driving Datasets](https://cvssp.org/data/diplecs/)

## Git repo references
[https://github.com/kyle-dorman/steering-angle-predictor](https://github.com/kyle-dorman/steering-angle-predictor) <br>
[https://github.com/stes/saliency](https://github.com/stes/saliency)

## Cheatsheets
[Conda](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
