import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import sys
from collections import defaultdict

print("프로그램 시작...")

class ImageToCode:
    def __init__(self):
        print("GUI 초기화 중...")
        self.window = tk.Tk()
        self.window.title("이미지를 코드로 변환")
        self.window.geometry("800x600")
        
        print("GUI 구성요소 초기화 중...")
        # GUI 구성요소 초기화
        self.setup_gui()
        
        # 이미지 데이터 초기화
        self.image = None
        self.processed_image = None
        self.generated_code = ""
        print("초기화 완료!")
        
    def setup_gui(self):
        try:
            # 왼쪽 프레임 (이미지 표시용)
            self.left_frame = tk.Frame(self.window)
            self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
            
            # 오른쪽 프레임 (코드 표시용)
            self.right_frame = tk.Frame(self.window)
            self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
            
            # 이미지 캔버스
            self.canvas = tk.Canvas(self.left_frame, width=400, height=400)
            self.canvas.pack()
            
            # 픽셀 간격 입력
            self.pixel_spacing_frame = tk.Frame(self.right_frame)
            self.pixel_spacing_frame.pack(pady=5)
            tk.Label(self.pixel_spacing_frame, text="픽셀 간격:").pack(side=tk.LEFT)
            self.pixel_spacing = tk.Entry(self.pixel_spacing_frame, width=5)
            self.pixel_spacing.insert(0, "5")
            self.pixel_spacing.pack(side=tk.LEFT)
            
            # 점 크기 입력
            self.dot_size_frame = tk.Frame(self.right_frame)
            self.dot_size_frame.pack(pady=5)
            tk.Label(self.dot_size_frame, text="점 크기:").pack(side=tk.LEFT)
            self.dot_size = tk.Entry(self.dot_size_frame, width=5)
            self.dot_size.insert(0, "3")
            self.dot_size.pack(side=tk.LEFT)
            
            # 상태 표시 레이블
            self.status_label = tk.Label(self.right_frame, text="이미지를 선택해주세요")
            self.status_label.pack(pady=5)
            
            # 버튼들
            tk.Button(self.right_frame, text="이미지 선택", command=self.load_image).pack(pady=5)
            tk.Button(self.right_frame, text="코드 생성", command=self.generate_code).pack(pady=5)
            tk.Button(self.right_frame, text="코드 저장", command=self.save_code).pack(pady=5)
            
            # 코드 표시 영역
            self.code_text = tk.Text(self.right_frame, width=40, height=20)
            self.code_text.pack(pady=5)
            
            print("GUI 구성요소 설정 완료!")
            
        except Exception as e:
            print(f"GUI 설정 중 오류 발생: {str(e)}")
            sys.exit(1)
        
    def load_image(self):
        print("이미지 선택 대화상자 열기...")
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if file_path:
            try:
                print(f"선택된 이미지: {file_path}")
                # 이미지를 컬러로 로드
                self.image = cv2.imread(file_path)
                if self.image is None:
                    raise Exception("이미지를 로드할 수 없습니다.")
                
                print("이미지 크기 조정 중...")
                # 이미지 크기 조정
                height, width = self.image.shape[:2]
                max_size = 400
                if width > height:
                    new_width = max_size
                    new_height = int(height * (max_size / width))
                else:
                    new_height = max_size
                    new_width = int(width * (max_size / height))
                
                self.processed_image = cv2.resize(self.image, (new_width, new_height))
                
                print("GUI에 이미지 표시 중...")
                # BGR에서 RGB로 변환하여 GUI에 표시
                rgb_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image)
                self.tk_image = ImageTk.PhotoImage(pil_image)
                self.canvas.create_image(200, 200, image=self.tk_image)
                self.status_label.config(text="이미지 로드 완료!")
                print("이미지 로드 완료!")
                
            except Exception as e:
                print(f"이미지 로드 중 오류 발생: {str(e)}")
                messagebox.showerror("에러", str(e))
                self.status_label.config(text="이미지 로드 실패")
                
    def generate_code(self):
        if self.processed_image is None:
            print("이미지가 로드되지 않았습니다.")
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return
            
        try:
            print("코드 생성 중...")
            # 코드 생성
            self.generated_code = self.create_turtle_code()
            
            # 생성된 코드를 텍스트 영역에 표시
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, self.generated_code)
            
            self.status_label.config(text="코드가 생성되었습니다.")
            print("코드 생성 완료!")
            messagebox.showinfo("완료", "코드가 생성되었습니다.")
            
        except Exception as e:
            print(f"코드 생성 중 오류 발생: {str(e)}")
            messagebox.showerror("오류", f"코드 생성 중 오류 발생: {str(e)}")
            self.status_label.config(text="코드 생성 실패")
            
    def create_turtle_code(self):
        print("Turtle 코드 생성 중...")
        try:
            spacing = int(self.pixel_spacing.get())
            dot_size = int(self.dot_size.get())
        except ValueError:
            messagebox.showerror("에러", "픽셀 간격과 점 크기는 숫자여야 합니다.")
            return ""
        
        # 이미지를 흑백으로 변환
        gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        
        code = [
            "import turtle",
            "screen = turtle.Screen()",
            "screen.title('Generated Drawing')",
            "t = turtle.Turtle()",
            "t.speed(0)",  # 최대 속도
            "t.hideturtle()",  # 터틀 숨기기
            "screen.tracer(0)",  # 화면 업데이트 비활성화
            "",
            "# 점 그리기 함수",
            "def draw_dot(x, y, size):",
            "    t.penup()",
            "    t.goto(x, y)",
            "    t.pendown()",
            "    t.dot(size)",
            "",
            "# 검은 점 위치 저장",
            "black_dots = []",
        ]
        
        height, width = binary_image.shape
        for y in range(0, height, spacing):
            for x in range(0, width, spacing):
                if binary_image[y, x] < 127:  # 검은색 픽셀
                    # 좌표계 변환 (이미지 중앙이 원점)
                    screen_x = x - width/2
                    screen_y = (height/2) - y
                    code.append(f"black_dots.append(({screen_x}, {screen_y}))")
        
        code.extend([
            "",
            "# 모든 점 그리기",
            "for x, y in black_dots:",
            f"    draw_dot(x, y, {dot_size})",
            "",
            "screen.update()",  # 최종 업데이트
            "screen.mainloop()"
        ])
        
        print("Turtle 코드 생성 완료!")
        return "\n".join(code)
        
    def save_code(self):
        if not self.generated_code:
            print("생성된 코드가 없습니다.")
            messagebox.showwarning("경고", "먼저 코드를 생성해주세요.")
            return
            
        print("저장 대화상자 열기...")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py")],
            initialfile="generated_drawing.py"
        )
        
        if file_path:
            try:
                print(f"코드를 파일에 저장 중: {file_path}")
                # 디렉토리가 없는 경우 생성
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.generated_code)
                self.status_label.config(text=f"코드가 저장되었습니다: {os.path.basename(file_path)}")
                print("코드 저장 완료!")
                messagebox.showinfo("완료", "코드가 저장되었습니다.")
                
            except Exception as e:
                print(f"파일 저장 중 오류 발생: {str(e)}")
                messagebox.showerror("오류", f"파일 저장 중 오류 발생: {str(e)}")
                self.status_label.config(text="코드 저장 실패")
                
    def run(self):
        print("메인 루프 시작...")
        self.window.mainloop()
        print("프로그램 종료.")

if __name__ == "__main__":
    try:
        print("프로그램 인스턴스 생성 중...")
        app = ImageToCode()
        print("프로그램 실행...")
        app.run()
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {str(e)}")
        sys.exit(1)