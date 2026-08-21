# Quiz: Hands-on Development with genAI Frameworks and Tools

**Type**: summative
**Total Points**: 70
**Time Limit**: 60 minutes
**Passing Score**: 70%

## Questions

### Question 1 (Easy)

**Type**: multiple_choice

What best defines generative AI as discussed in the course?

- Models that classify input data into predefined categories
- Models that generate new content based on learned data distributions
- Systems that store large datasets for future retrieval
- Algorithms that only summarize existing documents

**Answer**: Models that generate new content based on learned data distributions
**Explanation**: Generative AI models produce novel and coherent outputs by learning underlying patterns of datasets, unlike discriminative models which classify or predict predefined labels.
*Tests*: Understand the fundamental concept of generative AI

---

### Question 2 (Medium)

**Type**: multiple_choice

Which of the following is NOT typically considered a genAI development framework or tool?

- Hugging Face Transformers
- Diffusers library
- Django web framework
- OpenAI SDK

**Answer**: Django web framework
**Explanation**: Django is a general-purpose web framework, not specialized for generative AI tasks, whereas the others are designed specifically to support genAI model training, fine-tuning, or deployment.
*Tests*: Identify common frameworks and tools for genAI development

---

### Question 3 (Easy)

**Type**: true_false

Fine-tuning a pretrained generative AI model involves training it further on task-specific data to improve performance in that domain.

**Answer**: True
**Explanation**: Fine-tuning adapts a general pretrained model to specific contexts by continuing training on domain-relevant datasets, enhancing generation quality.
*Tests*: Explain the purpose and process of fine-tuning genAI models

---

### Question 4 (Medium)

**Type**: multiple_choice

During genAI model evaluation, which metric is primarily used to measure a model’s uncertainty in predicting text?

- FID (Fréchet Inception Distance)
- BLEU score
- Perplexity
- Accuracy

**Answer**: Perplexity
**Explanation**: Perplexity quantifies how well a language model predicts a sample. Lower perplexity indicates less uncertainty and better predictive performance, especially relevant for text generation.
*Tests*: Understand key metrics for evaluating genAI models

---

### Question 5 (Easy)

**Type**: short_answer

Name two hardware or software requirements important for hands-on development with genAI frameworks.

**Answer**: Python 3.7+ environment and GPU (e.g., NVIDIA CUDA compatible)
**Explanation**: Python 3.7+ is a common programming environment, and GPUs are critical for handling the computational load of training and inference in genAI tasks.
*Tests*: Recall essential hardware and software requirements for genAI development

---

### Question 6 (Medium)

**Type**: multiple_choice

What is a recommended practice when setting up your genAI development environment to manage dependencies and package versions?

- Installing all packages globally without isolation
- Using virtual environments like venv or conda
- Relying solely on system Python without a package manager
- Avoiding version control systems like Git

**Answer**: Using virtual environments like venv or conda
**Explanation**: Virtual environments isolate project dependencies, preventing conflicts and making environment management clean and reproducible.
*Tests*: Demonstrate proper environment setup practices for genAI projects

---

### Question 7 (Medium)

**Type**: true_false

Model compression techniques such as quantization and pruning help improve genAI model inference speed without significantly degrading output quality.

**Answer**: True
**Explanation**: Compression reduces model size and computational requirements which accelerates inference, often with minimal accuracy loss when done carefully.
*Tests*: Explain optimization techniques to enhance genAI model performance

---

### Question 8 (Medium)

**Type**: multiple_choice

Which step is NOT part of the typical genAI development workflow presented?

- Prepare data and tokenizers
- Write model architecture from scratch
- Fine-tune model on custom data
- Deploy model for inference

**Answer**: Write model architecture from scratch
**Explanation**: The workflow emphasizes loading pretrained models rather than building them from scratch, streamlining development through fine-tuning and deployment.
*Tests*: Understand typical workflow steps in genAI development

---

### Question 9 (Medium)

**Type**: short_answer

List one ethical consideration important in genAI development and why it matters.

**Answer**: Bias in training data, because it can lead to unfair or harmful outputs.
**Explanation**: Bias affects the fairness and inclusivity of generated results, potentially perpetuating stereotypes or misinformation; ethical awareness guides responsible model use.
*Tests*: Recognize key ethical challenges of generative AI

---

### Question 10 (Easy)

**Type**: code_problem

Given this Python snippet loading a Hugging Face pipeline:

```python
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
output = generator('Hello world', max_length=20)
print(output[0]['generated_text'])
```

What is the primary purpose of this code?

**Answer**: To load a pretrained text generation model and produce text continuation starting with 'Hello world'.
**Explanation**: It imports the pipeline abstraction, loads the GPT-2 model for text generation, then generates text up to 20 tokens, demonstrating pretrained model usage.
*Tests*: Apply basic code to use pretrained genAI models

---

### Question 11 (Medium)

**Type**: multiple_choice

Which library specializes in diffusion models for image generation?

- Hugging Face Transformers
- Diffusers library
- OpenAI SDK
- PyTorch Lightning

**Answer**: Diffusers library
**Explanation**: The Diffusers library focuses on diffusion-based generative models, a popular approach for advanced image synthesis.
*Tests*: Identify specialized genAI libraries according to model type

---

### Question 12 (Hard)

**Type**: multiple_choice

In the context of evaluating genAI models, which method is NOT typically used?

- Human qualitative review of outputs
- BLEU score comparison to reference texts
- Perplexity measurement
- Counting the number of model parameters

**Answer**: Counting the number of model parameters
**Explanation**: While parameter count indicates model size, evaluation focuses on quality and performance metrics like BLEU, perplexity, and human judgement rather than size alone.
*Tests*: Differentiate evaluation metrics and their appropriate use

---

### Question 13 (Medium)

**Type**: multiple_choice

Why is version control (e.g., Git) important when developing genAI applications?

- It allows collaborative code management and history tracking
- It automatically improves model accuracy
- It prevents any coding errors
- It handles GPU memory optimization

**Answer**: It allows collaborative code management and history tracking
**Explanation**: Version control manages code versions and supports multiple developers working together, aiding reproducibility and debugging but does not directly impact model accuracy or hardware.
*Tests*: Explain the importance of software development best practices in genAI projects

---

### Question 14 (Easy)

**Type**: short_answer

What is one advantage of using cloud platforms (e.g., AWS, GCP) in genAI development?

**Answer**: Access to scalable hardware resources like GPUs without upfront infrastructure costs.
**Explanation**: Cloud platforms provide flexible and powerful compute resources on demand, facilitating large-model training and deployment without local hardware.
*Tests*: Understand hardware options for scaling genAI workloads

---

### Question 15 (Hard)

**Type**: multiple_choice

Which practice helps ensure ethical deployment of genAI models in applications?

- Providing user transparency and obtaining informed consent
- Maximizing model size regardless of output nature
- Removing all human oversight to speed deployment
- Ignoring potential biases in generated content

**Answer**: Providing user transparency and obtaining informed consent
**Explanation**: Ethical deployment involves being clear with users about AI involvement and ensuring consent, thereby maintaining trust and responsibility.
*Tests*: Apply ethical principles in genAI application deployment

---

## Study Tips
Focus on understanding generative AI concepts and workflows from theory to practical coding. Practice setting up environments and running basic code examples. Review common frameworks and the evaluation metrics used to assess models. Reflect on the ethical implications to appreciate responsible AI development. Hands-on exercises and revisiting deployment scenarios will reinforce learning.