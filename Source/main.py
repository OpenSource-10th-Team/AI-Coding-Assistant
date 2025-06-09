from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import Debug

# ✅ 모델 이름
model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"

# ✅ 토크나이저 로드 (대화형 입력 지원)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# ✅ 디바이스 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ 모델 로드
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16 if device.type == "cuda" else torch.float32
).to(device)

# ✅ deepseek 방식의 응답 생성 함수
def generate_response(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_new_tokens=512,
            temperature=0.6,
            top_p=0.8,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)

# ✅ 주석 생성 함수
def annotate_code_with_comments(code: str):
    prompt = f"다음은 파이썬 코드입니다. 각 줄에 주석을 달아주세요. 반복된 답변은 출력하지 말아주세요.\n\n{code}"
    return generate_response(prompt)

# ✅ 코드 수정 함수
def modify_code(code: str):
    prompt = f"다음은 파이썬 코드입니다. 코드에 오류가 있으면 수정해주세요. 반복된 답변은 출력하지 말아주세요.\n\n{code}"
    return generate_response(prompt)

# ✅ 코드 생성 함수
def create_code(description: str):
    prompt = f"다음은 원하는 파이썬 코드에 대한 설명입니다. 적절한 파이썬 코드를 만들어 주세요. 반복된 답변은 출력하지 말아주세요.\n\n{description}"
    return generate_response(prompt)

# ✅ 실행부
if __name__ == "__main__":
    print("🧠 DeepSeek Coder 1.3B 모델 로드 완료.")
    while True:
        print("\n'생성', '수정', '주석', '종료', '디버그' 중 하나를 입력하시오")
        command = input("💬 Prompt: ").strip()

        if command.lower() in ["exit", "quit", "종료"]:
            break

        elif command == "생성":
            print("\n✏️ 원하는 코드에 대한 설명을 입력하세요.")
            description = input()
            response = create_code(description)

        elif command == "주석":
            print("\n✏️ 코드를 입력하세요. 종료하려면 'End Code' 입력")
            lines = []
            while True:
                line = input()
                if line.strip() == "End Code":
                    break
                lines.append(line)
            user_code = "\n".join(lines)
            response = annotate_code_with_comments(user_code)

        elif command == "수정":
            print("\n✏️ 코드를 입력하세요. 종료하려면 'End Code' 입력")
            lines = []
            while True:
                line = input()
                if line.strip() == "End Code":
                    break
                lines.append(line)
            user_code = "\n".join(lines)
            response = modify_code(user_code)
        
        elif command == "디버그":
            print("\n✏️ 코드를 입력하세요. 또는 .py 경로를 입력하세요. 종료하려면 'End Code' 입력")
            lines = []
            while True:
                line = input()
                if line.strip() == "End Code":
                    break
                lines.append(line)
            user_code = "\n".join(lines)
            D = Debug.Debug(user_code)
            
            while(True):
                r = input("강한 검사와 약한 검사 중 선택해주세요 (강한 검사 : s, 약한 검사 w)")
                if r == 's' or r == 'w':
                    break
            if r == 'w' :
                response = D.check_grammar(strength='weak')
            else : 
                response = D.check_grammar(strength='strong')
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")
            continue

        print("\n🧠 답변:\n", response)
