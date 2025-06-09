# AI-Coding-Assistant (ACA)

---

## Abstract

AI-Coding-Assistant (ACA) guides you toward making your code better and better.  
It offers three main features:

1. Generates code based on algorithm descriptions.  
2. Detects and corrects errors in your code.  
3. Provides helpful advice to improve your coding skills.

---

## Model

ACA uses the [DeepSeek Coder 1.3B Instruct](https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct) model,  
an instruction-tuned open-source code generation model developed by [DeepSeek AI](https://huggingface.co/deepseek-ai).  
DeepSeek Coder is instruction-tuned, meaning it has been specifically trained to follow human instructions,  
making it well-suited for tasks like code modification, explanation, and annotation.

---

## Requirements

### Software

- Python ≥ 3.9  
- PyTorch ≥ 2.0  
- `transformers` (by Hugging Face)  
- `accelerate` (optional, for faster performance)  

### Hardware

- GPU with at least 8GB of VRAM (e.g., NVIDIA RTX 3060 or higher recommended)  
- CPU is also supported but slower

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/OpenSource-10th-Team/AI-Coding-Assistant.git
cd AI-Coding-Assistant
```

2. install Python dependencies:

```bash
pip install torch transformers accelerate
```

> **Additional Info:**  
> - The default installation of 'pipe install torch' is the CPU version.  
> - For GPU version installation, check the [PyTorch official site] (https://pytorch.org/) for commands that match the CUDA version.  
> - For example: In CUDA 11.8 environments
> ```bash
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
> ```

---

## Usage
examples
 
### create
Run the assistant:

```bash
python main.py
```

You will be prompted to choose one of the following actions:
- '생성' – generate code from a description

- '수정' – fix or improve your code

- '주석' – annotate code with line-by-line comments

- '종료' – exit the program

- '디버그' – create debugging files. 

Example:

```text
💬 Prompt: 생성
✏️ 원하는 코드에 대한 설명을 입력하세요.
정수를 입력받아 소수인지 판별하는 코드를 만들어줘
```

### debug

Example:

```text
💬 코드 입력:        #or .py file path
def f(x):
  return x > 1
End Code

💬 결과:
Checking code grammar...
Grammar check completed. Output saved to output.txt
```

---
## COLAB
you can test our program with entering this [colab link](https://colab.research.google.com/drive/1qrpBMnsv9G6QOem_QWv-0f-6uocGMTwJ?usp=sharing) and copy notebook.
    
    
## License

This project uses open-source models and tools. Please refer to the individual model licenses for full terms:

- DeepSeek Coder License

All original code in this repository is under the MIT License unless otherwise stated.
