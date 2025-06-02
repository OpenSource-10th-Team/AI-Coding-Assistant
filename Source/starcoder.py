from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ✅ 모델 이름
model_name = "bigcode/starcoder2-3b"

# ✅ 2. 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_fast=True
)

# ✅ 3. 모델 로드 (4bit, device_map 자동 할당, CPU 오프로드 가능)
# 기존 코드 유지하면서 이 부분만 추가하세요
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    max_memory={"cpu": "12GiB"}  
)

# ✅ 4. 테스트용 응답 함수 (텍스트 프롬프트 입력 → 텍스트 출력)
def generate_response(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ✅ 5. 테스트용 주석 생성 함수 (코드 입력 → 주석 붙은 코드 출력)
def annotate_code_with_comments(code: str):
    prompt = f"다음은 파이썬 코드입니다. 각 줄에 주석을 달아주세요.\n\n{code}"
    return generate_response(prompt)

# ✅ 6. 테스트용 코드 수정 함수 (코드 입력 → 수정 된 코드 출력)
def modify_code(code: str):
    prompt = f"다음은 파이썬 코드입니다. 코드에 오류가 있으면 수정해주세요.\n\n{code}"
    return generate_response(prompt)


# ✅ 7. 실행 예시
#if 문에 코드 생성(예시:버블정렬코드 만들어줘)과 코드 수정, 주석 추가의 경우를 나눠서 입력받도록 만들고
#수정과 주석은 코드 입력이니 End Code 입력 전까지 계속 입력받도록 변경
if __name__ == "__main__":
    print("🧠 StarCoder2-3B model loaded.")
    while True:
        print("\n'생성', '수정', '주석', '종료' 중 하나를 입력하시오")
        prompt = input("💬 Prompt: ")
        if prompt.lower() in ["exit", "quit", "종료"]:
            break

        elif prompt.lower() in ["생성"]:
            print('\n✏️ 원하는 코드 형태를 적어주세요.')
            code_type = input("")
            response = generate_response(code_type)

        elif prompt.lower() in ["주석"]:
            print('\n✏️ 코드를 입력해주세요.')
            print("입력을 마치려면 'End Code' 를 입력하세요.")
            code_lines = []

            while True:
                line = input()
                if line.strip() == "End Code":
                    break
                code_lines.append(line)

            user_code = "\n".join(code_lines)
            response = annotate_code_with_comments(user_code)

        elif prompt.lower() in ["수정"]:
            print('\n✏️ 코드를 입력해주세요.')
            print("입력을 마치려면 'End Code' 를 입력하세요.")
            code_lines = []

            while True:
                line = input()
                if line.strip() == "End Code":
                    break
                code_lines.append(line)

            user_code = "\n".join(code_lines)
            response = modify_code(user_code)

        else:
            print("잘못된 입력입니다")
            response = "다시 입력해 주세요"
        
        print("\n🧠 답변:\n", response)