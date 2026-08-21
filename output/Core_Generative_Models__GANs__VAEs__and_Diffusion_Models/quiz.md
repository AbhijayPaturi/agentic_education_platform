# Quiz: Core Generative Models: GANs, VAEs, and Diffusion Models

**Type**: summative
**Total Points**: 80
**Time Limit**: 60 minutes
**Passing Score**: 70%

## Questions

### Question 1 (Easy)

**Type**: multiple_choice

What is the primary goal of generative modeling?

- To classify data into distinct categories
- To learn data distributions in order to create realistic new samples
- To reduce the dimensionality of large datasets
- To optimize reinforcement learning policies

**Answer**: To learn data distributions in order to create realistic new samples
**Explanation**: Generative modeling aims to understand and capture the underlying distribution of data to generate new, realistic samples that reflect that distribution.
*Tests*: Understand the fundamental purpose of generative modeling

---

### Question 2 (Easy)

**Type**: multiple_choice

In a Generative Adversarial Network (GAN), what roles do the two neural networks play?

- Encoder and Decoder
- Generator creates fake samples, Discriminator distinguishes real from fake samples
- Both networks generate samples independently
- Both networks serve as discriminators for different datasets

**Answer**: Generator creates fake samples, Discriminator distinguishes real from fake samples
**Explanation**: GANs consist of two networks: the Generator synthesizes data resembling real samples, while the Discriminator learns to differentiate between real and generated data, driving adversarial learning.
*Tests*: Explain the roles of generator and discriminator in GANs

---

### Question 3 (Medium)

**Type**: true_false

Mode collapse in GANs refers to the generator producing a limited variety of outputs, failing to capture full data diversity.

**Answer**: True
**Explanation**: Mode collapse occurs when the GAN generator repeatedly outputs similar or identical samples, indicating poor coverage of the data distribution's modes.
*Tests*: Identify key challenges in GAN training

---

### Question 4 (Medium)

**Type**: multiple_choice

Which of the following best describes the Evidence Lower Bound (ELBO) objective optimized by Variational Autoencoders (VAEs)?

- Maximizing reconstruction accuracy without regularization
- A trade-off between data reconstruction loss and KL divergence between approximate posterior and prior
- Minimizing discriminator loss against generator samples
- Maximizing the variance of latent variables

**Answer**: A trade-off between data reconstruction loss and KL divergence between approximate posterior and prior
**Explanation**: ELBO balances reconstructing data well (likelihood term) with regularizing the latent space distribution (KL divergence), enabling meaningful latent representations.
*Tests*: Understand the VAE objective function and its components

---

### Question 5 (Medium)

**Type**: multiple_choice

What is the main purpose of the reparameterization trick in VAEs?

- To increase the capacity of the decoder network
- To enable gradient backpropagation through stochastic latent variable sampling
- To speed up data preprocessing
- To make the discriminator more powerful

**Answer**: To enable gradient backpropagation through stochastic latent variable sampling
**Explanation**: The reparameterization trick expresses latent variable sampling as a differentiable transformation, allowing gradients to flow and the VAE to be trained end-to-end efficiently.
*Tests*: Explain the importance and mechanism of the reparameterization trick in VAEs

---

### Question 6 (Easy)

**Type**: multiple_choice

How do diffusion models generate new data samples?

- By directly mapping noise to data in a single forward pass
- By iteratively adding noise followed by learned denoising steps in reverse
- Using adversarial loss to fool a discriminator network
- By encoding data into latent variables and decoding them

**Answer**: By iteratively adding noise followed by learned denoising steps in reverse
**Explanation**: Diffusion models first define a forward noising process that gradually corrupts data, then learn a reverse denoising process to reconstruct data from noise through multiple iterative steps.
*Tests*: Describe the core generation process in diffusion models

---

### Question 7 (Medium)

**Type**: true_false

Training a GAN is generally considered easier and more stable compared to diffusion models and VAEs.

**Answer**: False
**Explanation**: GANs are known for training instability issues like mode collapse and oscillations, whereas diffusion models tend to have more stable training albeit slower generation.
*Tests*: Compare training difficulties across GANs, VAEs, and diffusion models

---

### Question 8 (Medium)

**Type**: multiple_choice

Which metric is commonly used to evaluate GANs by quantifying the quality and diversity of generated images?

- BLEU score
- Fréchet Inception Distance (FID)
- Cross entropy loss
- Mean squared error (MSE)

**Answer**: Fréchet Inception Distance (FID)
**Explanation**: FID measures the distance between feature distributions of real and generated images to assess both quality and diversity, widely used for GAN evaluation.
*Tests*: Identify evaluation metrics relevant to GANs

---

### Question 9 (Hard)

**Type**: short_answer

Briefly explain the difference in latent space structure between VAEs and GANs.

**Answer**: VAEs have a smooth, continuous, and probabilistically regularized latent space, whereas GANs do not explicitly enforce latent space structure.
**Explanation**: VAEs use KL divergence regularization encouraging a well-structured latent space enabling interpolation and meaningful sampling; GANs focus on producing realistic outputs without constrained latent distributions.
*Tests*: Analyze structural differences in latent representation across generative models

---

### Question 10 (Medium)

**Type**: multiple_choice

Which statement correctly characterizes diffusion models compared to GANs and VAEs?

- Diffusion models generate samples faster than GANs
- Diffusion models rely heavily on adversarial training
- Diffusion models optimize likelihood with iterative denoising, offering stable training but slower generation
- Diffusion models do not use neural networks

**Answer**: Diffusion models optimize likelihood with iterative denoising, offering stable training but slower generation
**Explanation**: Diffusion models maximize a tractable likelihood through gradual denoising steps, providing stable training and high-quality samples, although sampling is computationally intensive compared to one-shot GAN/VAEs.
*Tests*: Compare key characteristics of diffusion models with GANs and VAEs

---

### Question 11 (Hard)

**Type**: multiple_choice

In the GAN objective function min_G max_D V(D, G), what does the generator try to minimize?

- Discriminator’s accuracy in detecting real data
- The probability that the discriminator correctly classifies fake data as fake
- The log probability that the discriminator classifies generated data as real
- The KL divergence between generated and data distributions

**Answer**: The log probability that the discriminator classifies generated data as real
**Explanation**: The generator aims to minimize the discriminator’s ability to distinguish generated fake samples from real, effectively minimizing the log(1 - D(G(z))) or maximizing log D(G(z)) in some variants.
*Tests*: Understand adversarial training objectives in GANs

---

### Question 12 (Medium)

**Type**: true_false

The reparameterization trick helps VAEs avoid the problem of non-differentiable sampling operations during training.

**Answer**: True
**Explanation**: Because sampling from a distribution is a stochastic operation, it blocks gradient flow; the reparameterization trick reformulates sampling to allow differentiation and backpropagation.
*Tests*: Explain the function of the reparameterization trick in enabling VAE training

---

### Question 13 (Hard)

**Type**: short_answer

Describe one advantage and one disadvantage of diffusion models compared to GANs.

**Answer**: Advantage: diffusion models train more stably and maximize likelihood, producing diverse high-fidelity samples. Disadvantage: sampling is much slower due to iterative denoising steps.
**Explanation**: Diffusion models avoid adversarial training issues, yielding reliable generation quality, but their iterative process requires more computation time than GANs’ one-step generation.
*Tests*: Critically evaluate strengths and weaknesses of diffusion models relative to GANs

---

### Question 14 (Medium)

**Type**: multiple_choice

Hybrid generative models such as VAE-GANs aim to:

- Combine GANs’ sharp image synthesis with VAEs’ probabilistic latent space
- Simplify the diffusion model's sampling process
- Replace backpropagation with reinforcement learning
- Eliminate the need for a discriminator network

**Answer**: Combine GANs’ sharp image synthesis with VAEs’ probabilistic latent space
**Explanation**: VAE-GAN hybrids seek to leverage VAEs’ latent structure and likelihood-based learning with GANs’ ability to produce sharper, more realistic outputs, balancing quality and regularization.
*Tests*: Recognize motivations behind combining generative model architectures

---

### Question 15 (Hard)

**Type**: multiple_choice

What role does score matching play in the training of diffusion models?

- It trains the discriminator to improve generator quality
- It helps to estimate gradients of the data log-density to learn denoising
- It optimizes the KL divergence between latent distributions
- It encodes latent variables for efficient sampling

**Answer**: It helps to estimate gradients of the data log-density to learn denoising
**Explanation**: Score matching enables the diffusion model to learn the gradient (score) of the data distribution’s log-probability, guiding the reverse denoising to generate high-quality samples.
*Tests*: Explain the mathematical foundation of score matching in diffusion models

---

## Study Tips
Review the core concepts and architectures of GANs, VAEs, and Diffusion models, focusing on their generation processes, objectives, and training challenges. Pay attention to understanding key terms like mode collapse, ELBO, reparameterization trick, and score matching. Study diagrams illustrating architecture and sampling flows and practice explaining differences and trade-offs between models. Reviewing implementation snippets will help connect theory to practice. Finally, test yourself by summarizing advantages and disadvantages to deepen comparative insight.