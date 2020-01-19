## Current
[Bottom-up Attention, Models of](https://arxiv.org/pdf/1810.05680.pdf)

## Plan
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<pre>

INTRO:
bottom-up
	45, 36 - itti & koch
top-down aka context-driven
	52, 51, 2, 27, 57, 11

dynamic saliency vs static saliency (taking into account video frames) : 38

The computational modelling effort

Phase 1 - early computational works (IK 1985, Feature Integration Theory)
Phase 2 - extend ideas presented in Phase 1, implemntation of IK model
Phase 3 - Spectral residual model by Hou and Zhang in 2007 is an example of models in this phase
Phase 4 - neural networks, notable example is SALICON model (2015) with SALICON dataset. (first model that was trained on large scale attention dataset)

free viewing in the context of bottom-up attention: 64
models designed for specific task: 36, 64, 24, 69

BOTTOM-UP ATTENTION MODELLING: PRE DEEP LEARINNG ERA
computational architecture: 45, 38, 37, 56, 34, (59, 61) - where humans are viewing during passive viewing

static saliency models -> 	Attention for Information maximization (AIM) 	12
				Graph-based Visual Saliency (GBVS) 		26
				Saliency using Natural statistics (SUN) 	81
				Boolean Map based saliency (BMS) 		80
				Spectral Residual saliency (SR) 		32
				Judd et al model 				42

dynamic saliency models -> 	OBDL						31

BOTTOM-UP ATTENTION MODELLING: DEEP LEARINNG ERA
transfer learning is used

static saliency models -> 	eDN			72
				DeepGaze I & II		59
				Mr-CNN			55
				SALICON			33
				DeepFix			48
				SAM-ResNet		19
				EML-Net			39

dynamic saliency models -> 	Two-stream network	1
				Chaabouni		18
				Bazzani			3
				OM-CNN			40
				Gorji & Clark		23
				ACLNet			73
				SG-FCN			67

LSTM - 30

CNN-s may generalize classic IK models. consider a CNN with single convolutinal layer folloved 
by FC layer trained to predict fixations. This generalized the Itti model and learnig to cmbine feature maps
(43, 4, 75)

FC learns the linear combination weights.

classic models are not able to extract higher level object, parts of objects

classic model wins deep models 33 !!!!!!!!!!!!!!!!!

</pre>
</body>
</html>
