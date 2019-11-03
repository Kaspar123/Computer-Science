## Model's scripts
```sh
$ python saliency.py                    - calculate pyramids, features, conspicuity_maps, saliency map
$ python inhibition_of_return.py        - find top most salient points using IOR
$ python excitation_supression.py       - visualize excitation, supression of salient/non-salient regions
```

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
      * implementation details of 1985's paper
         <img src="https://latex.codecogs.com/gif.latex?\begin{matrix}&space;I&space;=&space;&&space;\frac{r&plus;g&plus;b}{3}&space;&&space;R&space;=&space;&&space;r&space;-&space;\frac{g&space;&plus;&space;b}{2}&space;\\&space;G&space;=&space;&&space;g&space;-&space;\frac{r&space;&plus;&space;b}{2}&space;&&space;B&space;=&space;&&space;b&space;-&space;\frac{r&space;&plus;&space;g}{2}&space;\\&space;Y&space;=&space;&&space;\frac{r&space;&plus;&space;g}{2}&space;-&space;\frac{\left&space;|&space;r&space;-&space;g&space;\right&space;|}{2}&space;-&space;b&space;\end{matrix}" title="\begin{matrix} I = & \frac{r+g+b}{3} & R = & r - \frac{g + b}{2} \\ G = & g - \frac{r + b}{2} & B = & b - \frac{r + g}{2} \\ Y = & \frac{r + g}{2} - \frac{\left | r - g \right |}{2} - b \end{matrix}" />
      * gaussian pyramids (8 levels) are constructed for each feature (1 + 4 + 4 pyramids)
      * center-surround difference (6 + 12 + 24 = 42 feature maps in total)
         <img src="https://latex.codecogs.com/gif.latex?I(c,&space;s)&space;=&space;\left&space;|&space;I(c)&space;\ominus&space;I(s)&space;\right&space;|,&space;c&space;\in&space;\left&space;\{&space;2,3,4&space;\right&space;\},&space;\delta&space;\in&space;\left&space;\{&space;\right&space;3,4&space;\},&space;s&space;=&space;c&space;&plus;&space;\delta" title="I(c, s) = \left | I(c) \ominus I(s) \right |, c \in \left \{ 2,3,4 \right \}, \delta \in \left \{ \right 3,4 \}, s = c + \delta" />
         <img src="https://latex.codecogs.com/gif.latex?RG(c,&space;s)&space;=&space;\left&space;|&space;\left&space;(R(c)&space;-&space;G(s)&space;\right&space;)&space;\ominus&space;\left&space;(G(c)&space;-&space;R(s)&space;\right&space;)&space;\right&space;|" title="RG(c, s) = \left | \left (R(c) - G(s) \right ) \ominus \left (G(c) - R(s) \right ) \right |" />
         <img src="https://latex.codecogs.com/gif.latex?BY(c,&space;s)&space;=&space;\left&space;|&space;\left&space;(B(c)&space;-&space;Y(s)&space;\right&space;)&space;\ominus&space;\left&space;(Y(c)&space;-&space;B(s)&space;\right&space;)&space;\right&space;|" title="BY(c, s) = \left | \left (B(c) - Y(s) \right ) \ominus \left (Y(c) - B(s) \right ) \right |" />
         <img src="https://latex.codecogs.com/gif.latex?O(c,&space;s,&space;\theta)&space;=&space;\left&space;|&space;O(c,&space;\theta)&space;\ominus&space;O(s,\theta)&space;\right&space;|" title="O(c, s, \theta) = \left | O(c, \theta) \ominus O(s,\theta) \right |" />
      * normalization operator
         * feature map values are normalized to fixed range [0..M] to eliminate amplitude differences between feature maps
         * global maximum M and average value m is found
         <img src="https://latex.codecogs.com/gif.latex?N(x)&space;=&space;(M&space;-&space;\overline{m})^{2}&space;\cdot&space;x" title="N(x) = (M - \overline{m})^{2} \cdot x" />
      * feature maps are combined into 3 conspicuity maps
         * cross-scale addition to the scale four is used
         <img src="https://latex.codecogs.com/gif.latex?\widetilde{I}&space;=&space;\otimes_{c=2}^{4}&space;\otimes_{s=c&plus;3}^{4}&space;N(I(c,&space;s))" title="\widetilde{I} = \otimes_{c=2}^{4} \otimes_{s=c+3}^{4} N(I(c, s))" />
         <img src="https://latex.codecogs.com/gif.latex?\widetilde{C}&space;=&space;\otimes_{c=2}^{4}&space;\otimes_{s=c&plus;3}^{4}&space;\left&space;[&space;N(RG(c,s)&space;&plus;&space;N(BY(c,s)))&space;\right&space;]" title="\widetilde{C} = \otimes_{c=2}^{4} \otimes_{s=c+3}^{4} \left [ N(RG(c,s) + N(BY(c,s))) \right ]" />
         <img src="https://latex.codecogs.com/gif.latex?\widetilde{O}&space;=&space;\sum_{\theta&space;\in&space;\left&space;\{&space;0^{\circ},&space;45^{\circ},&space;90^{\circ},&space;135^{\circ}&space;\right&space;\}}&space;N\left&space;[\otimes_{c=2}^{4}&space;\otimes_{s=c&plus;3}^{4}&space;N(O(c,&space;s,&space;\theta))&space;\right&space;]" title="\widetilde{O} = \sum_{\theta \in \left \{ 0^{\circ}, 45^{\circ}, 90^{\circ}, 135^{\circ} \right \}} N\left [\otimes_{c=2}^{4} \otimes_{s=c+3}^{4} N(O(c, s, \theta)) \right ]" />
      * saliency map is calculated
         <img src="https://latex.codecogs.com/gif.latex?S&space;=&space;\frac{1}{3}&space;\cdot&space;\left&space;[&space;N(\widetilde{I})&space;&plus;&space;N(\widetilde{C})&space;&plus;N(\widetilde{O})&space;\right&space;]" title="S = \frac{1}{3} \cdot \left [ N(\widetilde{I}) + N(\widetilde{C}) +N(\widetilde{O}) \right ]" />
      * inhibition of return is used to shift focus
    <b></b>
    <b></b>
    * <b>Laurent Itti, Christof Koch, "A saliency-based search mechanism for overt and covert shifts of visual attention," in <i>Vision Research</i>, Volume 40, 2000.</b>
      * based on the IK bottom-up model, but used with high-resolution (6144x4096) images of military vehicles
      * realization, that normalizing feature maps and adding them up yields poor performance. Either it should be:
         * learning linear map combination weights (40)
         * within-feature competition scheme
            * feature map is normalized to fixed range (0..1)
            * feature map is convolved with 2D Difference-of-gaussian kernel (DoG)
            * original image is added to the result
            <img src="https://latex.codecogs.com/gif.latex?M&space;\leftarrow&space;\left&space;|&space;M&space;&plus;&space;M&space;*&space;DoG&space;-&space;C_{inh}&space;\right&space;|_{\geq&space;0}" title="M \leftarrow \left | M + M * DoG - C_{inh} \right |_{\geq 0}" />
            * this is done iteratively ~ 10 times for feature map
            * feature maps are across-scales added into 3 conspicuity maps
            * 10 iterations of formula is applied to conspicuity maps
            * conspicuity maps are linearly summed into unique saliency map
</pre>
</body>
</html>
