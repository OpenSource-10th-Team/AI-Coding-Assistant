import os
from typing import Literal
import warnings
warnings.filterwarnings("ignore")  # 경고 없애기

from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()  # transformers 모든 info/warning 숨김

class Debug: # Debugging utility class #디버깅 역할을 할 클래스.
    def __init__(self, code:str=None): # code_file: str, code file directory
        if code == None:
            code = ""
        else :
            if code.endswith(".py") and os.path.isfile(code):   #code가 .py 파일이라면 .py의 코드를를 읽어오기.
                with open(code, "r", encoding="utf-8") as code_file:
                    self.code = code_file.read()
            else:   # code가 파일이 아니라면, 저장.
                self.code = code

    def get_code(self): #code를 입력 받는 함수
        code = ""
        print("검사받을 코드를 한 행씩 입력해주세요. (종료하려면 '!STOP' 입력)")
        while True:
            tmp = input()
            if not tmp.strip():    #빈 줄 건너뛰기.
                continue
            if tmp.strip()[0] == "!":   # '!'로 시작하는 경우, 명령어로 인식.
                if tmp.strip()[1:] == "STOP":   # '!STOP' 입력 시, 입력 종료.
                    break
                if tmp.strip()[1:] == "CHECK":
                    print(code)
            else :
                code += tmp + "\n"
        self.code = code
        
    def check_grammar(self, output_file_path: str = "output.txt", pylint_file_path: str = "pylint_output.txt", strength : Literal["strong", "weak"] = "weak") -> None: #문법 검사하는 메소드 #출력 파일이 두 개 생김, 모든 결과가 담긴 output.txt / 잘못된 부분만 출력해주는 pylint_output.txt
        if not self.code:
            print("No code to check.")
            return
        else:
            print("Checking code grammar...")
            run_pylint_to_file(self.code, output_file_path, pylint_file_path, strength)
            print(f"Grammar check completed. Output saved to {output_file_path}")
            with open(output_file_path, "r", encoding="utf-8") as file:
                print(file.read())
        

     
    
def run_pylint_to_file(code: str, output_file_path: str = "output.txt", pylint_file_path: str = "pylint_output.txt", strength : Literal["strong", "weak"] = "weak") -> None:
    """Run pylint on the provided code and save the output to a file."""
    import sys
    from pylint.lint import Run
    import os
    #code는 무조건 문자열만 받아야 함. .py 파일 받지 않음.
    tmp_file_path = "tmp_code.py"
    # Run pylint on the temporary file
    with open(tmp_file_path, "w", encoding="utf-8") as tmp_file:
            tmp_file.write(code)

        
    try:
        if strength == "weak":
            Run([tmp_file_path, f"--output={pylint_file_path}", "--msg-template='{line}:{column}/{msg_id}: {msg}'", "--errors-only"], exit=False)
        else:
            Run([tmp_file_path, f"--output={pylint_file_path}", "--msg-template='{line}:{column}/{msg_id}: {msg}'"], exit=False)
        _revise_code_with_pylint (tmp_file_path, pylint_file_path)
        #transfer tmp_file to output_file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            with open(tmp_file_path, "r", encoding="utf-8") as tmp_file:
                output_file.write(tmp_file.read())
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        # Clean up the temporary file
        os.remove(tmp_file_path)
    
# pylint_output 파일과 temp_code 파일의 내용을 비교. temp_code 파일의 내용에 pylint_output 파일의 내용을 추가하는 함수
def _revise_code_with_pylint(code_file_path: str, output_file_path: str = "pylint_output.txt") -> None:
    """Revise the code based on pylint output."""
    with open(output_file_path, "r", encoding="utf-8") as file:
        output_lines = file.readlines()
    with open(code_file_path, "r", encoding="utf-8") as file:
        code_lines = file.readlines()
    # 오류 메시지와 summary 구분을 위한 상태 사용
    in_error_section = True

    for i, line in enumerate(output_lines):
        if i == 0:
            continue
        if in_error_section:
            if not line.strip():
                in_error_section = False
                continue
            code_line_number = int(line.split(':')[0]) - 1
            answer = _make_answer_by_AI(code_lines, code_lines[code_line_number], line) #문제 코드와 코드의 오류 보내기.
            _add_string_to_line_in_file(code_file_path, code_line_number, f"{answer}")
        else:
            # 오류 섹션 넘어가면 아무것도 안함
            continue

def _add_string_to_line_in_file(file_path: str, line_number: int, add_string: str) -> None:
    """Add a string to a specific line in a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if 0 <= line_number < len(lines):   #코드 길이가 넘어가면 작성하지 않음.
        lines[line_number] = lines[line_number].rstrip() + " #" + add_string + "\n"

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
   
def _make_answer_by_AI(entire_code, code:str, error:str):
    import ai_model_deepseek
    prompt = """문제 코드, 발생 오류를 보고 오류를 없앨 수정 코드와 오류 발생 원인을 콜론(:) 뒤에 생성해주세요. 문제 코드, 발생 오류는 생성하지 말아주세요.  <-출력 금지
답변 생성 format을 지켜주세요.<-출력 금지
출력은 반드시 한 줄로 작성하고, 줄바꿈, 코드 블록, 불릿포인트, 기타 형식적 요소를 절대 사용하지 마세요. 단일 연속 문자열로만 출력하세요. <-출력 금지
수정 코드와 오류 발생 원인만 생성해주세요. <-출력 금지
반복 답변을 생성하지 말아주세요. <-출력 금지


#문제 코드 <- 출력 금지
{}

#발생 오류 - format : <line>:<column>/<message-code>: <message-text> (<optional-extra-info>) <- 출력 금지
{}

#답변 생성 
정답 코드 :,  오류 발생 원인 : """.format(entire_code, code, error)
    return ai_model_deepseek.get_AI_answer(prompt)

